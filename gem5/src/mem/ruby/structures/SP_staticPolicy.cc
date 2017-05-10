/*
 * Copyright (c) 2013 Advanced Micro Devices, Inc
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * Author: Derek Hower
 */

#include "mem/ruby/structures/SP_staticPolicy.hh"


using namespace std;

SP_staticPolicy::SP_staticPolicy(const Params * p)
    : AbstractReplacementPolicy(p),
      minGpuPartitionSize(p->min_gpu_partition_size),
      maxGpuPartitionSize(p->max_gpu_partition_size)
{
    printf("min: %d, max: %d\n", minGpuPartitionSize, maxGpuPartitionSize);
}


SP_staticPolicy::~SP_staticPolicy()
{
}

SP_staticPolicy *
SP_staticReplacementPolicyParams::create()
{
    return new SP_staticPolicy(this);
}


void
SP_staticPolicy::touch(string name, int64_t set, int64_t index, Tick time)
{
    assert(index >= 0 && index < m_assoc);
    assert(set >= 0 && set < m_num_sets);
    
    is_gpu_request[set][index] = name.find("l1_cntrl_sp");
    m_last_ref_ptr[set][index] = time;
}

int64_t
SP_staticPolicy::getVictim(string name, int64_t set) const
{
    Tick time;

    Tick smallest_time_cpu;
    int64_t smallest_index_cpu = -1;
    smallest_time_cpu = -1;

    Tick smallest_time_gpu;
    int64_t smallest_index_gpu = -1;
    smallest_time_gpu = -1;
     
    int numGpuLines = 0;
    
    for (unsigned i = 0; i < m_assoc; i++) {
        time = m_last_ref_ptr[set][i];

        if (is_gpu_request[set][i] )
            numGpuLines++;
            
            if (time < smallest_time_gpu || smallest_time_gpu == -1) {
                smallest_index_gpu = i;
                smallest_time_gpu = time;
        }
    }

    if(numGpuLines > maxGpuPartitionSize && name.find("l1_cntrl_sp"))
        return smallest_index_gpu;
    }

    for (unsigned i = 0; i < m_assoc; i++) {
        time = m_last_ref_ptr[set][i];

        if (!is_gpu_request[set][i] && (time < smallest_time_cpu || smallest_time_cpu == -1)) {
            smallest_index_cpu = i;
            smallest_time_cpu = time;
        }
    }
    
    if(numGpuLines < minGpuPartitionSize && !name.find("l1_cntrl_sp")) {
        return smallest_index_cpu;
    
    }

    if(smallest_time_cpu >= smallest_time_gpu){
        return smallest_index_gpu;
    
    }
    
    else{
        return smallest_index_cpu;
     
    }
}
