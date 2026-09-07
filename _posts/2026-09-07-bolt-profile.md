---
layout: post
title: "All About BOLT Profile"
date: 2026-09-07
comments: true
toc: true
---
# Intro
BOLT (Binary Optimization and Layout Tool) is a post-link **profile-guided** code layout optimizer.

This post will attempt to cover several dimensions of BOLT profiling: 
* profiling workload selection,
* profiling support in software and hardware,
* profile types and formats,
* profile lifecycle and handling in BOLT tools,
* real-world usage scenarios.

The profile plays a crucial role in its effectiveness. BOLT's raison d'être is that it matches binary profile to the binary directly, thus augmenting 
addressing the semantical gap of compiler-based PGO. 
Compiler works with a program representation

In compiler PGO, the profile has to describe program execution at program representation level that compiler manipulates
a higher level (source or IR), which causes reduced profile accuracy thus making the profile inaccurate when it reaches the low level representation. Late (CS IR) and flow/context-sensitive profiles reduce the gap but don't close it.

BOLT is a form of PGO (profile-guided optimizations) which 
has the advantage of identity profile mapping: the profile is collected from and mapped to the same semantical level

that works directly on executables which improves execution efficiency through profile-guided code layout optimizations.
and which implements profile-guided code layout optimizations
, a form of profile-guided optimizations (PGO). 
leveraging post-link optimizations that imp
is a binary optimization and layout tool, which is a form of profile-guided optimization (PGO)

This post attempts to cover the profile lifecycle, explain its handling in BOLT, and answer various practical questions.

In the end, I include ideas improving BOLT's ease of use through  profile collection domain and how it can be extended to make better use of existing and extra profiles.

This document is not assisted by AI, so all mistakes, typos and inaccuracies are my own.

# Getting the profile
This paragraph is about _what_ should be profiled and _how_.
## Workload selection
## Sampling
### IP
### Branch stack
## Tracing
### HW (ETM/PT)
### SW
## Instrumentation

## Workload selection
The very first question that needs to be answered when using BOLT is _what_ needs to be profiled.
The profile

### Do's and dont's
> Do profile your actual workload


works best results when optimization 
works best when the profile comes from the same workload that is going to be 

This recommendation extends to 
> (or benchmarks) – no train/test split.

> Don't profile tests.

Tests by design exercise corner cases – code paths that are not exercised often. Including them in the profile bloats hot code and 

### Server profiling
GWP, Strobelight, Perforator

### Client profiling

#### Compilers and interpreters
Clang: hello world, clang-bolt. Flang. MLIR?

CPython: pyperformance.

Rust: llvm, cargo-pgo

#### Android

#### Gentoo

## Hardware profiling
### Sampling events
* Events (cycles, taken branches, calls/rets)
* PEBS, skid
* Coverage vs accuracy

### Branch stacks
* No stacks: basic IP sampling
* 1-deep: SPE
* Fixed depth: LBR/BRBE, which branches
* Synthesized depth: PT/ETM and conversion (itrace)
* Extra information: branch type, mispredictions, latency

### Augmenting
* Imputting
* Infer-fall-throughs

### Extra profiles
* Memory

### Sanitizing hardware profiles
* Sample profile quality, mismatching traces
* SKL LBR erratum: duplicate LBR TOS, BAT mode
* ETM pid misattribution, heatmap

## Software-based profiling
### Instrumentation
* Options
* Sections and in-memory metadata

### Tracing

## External profiles

# Profile conversion and profile types
## Perf2bolt
Parallel processing and memory

## Profile types

### Unsymbolized
* Perf data
* Perfscript
* Pre-aggregated

### Symbolized
* fdata
* YAML
* symbols

## Input

### Perf data
* Simpleperf
* Memory profile

### Perf script

### Pre-aggregated
* eBPF
* Aggregation in SQL
* Multi-DSO

### AutoFDO/CSSPGO profiles

### Function order and selective instrumentation

