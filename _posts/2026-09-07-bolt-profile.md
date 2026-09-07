---
layout: post
title: "All About BOLT Profile"
date: 2026-09-07
comments: true
toc: true
---
# Intro
P in PGO
Lifecycle

# Getting the profile
## Workload selection
## Sampling
### IP
### Branch (SPE)
### Branch stack
## Tracing
### HW (ETM/PT)
### SW
## Instrumentation
## Compatible profile (“knowing it”)

## Workload selection
### Do's and dont's
Do profile workload (or benchmarks) – no train/test split.

Don't profile tests.

### Server profiling
GWP, Strobelight, Perforator

### Client profiling

#### Compilers and interpreters
Clang: hello world, clang-bolt. Flang. MLIR?

CPython: pyperformance.

Rust: llvm, cargo-pgo

#### Android

#### Gentoo

## Hardware
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

## Instrumentation
* Options
* Sections and in-memory metadata

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
