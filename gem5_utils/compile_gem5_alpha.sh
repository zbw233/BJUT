#!/usr/bin/env bash
export CUDAHOME=/usr/local/cuda
cd ../gem5
scons build/X86_MESI_Two_Level_GPU/gem5.opt --default=/home/zhangbowen/gem5-gpu/gem5-gpu/build_opts/X86_MESI_Two_Level_GPU_fix EXTRAS=/home/zhangbowen/gem5-gpu/gem5-gpu/src:/home/zhangbowen/gem5-gpu/gpgpu-sim/ -j8
scons build/X86_MESI_Two_Level_GPU/gem5.debug --default=/home/zhangbowen/gem5-gpu/gem5-gpu/build_opts/X86_MESI_Two_Level_GPU_fix EXTRAS=/home/zhangbowen/gem5-gpu/gem5-gpu/src:/home/zhangbowen/gem5-gpu/gpgpu-sim/ -j8
cd ../gem5_utils
