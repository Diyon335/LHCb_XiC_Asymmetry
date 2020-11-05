"""
fitting_dependencies.py

This file holds the dictionary for bin-specific parameters and writes to a text file
"""
import numpy, math, os, sys

DICTIONARY = {}

def computeA(yields):
    return (yields[0] - yields[1])/(yields[0] + yields[1])

def computeAerror(A, yields):
    return math.sqrt(abs((1 - A**2)/(yields[0]-yields[1])))

def computeSum(a_list):
    return numpy.sum(a_list)

def computeError(a_list):
    total = 0
    for error in a_list:
        total += (error)**2
    return math.sqrt(total)

def writeFile(text_file, dictionary):

    TUPLES = "/data/bfys/dwickrem/root_outputs/blinded_random/run_2/"

    tfile = open(text_file, "w")

    dsets = ["dataset1","dataset2"]
    b_types = ["ptbins","ybins","y_ptbins"]
    
    yield_dictionary = {}
    total_yields = []
    x = 0

    for b_type in b_types:
        
        b_type_dict = {}
        for dset in dsets:

            dset_dict = {}
            for root_file in os.listdir(TUPLES+dset+"/"+b_type+"/"):
                dset_dict[root_file] = [0 , 0]

            b_type_dict[dset] = dset_dict

        yield_dictionary[b_type] = b_type_dict

            

    for dataset in dictionary:
        tfile.write("\n*** For "+dataset+" ***")

        for bin_type in dictionary[dataset]:
            tfile.write("\n** Bin: "+bin_type+" **")

            for root_file in dictionary[dataset][bin_type]:
                tfile.write("\n{}:{}".format(root_file, dictionary[dataset][bin_type][root_file]["results"]))
                
                strings = dictionary[dataset][bin_type][root_file]["results"].split(":")
                
                x += float(strings[0])

                yield_dictionary[bin_type][dataset][root_file][0] = float(strings[0])
                yield_dictionary[bin_type][dataset][root_file][1] = float(strings[1])

            tfile.write("\n ")
            tfile.write("\n ")

        tfile.write("\n ")
        tfile.write("\n ")

        total_yields.append(x)
        x = 0

    tfile.write("\n****** RESULTS ******")

    list1 = []
    list2 = []

    yields = []
    errors = []

    for bin_type in yield_dictionary:
        tfile.write("\nAsymetry in {}: ".format(bin_type))

        for dataset in yield_dictionary[bin_type]:

            for root_file in yield_dictionary[bin_type][dataset]:

                list1.append(yield_dictionary[bin_type][dataset][root_file][0])
                list2.append(yield_dictionary[bin_type][dataset][root_file][1])

            yields.append(computeSum(list1))
            errors.append(computeError(list2))

            list1.clear()
            list2.clear()
        
        A = computeA(yields)
        E = computeAerror(A, yields)
        tfile.write("{} +/- {}".format(str(A),str(E)))
        tfile.write("\n ")

        yields.clear()
        errors.clear()

    totalA = computeA(total_yields)
    totalE = computeAerror(totalA, total_yields)
    tfile.write("\nTOTAL ASYMMETRY: {} +/- {}".format(str(totalA) , str(totalE)))
    tfile.write("\n ")
    tfile.write("\nend")

    tfile.close()
    
    
                
