#!/usr/bin/env python3

#
# A Python script to run all multi-core experiments for PARSEC 2.1 benchmarks.
#
# Copyright (C) Min Cai 2015
#

import os
import multiprocessing as mp

class benchmarks:
    arg=''
    name=''
   
    def __init__(self, arg, name):
        self.name=name
        self.arg=arg

def run(bench, l2_size, l2_assoc, num_threads):
    dir = 'results/' + bench.name + '/' + l2_size + '/' + str(l2_assoc) + 'way/' + str(num_threads) + 'c/'

    os.system('rm -fr ' + dir)
    os.system('mkdir -p ' + dir)

   
    cmd_run = '../gem5/build/X86_MESI_Two_Level_GPU/gem5.opt -d ' + dir + ' ../gem5-gpu/configs/se_fusion.py' \
              + ' --clusters=4' \
              + ' -c ' + '/home/zhangbowen/gem5-gpu/benchmarks/rodinia/' + bench.name + bench.arg \
              + ' --cpu-type=timing --num-cpus=' + str(num_threads) \
              + ' --caches --l2cache --num-l2caches=1' \
              + ' --l1d_size=32kB --l1i_size=32kB --l2_size=' + l2_size + ' --l2_assoc=' + str(l2_assoc)
    print(cmd_run)
    os.system(cmd_run)


def run_experiment(args):
    bench, l2_size, l2_assoc, num_threads = args
    run(bench, l2_size, l2_assoc, num_threads)

experiments = []


def run_experiments():
    num_processes = mp.cpu_count()
    pool = mp.Pool(num_processes)
    pool.map(run_experiment, experiments)

    pool.close()
    pool.join()


def add_experiment(bench, l2_size, l2_assoc, num_threads):
    args = bench, l2_size, l2_assoc, num_threads
    experiments.append(args)


def add_experiments(bench):
    add_experiment(bench, '256kB', 8, 2)
    #~ add_experiment(bench, '512kB', 8, 4)
    #~ add_experiment(bench, '1MB', 8, 4)
    #~ add_experiment(bench, '2MB', 8, 4)
    #~ add_experiment(bench, '4MB', 8, 4)
    #~ add_experiment(bench, '8MB', 8, 4)

def add_bench(arg, name):
    bench=benchmarks(arg, name)
    add_experiments(bench)


#~ add_bench(' -o "16 2 2 /home/zhangbowen/gem5-gpu/benchmarks/rodinia/data/hotspot/temp_64 /home/zhangbowen/gem5-gpu/benchmarks/rodinia/data/hotspot/power_64 output.out"', 'hotspot/gem5_fusion_hotspot')
#~ add_bench(' -o "-o -i /home/zhangbowen/gem5-gpu/benchmarks/rodinia/data/kmeans/kdd_cup"', 'kmeans/gem5_fusion_kmeans')
#~ add_bench(' -o "/home/zhangbowen/gem5-gpu/benchmarks/rodinia/data/heartwall/test.avi 5"', 'heartwall/gem5_fusion_heartwall')
add_bench(' -o 4096', 'backprop/gem5_fusion_backprop')
#~ add_bench(' -o /home/zhangbowen/gem5-gpu/benchmarks/rodinia/data/bfs/graph1MW_6.txt', 'bfs/gem5_fusion_bfs')
#~ add_bench(' -o "512 10"', 'nw/gem5_fusion_needle')
#~ add_bench(' -o "1000 100 20 > result.txt"', 'pathfinder/gem5_fusion_pathfinder')
#~ add_bench(' -o "2048 2048 0 127 0 127 0.5 2"', 'srad/gem5_fusion_srad')
#~ add_bench(' -o "10 20 256 65536 65536 1000 none output.txt 1"', 'strmcluster/gem5_fusion_strmcluster')
#~ add_bench(' -o "16 16 16 10000 16"', 'cell/gem5_fusion_cell')


   

run_experiments()
