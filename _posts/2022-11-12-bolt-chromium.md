---
layout: post
title: "Optimizing Chromium with BOLT"
date: 2022-11-12
comments: true
---
## Intro
As you might already know, BOLT helps achieve peak performance on top of compiler's best effort, i.e. over both PGO and LTO.
This post will cover the necessary steps to experiment with optimizing Chromium with BOLT. 

## Plan
We'll tackle this problem in the following steps:
- produce pre-bolt chromium binary with preserved (static) relocations
- collect the profile
- optimize the binary
- get performance data

## Building Chromium
I followed the steps here: [Checking out and building Chromium on Linux](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md).
Things worked for me on this revision:
```
commit 2570036418a961586b01697e1f79b9d9380fd103 (origin/main, origin/HEAD)
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Mon Jan 2 22:34:43 2023 +0000

    Roll Skia from 809e328ed55c to 697f9b541a0e (1 revision)
```

We'd need to enable the "official" build configuration which includes PGO:

```bash
# First fetch gclient config, tip https://stackoverflow.com/a/35382199
gclient config https://chromium.googlesource.com/chromium/src.git
gclient sync
gclient runhooks
```

Then add `"checkout_pgo_profiles": True` to custom_vars in the gclient config, see [here](https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/pgo.md#generating-pgo-profiles)
```bash
vim .gclient
gclient runhooks
```

If the `runhooks` step complains about invalid gs credentials, run the `gsutil config` command suggested in the output.
(Note: `gsutil` lives in depot_tools folder). Click on the link, log in to your Google account, paste the authorization code. Use 0 as project-id (worked for me).
Then repeat `gclient runhooks` step.

Set gn variables, see [here](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md#smaller-builds)
```bash
gn args out/Default
```

We need to disable Clang CFI as BOLT doesn't understand added symbols (see [bug](https://github.com/facebookincubator/BOLT/issues/302)):

Put the following to the file:
```
is_debug = false
is_official_build = true
symbol_level = 0
is_cfi = false
```
And finally build with: 
```
autoninja -C out/Default chrome
```

Chromium binary has a very large text section:

| Build | .text size |
|--|--|
| Release | 210MB |
| Official | 171MB |


## Pre-BOLT Chromium binary
In order to enable function reordering, one of the most important optimizations, the input binary needs to have .text relocations 
preserved by the linker.

I had to tweak build configuration to actually achieve this:
```diff
diff --git a/build/config/BUILDCONFIG.gn b/build/config/BUILDCONFIG.gn
index a373e55a33..7960db4c81 100644
--- a/build/config/BUILDCONFIG.gn
+++ b/build/config/BUILDCONFIG.gn
@@ -352,8 +352,15 @@ default_compiler_configs = [
   "//build/config/compiler/pgo:default_pgo_flags",
   "//build/config/coverage:default_coverage",
   "//build/config/sanitizers:default_sanitizer_flags",
+  "//build/config/compiler:emit-relocs",
 ]

 if (is_win) {
   default_compiler_configs += [
     "//build/config/win:default_cfg_compiler",
diff --git a/build/config/compiler/BUILD.gn b/build/config/compiler/BUILD.gn
index 3eede98ae4..8cbb5c8d79 100644
--- a/build/config/compiler/BUILD.gn
+++ b/build/config/compiler/BUILD.gn
@@ -233,6 +233,15 @@ config("no_unresolved_symbols") {
   }
 }

+# Emit relocs for BOLT
+config("emit-relocs") {
+  if (!using_sanitizer && is_linux) {
+    ldflags = [
+      "-Wl,--emit-relocs",
+    ]
+  }
+}
+
 # compiler ---------------------------------------------------------------------
 #
 ```
 
 With that, rerunning `autoninja -C out/Default chrome` produces the binary with text relocations:
 
```bash
$ readelf -We out/Default/chrome | grep rela.text
  [32] .rela.text        RELA            0000000000000000 11065398 ba63780 18   I 45  16  8
```
 
## Collecting the profile
The steps are described on BOLT's GitHub page: [Step 1: Collect Profile](https://github.com/llvm/llvm-project/tree/main/bolt#step-1-collect-profile).

It took me several iterations to figure out the sampling rate which can be adjusted with -c/-F flags for perf record.
I ended up with sampling frequency of 10Khz (`-F 10000`) to increase the quantity of collected profile.

The representative workload is borrowed from PGO build guide here: [Run representative benchmarks to produce profiles](https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/pgo.md#generating-pgo-profiles)

The profiling invocation looks like this:
```bash
perf record -e cycles:u -j any,u -o perf.data -- \
vpython3 tools/perf/run_benchmark speedometer2 \
--assert-gpu-compositing --browser=exact \
--browser-executable=out/Default/chrome
```

## Converting the profile
In order to simplify the use of profile (i.e. avoid converting it multiple times), we'll use perf2bolt to convert raw perf data to a profile:
```bash
perf2bolt out/Default/chrome -perfdata=perf.data -o perf.fdata -strict=0
```

## Optimizing the binary
Again, we're following BOLT's manual: [Step 3: Optimize with BOLT](https://github.com/llvm/llvm-project/tree/main/bolt#step-3-optimize-with-bolt).
There are a couple of Chromium's quirks:
- The optimized binary needs to be at the same path as the original (i.e. in `out/Default/` folder)
- Chromium employs V8 as a JS VM. It still has the same issue with code pointers described in this post: [Optimizing NodeJS with BOLT](https://aaupov.github.io/blog/2020/10/08/bolt-nodejs).

Here's the command line that I used:
```
llvm-bolt out/Default/chrome -o out/Default/chrome.bolt \
  -data=perf.fdata -dyno-stats \
  -reorder-blocks=ext-tsp -reorder-functions=hfsort \
  -split-functions -split-all-cold -split-eh \
  -skip-funcs=Builtins_.\*
```

BOLT optimization dynostats:
```

            11566179 : executed forward branches (-8.2%)
              748444 : taken forward branches (-65.7%)
             3764854 : executed backward branches (+37.6%)
             1565996 : taken backward branches (+3.4%)
              486354 : executed unconditional branches (-48.7%)
             1231833 : all function calls (=)
              483079 : indirect calls (=)
              139827 : PLT calls (=)
           107491548 : executed instructions (-0.9%)
            29806370 : executed load instructions (-0.0%)
            11393188 : executed store instructions (-0.0%)
               93934 : taken jump table branches (=)
                   0 : taken unknown indirect branches (=)
            15817387 : total branches (-2.8%)
             2800794 : taken branches (-39.7%)
            13016593 : non-taken conditional branches (+11.9%)
             2314440 : taken conditional branches (-37.4%)
            15331033 : all conditional branches (-0.0%)
```

## Perf testing

Testing system:
* Intel ADL i7-12700K
* Ubuntu 22.04

For performance testing I used the same Speedometer2 invocation (sorry, no proper train/test split):
```bash
vpython3 tools/perf/run_benchmark speedometer2 \
--assert-gpu-compositing --browser=exact \
--browser-executable=out/Default/chrome
```
### Speedometer2 Runs per minute

| Build | Runs per minute |
|--|--|
| Official with CFI | 391.575 ± 17.901 |
| Official sans CFI | 381.923 ± 11.436 |
| Official sans CFI with BOLT | 404.009 ± 13.378 |

### Uarch metrics
Running under `perf` to see the change in uarch metrics, narrowing down to just P-cores (Golden Cove):

```bash
taskset -c 0-15 perf stat -e instructions,cycles,L1-icache-misses,iTLB-misses -- vpython3 tools/perf/run_ben
chmark speedometer2 \
--assert-gpu-compositing --browser=exact \
--browser-executable=out/Default/chrome
```

| | Official sans CFI | Official sans CFI with BOLT | reduction with BOLT, % |
|--|--|--|--|
| seconds | 25.182281057 | 23.781656083 | 5.9% |
| instructions | 288,747,937,775 | 287,258,920,991 | 0.5% |
| cycles | 144,095,296,652 | 139,002,624,616 | 3.7% |
| L1-icache-misses | 4,703,384,066 | 3,893,492,873 | 20.8% |
| iTLB-misses | 42,881,805 | 32,524,602 | 31.8% |

## Summary
BOLT is effective in optimizing large code footprint applications, both server- and client-side. 
Chromium appears to be a good candidate as it exhibits elevated icache misses per 1000 instructions (MPKI) of about 16.
BOLT shows moderate speedups for Chromium of about 6% wall clock-wise, or 4% cycles-wise, driven by 21% icache miss reduction and 32% iTLB miss reduction.

## Future work
* Confirm if CPU frontend is a bottleneck for Chromium using top-down methodology.
* Support Clang CFI in BOLT.
* Improve profiling coverage, bringing the function coverage closer to PGO levels.
* Carefully measure the resulting performance, following benchmarking best practices and rigorous approach to statistics.