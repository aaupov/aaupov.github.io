---
layout: post
title: "Generalizing Clang-BOLT automation"
date: 2023-11-08
comments: true
toc: true
---
## Intro and problem statement
[Clang-BOLT](https://llvm.org/docs/AdvancedBuilds.html#bolt) 
is a set of CMake rules that automatically profile and apply BOLT optimizations to Clang binary.
This is similar to [PGO instrumentation](https://llvm.org/docs/AdvancedBuilds.html#multi-stage-pgo) with the primary difference being
that PGO instrumentation and optimizations are applied to the source, which allows optimizing other LLVM binaries beyond just Clang.
In contrast, BOLT is a binary optimization tool, so it's natural that it optimizes only one binary at a time.
Existing Clang-BOLT automation is developed as part of Clang build system, leaving out other projects.

**The goal is to address this shortcoming and extend BOLT optimization to other LLVM binaries using Clang-BOLT rules.**

It's primarily aimed at lld which incorporates the entire LLVM backend for LTO mode.
Optimized lld binary will benefit projects using LTO builds where the code generation happens during link time and is invoked
from lld binary.

## Solution
1. `CLANG_BOLT` automation needs to be extracted from `clang/CMakeLists.txt` into separate CMake files/functions
   under `llvm/cmake`.
2. The automation needs to be generalized to accept CMake target, and instantiated for Clang in place of
   existing `CLANG_BOLT` stuff.
3. Profiling: currently, Clang serves as a driver for PGO profiling, and PGO profiling lives in `clang/utils/perf-training` folder.
   There are several ways how profiling can be extended to arbitrary targets:
   - As a starting point, the profile collected from Clang binary can be applied to other binaries in hope that at least
   some functions will match. 
   - As a natural evolution, perf-training Lit tests can be added that run the target binary.
   - Alternatively, perf-training needs to be specialized for each subproject (i.e. added for lld).
  
## Call to action
It has been demonstrated that PGO and BOLT can yield sizable performance wins for Clang even with very small amount of training data:
check my 2022 LLVM Developer Meeting [presentation](https://llvm.org/devmtg/2022-11/#:~:text=Optimizing%20Clang%20with%20BOLT%20using%20CMake).

So the automatic optimization infrastructure has very high ROI: it can help save both developer time and CI server capacity.

If you benefit from faster Clang compile times with it and want to improve it and contribute back, 
this is a good project to do just that! Feel free to reach out to me with any questions.
