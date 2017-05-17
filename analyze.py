#!/usr/bin/env python3
from gem5_utils import parse_result, to_csv, generate_plot

# Define benchmark names.
benchmarks = [
    'backprop',
    #~ 'kmeans',
    #~ 'heartwall',
    #~ 'hotspot',
    #~ 'bfs',
    #~ 'nw',
    #~ 'pathfinder',
    #~ 'srad',
    #~ 'strmcluster',
    #~ 'cell',
    #~ 'canneal',
    #~ 'dedup',
    # 'facesim',
    # 'ferret',
    # 'fluidanimate',
    # 'freqmine',
    # 'streamcluster',
    # 'swaptions',
    # 'vips',
    # 'x264'
]

num_threads = 2   #4

# Create CSVs and Figures illustrating the relationship between the L2 Cache Size and the L2 Miss Rate.
def parse_results_l2_sizes():
    results = []

    for benchmark in benchmarks:
        #~ for l2_size in ['256kB', '512kB', '1MB', '2MB', '4MB', '8MB']:
        #~ for l2_size in ['256kB', '512kB']:
        for l2_size in ['256kB']:
            for l2_replacement_policy in ['LRU', 'Bypass']:
                 for min_gpu_partition_size in [-1]:
                    for max_gpu_partition_size in [-1]:
                        results.append(
                            parse_result('results/' +
                                        benchmark + '/' + l2_size + '/8way/' + 'nvm_' + str(min_gpu_partition_size) + '-' + str(max_gpu_partition_size) + '/' + l2_replacement_policy + '/2c/',
                                        benchmark=benchmark,
                                        l2_size=l2_size,
                                        max_gpu_partition_size=max_gpu_partition_size,
                                        min_gpu_partition_size=min_gpu_partition_size,
                                        l2_replacement_policy=l2_replacement_policy)
                        )
        #~ for l2_size in ['256kB']:
            #~ for l2_replacement_policy in ['SP_static']:
                 #~ for min_gpu_partition_size in [1,3,5,7]:
                    #~ for max_gpu_partition_size in [1,3,5,7]:
                        #~ if max_gpu_partition_size > min_gpu_partition_size:
                            #~ results.append(
                                #~ parse_result('results/' +
                                            #~ benchmark + '/' + l2_size + '/8way/' + 'nvm_' + str(min_gpu_partition_size) + '-' + str(max_gpu_partition_size) + '/' + l2_replacement_policy + '/2c/',
                                            #~ benchmark=benchmark,
                                            #~ l2_size=l2_size,
                                            #~ max_gpu_partition_size=max_gpu_partition_size,
                                            #~ min_gpu_partition_size=min_gpu_partition_size,
                                            #~ l2_replacement_policy=l2_replacement_policy)
                        #~ )
    
    def num_cycles(r):
        return int(r.stats[0]['system.{}.numCycles'.format('switch_cpus' if num_threads == 1 else 'switch_cpus0')])
        
    def committed_insts(r):
        if num_threads == 1:
            result = int(r.stats[0]['system.switch_cpus.committedInsts'])
        else:
            result = 0

            for i in range(0, num_threads):
                result += int(r.stats[0]['system.switch_cpus{}.committedInsts'.format(i)])

        return result
    
    def baseline_num_cycles(results, r1):
        for r in results:
            if r1.props['benchmark'] == r.props['benchmark'] and r.props['l2_replacement_policy'] == 'LRU':
                    return num_cycles(r)

        print("Cannot find baseline num_cycles from specified results")
        sys.exit(-1)    
        
    def speedup(results, r):
        return float(baseline_num_cycles(results, r)/num_cycles(r))
            
    def l2_hit_rate(stats):
        hits = stats[0]['system.ruby.l2_cntrl0.L2cache.demand_hits']
        accesses = stats[0]['system.ruby.l2_cntrl0.L2cache.demand_accesses']
        return str(float(hits) / float(accesses))
            
    to_csv('results/l2_sizes.csv', results, [
        ('Benchmark', lambda r: r.props['benchmark']),
        ('ReplacementPolicy', lambda r: r.props['l2_replacement_policy']),
        ('Min:Max GPU Partition Size', lambda r: str(int(r.props['min_gpu_partition_size'])) + ':' + str(int(r.props['max_gpu_partition_size']))),        
        ('L2 Size', lambda r: r.props['l2_size']),
        ('L2 Accesses', lambda r: r.stats[0]['system.ruby.l2_cntrl0.L2cache.demand_accesses']),
        ('L2 Replacements', lambda r: r.stats[0]['system.ruby.L2Cache_Controller.L2_Replacement']),
        ('Speedup', lambda r: speedup(results, r)),
        ('Committed Insts', committed_insts),
        ('Simulation Time', lambda r: r.stats[0]['host_seconds']),
        ('L2 Hit Rate', lambda r: l2_hit_rate(r.stats)),
        ('# Cycles', num_cycles)
    ])

    generate_plot('results/l2_sizes.csv',
                  'results/l2_sizes_vs_l2_hit_rate.pdf', 'Benchmark', 'L2 Hit Rate',
                  'L2 Size', 'L2 Hit Rate')
    generate_plot('results/l2_sizes.csv',
                  'results/l2_sizes_vs_num_cycles.pdf', 'Benchmark', '# Cycles',
                  'L2 Size', '# Cycles')

    return results


# Create CSVs and Figures illustrating the relationship between the L2 Cache Size and the L2 Miss Rate.
results_l2_sizes = parse_results_l2_sizes()
