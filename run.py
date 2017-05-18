#!/usr/bin/env python3

#
# A Python script to run all multi-core experiments for PARSEC 2.1 benchmarks.
#
# Copyright (C) Min Cai 2015
#

import os
import multiprocessing as mp

def run(bench, executable, args, l2_size, l2_assoc, l2_relacement_policy, num_threads, min_gpu_partition_size, max_gpu_partition_size):
    dir = 'results/' + bench + '/' + l2_size + '/' + str(l2_assoc) + 'way/' \
    + 'nvm_' + str(min_gpu_partition_size) + '-' + str(max_gpu_partition_size) + '/' + l2_relacement_policy + '/' + str(num_threads) + 'c/'

    os.system('rm -fr ' + dir)
    os.system('mkdir -p ' + dir)


    # + ' -c ' + '/home/zhangbowen/IdeaProjects/BJUT/gem5-gpu/tests/test-progs/gem5_gpu_backprop/bin/x86/linux/gem5_gpu_backprop -o 4096' \
    cmd_run = 'gem5/build/X86_MESI_Two_Level_GPU/gem5.opt -d ' + dir + ' gem5-gpu/configs/se_fusion.py' \
              + ' --clusters=4' + ' --total-mem-size=512MB' \
              + ' -c ' + executable + ' -o ' + args \
              + ' --cpu-type=timing --num-cpus=' + str(num_threads) \
              + ' --caches --l2cache --num-l2caches=1' \
              + ' --l1d_size=32kB --l1i_size=32kB --l2_size=' + l2_size + ' --l2_assoc=' + str(l2_assoc) \
              + ' --fast-forward=100000 --maxinsts=200000000' \
              + ' --min_gpu_partition_size=' + str(min_gpu_partition_size) + ' --max_gpu_partition_size=' + str(max_gpu_partition_size) \
              + ' --l2_replacement_policy=' + l2_relacement_policy
    print(cmd_run)
    os.system(cmd_run)


def run_experiment(a):
    bench, executable, args, l2_size, l2_assoc, l2_relacement_policy, num_threads, min_gpu_partition_size, max_gpu_partition_size = a
    run(bench, executable, args, l2_size, l2_assoc, l2_relacement_policy, num_threads, min_gpu_partition_size, max_gpu_partition_size)

experiments = []


def run_experiments():
    num_processes = mp.cpu_count()
    pool = mp.Pool(num_processes)
    pool.map(run_experiment, experiments)

    pool.close()
    pool.join()


def add_experiment(bench, executable, args, l2_size, l2_assoc, l2_relacement_policy, num_threads, min_gpu_partition_size, max_gpu_partition_size):
    a = bench, executable, args, l2_size, l2_assoc, l2_relacement_policy, num_threads, min_gpu_partition_size, max_gpu_partition_size
    experiments.append(a)


def add_experiments(bench, executable, args):
    for min_gpu_partition_size in [-1]:
        for max_gpu_partition_size in [-1]:
            add_experiment(bench, executable, args, '256kB', 8, 'LRU', 2, min_gpu_partition_size, max_gpu_partition_size)
            add_experiment(bench, executable, args, '256kB', 8, 'Bypass', 2, min_gpu_partition_size, max_gpu_partition_size)
    for min_gpu_partition_size in [1,3,5]:
        for max_gpu_partition_size in [3,5]:
            if max_gpu_partition_size > min_gpu_partition_size:
                add_experiment(bench, executable, args, '256kB', 8, 'SP_static', 2, min_gpu_partition_size, max_gpu_partition_size)
    for min_gpu_partition_size in [4]:
        for max_gpu_partition_size in [4]:
            add_experiment(bench, executable, args, '256kB', 8, 'SP_static', 2, min_gpu_partition_size, max_gpu_partition_size)
    #~ add_experiment(name, args, '512kB', 8, 4)
    #~ add_experiment(name, args, '1MB', 8, 4)
    #~ add_experiment(name, args, '2MB', 8, 4)
    #~ add_experiment(name, args, '4MB', 8, 4)
    #~ add_experiment(name, args, '8MB', 8, 4)

