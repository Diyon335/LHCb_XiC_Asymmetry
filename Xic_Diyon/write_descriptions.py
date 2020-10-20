"""
This script exists to write an automated description covering the important steps of tuple preparation


Author: Diyon Wickremeratne
"""

def makeFile(path, run, dictionary = None, blinded = False):
    tfile = open(path+"{}_description.txt".format(run), "x")
    tfile.write("This is an auto-generated description file for: {}".format(run))
    
    tfile.write("\nTuple preparation was done for the following data:")
    
    for element in dictionary:
        tfile.write("\n - {}".format(dictionary[element][0]))
    
    if(blinded):
        tfile.write("\nBlinded: Yes")
    else:
        tfile.write("\nBlinded: No")
        
    tfile.close()
    
def appendBins(path, run, bins = None):
    tfile = open(path+"{}_description.txt".format(run), "a")
    
    tfile.write("\nBins used to split files: ")
    
    for bin_type in bins:
        tfile.write("\n - {}".format(bin_type))
        
    tfile.close()
    
def appendVars(path, run, variables = None):
    tfile = open(path+"{}_description.txt".format(run), "a")
    
    tfile.write("\nThere were {} variables used in this preparation of tuples".format(str(len(variables))))
    tfile.write("\nVariables used to create trees: ")
    
    for var in variables:
        tfile.write("\n - {}".format(var))
        
    tfile.close()
    
    
def writeStartOfRandomisation(path, run):
    tfile = open(path+"{}_description.txt".format(run), "a")
    
    tfile.write("\n***Displayed below are the results of the randomisation process***")
    tfile.write("\n")
    tfile.write(" ")
    tfile.write("\n")
    tfile.close()
    
    
    
def appendTreeAnalysis(path, run, data_folder, file_name, totalEvents, tree1Events, tree2Events):
    tfile = open(path+"{}_description.txt".format(run), "a")
    
    tfile.write("\n** FOR {} DATA **".format(data_folder))
    tfile.write("\n * {}".format(file_name))
    tfile.write("\n Total events: {}".format(str(totalEvents)))
    tfile.write("\nEvents in tree1: {}".format(str(tree1Events)))
    tfile.write("\nEvents in tree2: {}".format(str(tree2Events)))
    tfile.write("\nUnused events: {}".format(str(totalEvents - (tree1Events + tree2Events))))
    tfile.write("\nAsymmetry: {}".format(str((tree1Events - tree2Events)/(tree1Events + tree2Events))))
    tfile.write("\n")
    tfile.write(" ")
    
    tfile.close()

def appendTimeElapsed(path, run, time):
    tfile = open(path+"{}_description.txt".format(run), "a")
    
    tfile.write("\nTime elapsed in hours: {}".format( str((time/60)/60)) )
    tfile.close()
    
    
