#!/usr/bin/env bash
export CUDAHOME=/usr/local/cuda
cd gem5
scons build/X86_MESI_Two_Level_GPU/gem5.opt EXTRAS=../gpgpu-sim/ -j8
cd ..