def add_bench(bench, executable, args):
    add_experiments(bench, executable, args)


#~ add_bench(' "16 2 2 benchmarks/rodinia/data/hotspot/temp_64 benchmarks/rodinia/data/hotspot/power_64 output.out"', 'benchmarks/rodinia/hotspot/gem5_fusion_hotspot')
#~ add_bench(' "-o -i benchmarks/rodinia/data/kmeans/kdd_cup"', 'benchmarks/rodinia/kmeans/gem5_fusion_kmeans')
#~ add_bench(' "benchmarks/rodinia/data/heartwall/test.avi 5"', 'benchmarks/rodinia/heartwall/gem5_fusion_heartwall')
# add_bench(' 4096', 'backprop/gem5_fusion_backprop')
#~ add_bench(bfs, 'benchmarks/rodinia/bfs/gem5_fusion_bfs', ' benchmarks/rodinia/data/bfs/graph1MW_6.txt', )
#~ add_bench(' "512 10"', 'benchmarks/rodinia/nw/gem5_fusion_needle')
#~ add_bench(' "1000 100 20 > result.txt"', 'benchmarks/rodinia/pathfinder/gem5_fusion_pathfinder')
#~ add_bench(' "2048 2048 0 127 0 127 0.5 2"', 'benchmarks/rodinia/srad/gem5_fusion_srad')
#~ add_bench(' "10 20 256 65536 65536 1000 none output.txt 1"', 'benchmarks/rodinia/strmcluster/gem5_fusion_strmcluster')
#~ add_bench(' "16 16 16 10000 16"', 'benchmarks/rodinia/cell/gem5_fusion_cell')

#~ add_bench('backprop1', 'gem5-gpu/tests/test-progs/gem5_gpu_backprop/bin/x86/linux/gem5_gpu_backprop', '4096')

add_bench('hotspot', '/home/zhangbowen/IdeaProjects/BJUT/benchmarks/rodinia/hotspot/gem5_fusion_hotspot', '"512 2 2 benchmarks/rodinia/data/hotspot/temp_1024 benchmarks/rodinia/data/hotspot/power_1024 output.out"')
add_bench('kmeans', '/home/zhangbowen/IdeaProjects/BJUT/benchmarks/rodinia/kmeans/gem5_fusion_kmeans', '"-i benchmarks/rodinia/data/kmeans/kdd_cup"')
add_bench('heartwall', '/home/zhangbowen/IdeaProjects/BJUT/benchmarks/rodinia/heartwall/gem5_fusion_heartwall', '"benchmarks/rodinia/data/heartwall/test.avi 5"')
add_bench('backprop', '/home/zhangbowen/IdeaProjects/BJUT/benchmarks/rodinia/backprop/gem5_fusion_backprop', '65536')
add_bench('bfs', '/home/zhangbowen/IdeaProjects/BJUT/benchmarks/rodinia/bfs/gem5_fusion_bfs', 'benchmarks/rodinia/data/bfs/graph1MW_6.txt')
#~ add_bench('nw', '/home/zhangbowen/IdeaProjects/BJUT/benchmarks/rodinia/nw/gem5_fusion_needle', '"2048 10"')
add_bench('pathfinder', '/home/zhangbowen/IdeaProjects/BJUT/benchmarks/rodinia/pathfinder/gem5_fusion_pathfinder', '"100000 100 20 > result.txt"')
add_bench('srad', '/home/zhangbowen/IdeaProjects/BJUT/benchmarks/rodinia/srad/gem5_fusion_srad', '"2048 2048 0 127 0 127 0.5 2"')
add_bench('strmcluster', '/home/zhangbowen/IdeaProjects/BJUT/benchmarks/rodinia/streamcluster/gem5_fusion_streamcluster', '"10 20 256 65536 65536 1000 none output.txt 1"')




run_experiments()
