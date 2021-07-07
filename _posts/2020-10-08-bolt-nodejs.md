---
layout: post
title: "Optimizing NodeJS with BOLT"
date: 2020-10-08
comments: true
---
## Background
This section aims to cover the reason why straightforward
application of BOLT for NodeJS can fail.

NodeJS binary contains precompiled native code for V8 built-in functions,
in a structure called "embedded blob". More on this topic is available
in [v8 blog/embedded-builtins](https://v8.dev/blog/embedded-builtins).

BOLT performs function reordering, thus it 
- updates all references to functions, and
- generally prohibits the code which makes assumptions about
code layout.

Unfortunately, v8 embedded builtins present both issues:
1. In `InstructionStream::TryLookupCode` there's a `PcIsOffHeap` check 
which tests if the address falls into `embedded_blob` range. The check
fails for moved builtins as they no longer live in the original range.

2. In debug mode, `Isolate::SetEmbeddedBlob` checks if "the contents of
the embedded blob are unchanged from serialization-time, just to ensure
the compiler isn't messing with us". BOLT changes the layout of 
functions in embedded blob, so the check fails.

In order to work around those issues, we need to instruct BOLT to keep
builtin functions intact. Luckily, there's an option exactly for that:
`-skip-funcs`, which accepts function name regex. All V8 builtins start
with `Builtins_` prefix (as of Oct'20), so the final option is:

```
-skip-funcs=Builtins_.*
```

## Setup
# Host system
Acer C720 with Intel Haswell 2955U, Ubuntu 18.04.

# BOLT
BOLT is checked out from and built locally using the instructions from the
official repository [facebookincubator/BOLT](https://github.com/facebookincubator/BOLT#manual-build).

Commit:
```
2926855	Oct 5 2020 Add -check-overlapping-elements option
```

# NodeJS
NodeJS is checked out from and built locally using the instructions from the official repository [nodejs/node](https://github.com/nodejs/node/blob/master/BUILDING.md#unix-prerequisites).

Commit:
```
ad012c9bbc Oct 6 2020 doc: fix YAML syntax errors
```

NodeJS configure command:
```bash
CFLAGS=-Wl,--emit-relocs\ -Wl,-znow \
LDFLAGS=-Wl,--emit-relocs\ -Wl,-znow \
./configure --ninja
```

`--emit-relocs` and `-znow` linker flags are needed by BOLT:
- `--emit-relocs` is mandatory for function reordering,
- `-znow` is optional for `-plt=...` optimization.

UPD: depending on Ubuntu version, `-no-pie -fno-PIE` CFLAGS/CXXFLAGS might be needed to avoid `PIC jump table heuristic failure` assertion in perf2bolt. 
(Thanks @gabrielshulhof!)

## Profile collection
Profile was collected using system-wide perf sampling for 3 minutes.
Node's `make js-test` was selected as a profiling workload.

`make js-test` and `perf` were launched manually at the same time.

# Perf
```
$ perf record -e cycles:u -j any,u -a -o perf.data -- sleep 180
[ perf record: Woken up 1663 times to write data ]
[ perf record: Captured and wrote 415.811 MB perf.data (979261 samples) ]
```
# perf2bolt
Sampled profile was converted into BOLT format using perf2bolt
```
$ ./perf2bolt -p perf.data -o perf.fdata node/node -skip-funcs=Builtins_.*
PERF2BOLT: Starting data aggregation job for perf.data
PERF2BOLT: spawning perf job to read branch events
PERF2BOLT: spawning perf job to read mem events
PERF2BOLT: spawning perf job to read process events
PERF2BOLT: spawning perf job to read task events
BOLT-INFO: Target architecture: x86_64
BOLT-INFO: BOLT version: f137ed238db11440f03083b1c88b7ffc0f4af65e
BOLT-INFO: first alloc address is 0x400000
BOLT-INFO: creating new program header table at address 0x2600000, offset 0x2200000
BOLT-INFO: enabling relocation mode
...
PERF2BOLT: input binary is associated with 1948 PID(s)
PERF2BOLT: waiting for perf events collection to finish...
PERF2BOLT: parse branch events...
PERF2BOLT: read 931286 samples and 14861654 LBR entries
PERF2BOLT: 47975 samples (4.9%) were ignored
PERF2BOLT: traces mismatching disassembled function contents: 2 (0.0%)
PERF2BOLT: out of range traces involving unknown regions: 1335244 (9.6%)
...
PERF2BOLT: wrote 144584 objects and 0 memory objects to perf.fdata
```
## BOLT invocation
Finally, we invoke BOLT with the processed perf.fdata:
```
$ ./llvm-bolt node/node -o node.bolt_opt -data=perf.fdata -reorder-blocks=cache+ -reorder-functions=hfsort -split-functions=2 -split-all-co
ld -split-eh -dyno-stats -skip-funcs=Builtins_.*
BOLT-INFO: Target architecture: x86_64
BOLT-INFO: BOLT version: f137ed238db11440f03083b1c88b7ffc0f4af65e
BOLT-INFO: first alloc address is 0x400000
BOLT-INFO: creating new program header table at address 0x2600000, offset 0x2200000
BOLT-WARNING: debug info will be stripped from the binary. Use -update-debug-sections to keep it.
BOLT-INFO: enabling relocation mode
...
BOLT-INFO: 9991 out of 44114 functions in the binary (22.6%) have non-empty execution profile
BOLT-INFO: 537 functions with profile could not be optimized
BOLT-INFO: profile for 1 objects was ignored
BOLT-INFO: the input contains 4372 (dynamic count : 84835) opportunities for macro-fusion optimization. Will fix instances on a hot path.
BOLT-INFO: removed 235 'repz' prefixes with estimated execution count of 19606 times.
BOLT-INFO: basic block reordering modified layout of 6166 (13.83%) functions
BOLT-INFO: UCE removed 3 blocks and 11 bytes of code.
BOLT-INFO: splitting separates 1993580 hot bytes from 3203330 cold bytes (38.36% of split functions is hot).
BOLT-INFO: program-wide dynostats after all optimizations before SCTC and FOP:

             9514525 : executed forward branches
             3820211 : taken forward branches
             4641003 : executed backward branches
             3131589 : taken backward branches
             1381871 : executed unconditional branches
             2252361 : all function calls
              334497 : indirect calls
              166548 : PLT calls
           177500193 : executed instructions
            40140973 : executed load instructions
            18982774 : executed store instructions
              304380 : taken jump table branches
                   0 : taken unknown indirect branches
            15537399 : total branches
             8333671 : taken branches
             7203728 : non-taken conditional branches
             6951800 : taken conditional branches
            14155528 : all conditional branches

             8586977 : executed forward branches (-9.7%)
              673061 : taken forward branches (-82.4%)
             5568551 : executed backward branches (+20.0%)
             2881907 : taken backward branches (-8.0%)
              667119 : executed unconditional branches (-51.7%)
             2252361 : all function calls (=)
              334497 : indirect calls (=)
              166548 : PLT calls (=)
           176181879 : executed instructions (-0.7%)
            40140973 : executed load instructions (=)
            18982774 : executed store instructions (=)
              304380 : taken jump table branches (=)
                   0 : taken unknown indirect branches (=)
            14822647 : total branches (-4.6%)
             4222087 : taken branches (-49.3%)
            10600560 : non-taken conditional branches (+47.2%)
             3554968 : taken conditional branches (-48.9%)
            14155528 : all conditional branches (=)

BOLT-INFO: SCTC: patched 53 tail calls (53 forward) tail calls (0 backward) from a total of 53 while removing 2 double jumps and removing 54 basic blocks totalling 270 bytes of code. CTCs total execution count is 14337 and the number of times CTCs are taken is 6625.
...
BOLT-INFO: patched build-id (flipped last bit)
```

Let's see what's the resulting text section size looks like 
before and after BOLT (using `size` to get section sizes):

| Section | Original | BOLTed |
|---------|---------:|-------:|
| `.text` | 15.74Mb  | 2.28Mb |
| `.text.cold` | N/A | 12.24Mb|

Looks good. Now on to testing.

## Testing
We want to quickly test if the optimized binary is functionally correct
and see if there are noticeable performance changes (without bothering
too much about proper benchmarking setup).
We kill two birds with one stone by running `make jstest` again.
We've used it for profiling, but only at ~1/3 of its duration, so 
it's borderline fair. Sorry, no proper train/test split this time!

# Original binary
```
~/node$ time NODE_OPTIONS="--use-largepages=on" make -s jstest
...
[08:28|% 100|+ 3178|-   0]: Done

real    8m32.790s
user    9m5.653s
sys     1m16.797s
```

# Optimized binary
To run testing with the optimized binary, we do the simplest hack
possible: replace the original binary in `node/out/Release` with the
new one.

```
~/node$ time NODE_OPTIONS="--use-largepages=on" make -s jstest
...
[07:49|% 100|+ 3178|-   0]: Done

real    7m53.215s
user    8m19.538s
sys     1m13.263s
```

Great! Optimized binary doesn't fail js tests, and also runs about 8%
faster. It's possible to confirm the difference using uarch events
provided by perf, but we'll keep it for another post.