## Output

### Unsymbolized
* Perfscript
* Pre-aggregated

### Symbolized
* fdata: legacy + memory profile
* YAML: rich + stale matching
* merge-data

# Profile reading and attaching

## Steps
* Parsing: lite mode and mayHaveProfile
* PreCFG: indirect control flow
* CFG

## Reading
* Traces
* DataAggregator/DataReader classes

## Attaching
* External fall-throughs, traces/returns
* Fix-block-counts
* Basic samples/MCF

## Profile staleness

# Assessing profile, its quantity and quality
## Inspecting
### heatmap
* unsymbolized
* PGO and BOLT evaluation
* perf2bolt mode
* Working set size

### print-cfg
* edge filtering

### dump-cg

## Quantitative evaluation
* Profile density
* Density thresholds and function coverage heuristics

## Profile quality vs flow graphs
* Continuity
* Flow conservation
* Basic samples
* MCF, edge overlap, TSP score

# Real world concerns
## Stale profile matching
* YAML metadata explained
* Knobs
* Pseudo probe matching
* Cross-ISA matching
* Inference

## Comparing and representativeness
* boltdiff

### Profile representativeness

For PGO systems, the following flowchart shows the relationship between "optimization" (input) and "production" (actual) profiles.

```
     -> Input/Optimization Profile
                    |
                    v
Input Program -> PGO/BOLT -> Optimized Program
                                      |
                                      v
                           Actual/Production Profile
```

To be practical, BOLT and AutoFDO/CSSPGO are designed to work with profiles captured from production usage, thus the general flow looks like the following:

```
source: ... --- old --- new
                 \       \
                  v       v
binary:       previous    current
                   \     ^   
                    v   /     
profile:          production     
```

AutoFDO/CSSPGO can consume production profile collected directly from the previous binary build, thanks to source/IR matching making it easier to tolerate source drift and profile staleness.

In case of BOLT, in theory it's possible to use the profile collected from the previous binary build but interaction with refreshed PGO makes it impractical, so that a flow with separate no-BOLT binary yields better resulting performance:

```
source: ... --- old --- new
                 \       \
                  v       v
binary:       previous    current
                   \     ^
                    v   /
profile:          production     
```

For compiler PGO, as the profile is matched to source/IR level, later stage optimizations do not inhibit its ability to consume the profile from drastically different binary.
However, compiler PGO is better at tolerating source drift and profile staleness compared to 
because of slower pace of change compared to waterfall changes in the binary
an important distinction between BOLT and compiler PGO is the ability to tolerate staleness.
AutoFDO/CSSPGO are designed to work directly with production profile collected from the previous workload build, tolerating source drift and profile staleness:


Unlike AutoFDO/CSSPGO that are designed to work with the profile collected from an actual ("production") workload execution, BOLT profile typically comes from separate build (no-bolt or pre-bolt) running with a subset of inputs/traffic ("dedicated profiling tier"). This creates a split between the profile that's used for optimization (opt profile) and actual (production) usage.

* Opt/prod profiles: in case of BOLT, the profile typically comes from separate binary build (no-BOLT/pre-BOLT) running on a subset of inputs/traffic, ideally 
* Optimization profile: the profile that's used to optimize the binary.
* Production profile: profile collected from the workload execution on real inputs.
* Partition score

## Continuous profile
* YAML BAT
* Continuous profile as secondary

## Interaction with PGO
* Zero-gap profiling
* BOLT-compatible AutoFDO
* Continuous BOLT and profiling optimized binaries
* CSSPGO/pseudo probes

# Profiling evolution

## Instrumentation
* YAML
* Unsymbolized

## Continuous BOLT
* Via driver
* In compiler/linker

## Dynamic BOLT
* OCOLOS
* Reoptimization

## Multi-BOLT
* Cross-DSO inlining

## Context-sensitive BOLT
* Inlining
* Data-flow optimizations

## Runtime BOLT
* TSX
