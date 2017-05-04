#!/usr/bin/env bash
export CUDAHOME=/usr/local/cuda
cd gem5
scons build/X86_MESI_Two_Level_GPU/gem5.opt --default=../gem5-gpu/build_opts/X86_MESI_Two_Level_GPU EXTRAS=../gem5-gpu/src:../gpgpu-sim/ -j8
cd ..
