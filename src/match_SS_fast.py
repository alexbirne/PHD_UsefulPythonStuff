#!/usr/bin/env python

"""Script to select a subset of trees out of a multiple tree rootfile and save this subset in another root file."""

import sys, os, ROOT
from array import array

# vars_source = ["obsEtaSSProton", "obsTagSSProton"]
vars_source = ["lab0_SS_Proton_PROB", "lab0_SS_Proton_DEC"]
vars_target = ["lab0_SS_Proton_PROB", "lab0_SS_Proton_DEC"]

# unique_vars_source = [("run", ROOT.TLeaf.GetValueLong64),
#                       ("event", ROOT.TLeaf.GetValueLong64)]
unique_vars_source = [("runNumber", ROOT.TLeaf.GetValueLong64),
                      ("eventNumber", ROOT.TLeaf.GetValueLong64)]

unique_vars_target = [("runNumber", ROOT.TLeaf.GetValueLong64),
                      ("eventNumber", ROOT.TLeaf.GetValueLong64)]

# source_directory = '/fhgfs/users/abirnkraut/storage/SSPionProton/ProtonTagger'
# source_file_name = 'Data2011+2012_Bd2JpsiKst_Stripping21_Dvv38r1p2_Khanji_BTaggingAnalysis_FinalCalibrationTuple_IgnNeg.root'
source_directory = '/fhgfs/users/abirnkraut'
source_file_name = 'MU_2011_JpsiKst3.root'

target_directory = '/fhgfs/users/abirnkraut/Reprocessing_firstIteration'
target_file_name = 'MU_2011_JpsiKst3.root'

source_tree = 'Tagging'
target_tree = 'Tagging'


print("Processing {}...".format(source_file_name))

f_source = ROOT.TFile.Open('{}/{}'.format(source_directory, source_file_name))
if not f_source:
    print("File not found: {}".format(f_source))
    sys.exit(1)
t_source = f_source.Get(source_tree)
assert(isinstance(t_source, ROOT.TTree))

f_target = ROOT.TFile.Open('{}/{}'.format(target_directory, target_file_name))
if not f_target:
    print("File not found: {}".format(f_target))
    sys.exit(1)
t_target = f_target.Get(target_tree)
assert(isinstance(t_target, ROOT.TTree))

# Make a dictionary of value from the source
print("Creating input dictionary...")
var_leaf = []
for var in vars_source:
    var_leaf.append(t_source.GetLeaf(var))
result = {}
unique_leaves = [(t_source.GetLeaf(name), func) for name, func in unique_vars_source]
last_leaf = unique_leaves[-1][0]
# print "Some debug output"
# print unique_leaves
# print last_leaf
# print var_leaf

nEntries = t_source.GetEntriesFast()
for iEntry in xrange(nEntries):
    t_source.GetEntry(iEntry)
    var_value = []
    for var_leaff in var_leaf:
        var_value.append(var_leaff.GetValue())

    current_result_dict = result
    # print current_result_dict
    for unique_leaf, func in unique_leaves:
        value = func(unique_leaf)
        if unique_leaf is last_leaf:
            if value in current_result_dict.keys():
                raise("Duplicate value: {}".format(current_result_dict))
            else:
                current_result_dict[value] = var_value
        else:
            if value in current_result_dict.keys():
                current_result_dict = current_result_dict[value]
            else:
                new_dict = {}
                current_result_dict[value] = new_dict
                current_result_dict = new_dict
print("Created input dictionary!")
# print result

# Loop over the target, storing the events in the new tree
print("Matching events...")
counter_tag = 0
counter_mistag = 0
counter_all = 0
target_pair = []
nEntries = t_target.GetEntriesFast()
for iEntry in xrange(nEntries):
    target_pair = []
    t_target.GetEntry(iEntry)
    unique_values = [func(t_target.GetLeaf(name)) for name, func in unique_vars_target]
    current_result_dict = result
    var_value = None
    # print unique_values
    subdict = current_result_dict.get(unique_values[0], None)
    if subdict is None:
        # No match
        continue
    else:
        pair = subdict.get(unique_values[1], None)
        if pair is None:
            # no match
            continue
    target_pair.append(t_target.GetLeaf(vars_target[0]).GetValue(0))
    target_pair.append(t_target.GetLeaf(vars_target[1]).GetValue(0))
    # print "EventNumber: {0:.0f}, RunNumber: {1:.0f}".format(unique_values[1],unique_values[0])
    # print pair
    # print target_pair
    if abs(pair[0] - target_pair[0]) > 0.0001:
        counter_mistag = counter_mistag + 1
    if pair[1] != target_pair[1]:
        counter_tag = counter_tag + 1
    counter_all = counter_all + 1

print("Found {}/{} disagreements for the tag ({:.2f}%)".format(counter_tag, counter_all, 100. * counter_tag / counter_all))
print("Found {}/{} disagreements for the mistag ({:.2f}%)".format(counter_mistag, counter_all, 100. * counter_mistag / counter_all))
