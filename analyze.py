#!/usr/bin/env python3
from gem5_utils import parse_result, to_csv, generate_plot

# Define benchmark names.
benchmarks = [
    #~ 'cell/gem5_fusion_cell',
    'backprop/gem5_fusion_backprop',
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


# Create CSVs and Figures illustrating the relationship between the L2 Cache Size and the L2 Miss Rate.
def parse_results_l2_sizes():
    results = []

    for benchmark in benchmarks:
        #~ for l2_size in ['256kB', '512kB', '1MB', '2MB', '4MB', '8MB']:
        #~ for l2_size in ['256kB', '512kB']:
        for l2_size in ['256kB']:
            results.append(
                parse_result('results/' +
                             benchmark + '/' + l2_size + '/8way/2c/',
                             benchmark=benchmark,
                             l2_size=l2_size)
            )
            
    def l2_hit_rate(stats):
        hits = stats[0]['system.ruby.l2_cntrl0.L2cache.demand_hits']
        accesses = stats[0]['system.ruby.l2_cntrl0.L2cache.demand_accesses']
        return str(float(hits) / float(accesses))
        
    to_csv('results/l2_sizes.csv', results, [
        ('Benchmark', lambda r: r.props['benchmark']),
        ('L2 Size', lambda r: r.props['l2_size']),
        ('L2 Accesses', lambda r: r.stats[0]['system.ruby.l2_cntrl0.L2cache.demand_accesses']),
        ('L2 Hit Rate', lambda r: l2_hit_rate(r.stats)),
        ('# Cycles', lambda r: r.stats[0]['system.cpu0.numCycles'])
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
