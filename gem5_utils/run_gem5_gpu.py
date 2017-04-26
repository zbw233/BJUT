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

def initbench(arg, name):
    bench=benchmarks(arg, name)
    add_experiments(bench)


#~ initbench(' -o "512 2 2 ../../data/hotspot/temp_512 ../../data/hotspot/power_512 output.out"', 'hotspot/gem5_fusion_hotspot')
#~ initbench(' -o "-o -i ../../data/kmeans/kdd_cup" ', 'kmeans/gem5_fusion_kmeans')
#~ initbench(' ', 'heartwall/gem5_fusion_heartwall')
#~ initbench(' -o 512', 'backprop/gem5_fusion_backprop')
#~ initbench(' -o 512', 'bfs/gem5_fusion_bfs')
initbench(' -o "2048 10"', 'nw/gem5_fusion_needle')
#~ initbench(' ', 'pathfinder/gem5_fusion_pathfinder')
#~ initbench(' ', 'srad/gem5_fusion_srad')
#~ initbench(' ', 'strmcluster/gem5_fusion_strmcluster')

   

run_experiments()
