#!/usr/bin/env python
import os

import time

from runSuperFine import parse_options
from superfine.SuperFine import SuperFine


SOURCE_SUFFIX = "model_source_trees"
QUARTETS_SUFFIX = "wqrt"


def convert_quartets_to_source_trees(quartets_path):
    print("Converting Quartets: " + quartets_path)
    with open(quartets_path, 'r') as fh:
        quartets = fh.read()
    quartet_list = quartets.split(" ")
    source_trees = ""

    for quartet in quartet_list:
        if "|" in quartet:
            left_pair, right_weight_pair = quartet.split("|")
            right_pair, weight = right_weight_pair.split(":")
            source_trees += "(({}),({}));\n".format(right_pair, left_pair)
    return source_trees


def execute_SF(simulated_tree_path, simulated_tree_path_prefix, reconciler='qmc', result_tree_suffix='SFwQMC'):
    start_time = time.time()
    print("start processing " + simulated_tree_path)
    (input, options) = parse_options(input=simulated_tree_path, reconciler=reconciler)
    # try:
    tree = SuperFine(input, options)
    # except:
    #     print("######### Error for " + simulated_tree_path)
    #     return
    running_time = time.time() - start_time
    result_tree_path = '{}+{}.{}'.format(simulated_tree_path_prefix, running_time, result_tree_suffix)
    print("save to " + result_tree_path)
    with open(result_tree_path, 'w') as fh:
        fh.write(str(tree) + ';')


def main():
    # simulated_folder_path = 'datasets/simulated'
    simulated_folder_path = '/home/zahi/Desktop/tree_simulation/tree_simulation_python/tree_simulation/data/simulated'
    for taxa in os.listdir(simulated_folder_path):
        taxa_folder_path = simulated_folder_path + "/" + taxa
        for scaffold in os.listdir(taxa_folder_path):
            scaffold_path = taxa_folder_path + "/" + scaffold
            for simulated_tree in os.listdir(scaffold_path):
                if simulated_tree.endswith(SOURCE_SUFFIX) or simulated_tree.endswith(QUARTETS_SUFFIX):
                    simulated_tree_path = scaffold_path + "/" + simulated_tree
                    if simulated_tree.endswith(QUARTETS_SUFFIX):
                        quartets_tree_path = simulated_tree_path
                        simulated_tree_path = simulated_tree_path.replace(QUARTETS_SUFFIX, SOURCE_SUFFIX)
                        if os.path.isfile(simulated_tree_path):
                            continue
                        model_source_trees = convert_quartets_to_source_trees(quartets_tree_path)
                        with open(simulated_tree_path, 'w') as fh:
                            fh.write(model_source_trees)
                    simulated_tree_path_prefix = simulated_tree_path[:simulated_tree_path.rindex(".")]
                    execute_SF(simulated_tree_path, simulated_tree_path_prefix, reconciler='qmc', result_tree_suffix='SFwQMC')
                    execute_SF(simulated_tree_path, simulated_tree_path_prefix, reconciler='rmrp', result_tree_suffix='SFpaup')

# MAIN
if __name__ == '__main__':
    main()
