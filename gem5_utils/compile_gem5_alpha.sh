#!/usr/bin/env bash
export CUDAHOME=/usr/local/cuda
cd ../gem5
scons build/X86_VI_hammer_GPU/gem5.opt --default=X86 EXTRAS=/home/zhangbowen/gem5-gpu/gem5-gpu/src:/home/zhangbowen/gem5-gpu/gpgpu-sim/ PROTOCOL=VI_hammer GPGPU_SIM=True -j8
cd ../gem5_utils_gpu
