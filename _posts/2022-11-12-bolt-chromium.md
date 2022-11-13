---
layout: post
title: "Optimizing Chromium with BOLT"
date: 2022-11-12
comments: true
---
## Intro
As you might already know, BOLT helps achieve peak performance on top of compiler's best effort, i.e. over both PGO and LTO.
This post will cover the necessary steps to experiment with optimizing Chromium with BOLT. 
I don't have any knowledge of Chromium so it's going to be quick and dirty.

## Plan
We'll tackle this problem in the following steps:
- produce pre-bolt chromium binary with preserved (static) relocations
- collect the profile
- optimize the binary
- try to get some performance data

## Building Chromium
I followed the steps here: [Checking out and building Chromium on Linux](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md).
Things just worked for me on this revision:
```
commit c2149180c4a2616202ad37580cb1cdf8372bbfa0 (HEAD, origin/main, origin/HEAD)
Author: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Date:   Fri Nov 11 06:42:23 2022 +0000

    Roll clank/internal/apps from 2dd286627b38 to 3abebe8793b9 (1 revision)
```

Chromium binary has a very large text section:
```
$ size -A out/Default/chrome
...
.text                 209883648    66822144
```
Meaning it's about 210MB in size!

## Pre-BOLT Chromium binary
In order to enable function reordering, one of <s>two</s>the most important optimizations, the input binary needs to have .text relocations 
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
I ended up not adding them at all and instead increasing the workload.

As a workload, I used the following steps that I believe are somewhat representative of a typical Chrome usage:
- Type "google" into Google's search bar.
- Click the first link leading to Google's search page.
- There, enter "facebook".
- Click on "Login" button, followed by "Forgot password".
- Close the tab in frustration. Type "web benchmark" in search bar.
- Click on "Speedometer 2.0" link.
- Let it run and close the browser.

For me, that produced an unreasonable ~500Mb perf.data file with very low coverage (on that later). But that'll suffice for now.

## Optimizing the binary
Again, we're following BOLT's manual: [Step 3: Optimize with BOLT](https://github.com/llvm/llvm-project/tree/main/bolt#step-3-optimize-with-bolt).
There are a couple of Chromium's quirks:
- The optimized binary needs to be at the same path as the original (i.e. in `out/Default/` folder)
- Chromium employs V8 as a JS VM. It still has the same issue with code pointers described in this post: [Optimizing NodeJS with BOLT](https://aaupov.github.io/blog/2020/10/08/bolt-nodejs).

Here's the command line that I used:
```
llvm-bolt out/Default/chrome -o out/Default/chrome.bolt \
  -data=perf.data -dyno-stats \
  -reorder-blocks=ext-tsp -reorder-functions=hfsort \
  -split-functions -split-all-cold -split-eh \
  -skip-funcs=Builtins_.\*
```

## Perf testing
As performance testing, I used Web benchmark (Speedometer 2.0) to see if the optimization was effective:
<TBD>