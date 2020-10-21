"""
BDT_script.py

This script uses a weights file from a trained BDT to reduce background events from a root file

Based on an existing tutorial, originally written in C++

Author: Diyon Wickremeratne
"""

import ROOT, os, sys, array, numpy
from ROOT import TFile, TTree

"""

The Main function that will carry out automated analysis

"""
def run():

    ROOT.TMVA.Tools.Instance()

    #Where you store your tuples
    TUPLES = "/data/bfys/dwickrem/tuples/"
    
    #True if running on randomised data, else on regular data
    random_data = True

    #Specify the run you want to apply the BDT to
    run_number = "run_1"

    weights_file = "/data/bfys/dwickrem/weights/BDT_BDT_BDT_Xic_pKpi_run21_100trees.weights.xml"

    print("\nBeginning the BDT script")

    TUPLES += run_number+"/"
    
    for i in os.listdir(TUPLES):

        #Ignore folders of clusters that may have not been deleted
        if "cluster" in i:
            continue

        #Ignore text files
        if "description" in i:
            continue

        if(random_data):
            for dset in os.listdir(TUPLES+i+"/random_data/"):

                print("\nWorking on: "+dset)

                for bin_type in os.listdir(TUPLES+i+"/random_data/"+dset+"/"):

                    print("\nFor the "+bin_type)

                    for root_file in os.listdir(TUPLES+i+"/random_data/"+dset+"/"+bin_type+"/"):

                        if not os.path.exists(TUPLES+i+"/BDT_outputs/"+run_number+"/"+dset+"/"+bin_type+"/"):
                            os.makedirs(TUPLES+i+"/BDT_outputs/"+run_number+"/"+dset+"/"+bin_type+"/")

                        saving_directory = TUPLES+i+"/BDT_outputs/"+run_number+"/"+dset+"/"+bin_type+"/"

                        print("\nWorking on: "+root_file)

                        runMVA(root_file, TUPLES+i+"/random_data/"+dset+"/"+bin_type+"/"+root_file, saving_directory, weights_file)
        else:
            for bin_type in os.listdir(TUPLES+i+"/bins/"):

                print("\nFor the "+bin_type)

                for root_file in os.listdir(TUPLES+i+"/bins/"+bin_type+"/"):

                    if not os.path.exists(TUPLES+i+"/BDT_outputs/"+run_number+"/"+bin_type+"/"):
                        os.makedirs(TUPLES+i+"/BDT_outputs/"+run_number+"/"+bin_type+"/")

                    saving_directory = TUPLES+i+"/BDT_outputs/"+run_number+"/"+bin_type+"/"

                    print("\nWorking on: "+root_file)

                    runMVA(root_file, TUPLES+i+"/bins/"+bin_type+"/"+root_file, saving_directory, weights_file)

        
"""

This function carries out the TMVA analysis

Parameters are a file name, the root file to analyse, where you want to save it and finally the weights file you want to use

"""
def runMVA(file_name, root_file, saving_directory, weights_file):
    
    read_file = ROOT.TFile(root_file, "READ")
    dataTree = read_file.Get("DecayTree")

    reader =  ROOT.TMVA.Reader("V:Color:!Silent")
    
    #Variables that were used to train the BDT
    variables =[ "lcplus_RAPIDITY",
	 	 "piplus_RAPIDITY",
		 "pplus_RAPIDITY",
		 "kminus_RAPIDITY",
		 "lcplus_ENDVERTEX_CHI2",
		 "lcplus_IPCHI2_OWNPV",
		 "pplus_OWNPV_CHI2",
		 "kminus_OWNPV_CHI2",
		 "piplus_OWNPV_CHI2",
		 "lcplus_IP_OWNPV",
		 "piplus_ProbNNpi",
		 "pplus_ProbNNp",
		 "kminus_ProbNNk",
		 "pplus_TRACK_PCHI2",
		 "piplus_TRACK_PCHI2",
		 "kminus_TRACK_PCHI2",
                 "log(lcplus_FD_OWNPV)",
                 "log(pplus_PT)",
                 "log(piplus_IP_OWNPV)",
                 "log(pplus_IP_OWNPV)",
                 "log(kminus_IP_OWNPV)",
                 "log(kminus_PT)",
                 "log(piplus_PT)",
                 "log(lcplus_PT)",
                 "log(kminus_IPCHI2_OWNPV)",
                 "log(piplus_IPCHI2_OWNPV)",
                 "log(pplus_IPCHI2_OWNPV)"]

    n = 0
    for variable in variables:
        exec("var"+str(n)+" = array.array(\"f\",[0])")
        exec("reader.AddVariable(\""+variable+"\",var"+str(n)+")")
        n+=1

    reader.BookMVA("BDT method", weights_file)

    dataSample_vars =  ["lcplus_MM", 
                       "lcplus_P", 
                       "lcplus_PT", 
                       "lcplus_ETA",
                       "lcplus_RAPIDITY", 
                       "lcplus_TIP", 
                       "lcplus_IPCHI2_OWNPV", 
                       "lcplus_OWNPV_CHI2", 
                       "lcplus_TAU",
                       "lcplus_IP_OWNPV",
                       "lcplus_L0HadronDecision_TOS", 
                       "lcplus_FD_OWNPV",
                       "lcplus_ENDVERTEX_CHI2",
                       "pplus_M", 
                       "pplus_P", 
                       "pplus_PT",
                       "pplus_RAPIDITY", 
                       "pplus_ETA",
                       "pplus_ProbNNp",
                       "pplus_OWNPV_CHI2",
                       "kminus_OWNPV_CHI2",
                       "piplus_OWNPV_CHI2",
                       "piplus_M",
                       "piplus_P", 
                       "piplus_PT", 
                       "piplus_RAPIDITY",
                       "piplus_ETA",
                       "piplus_ProbNNpi",
                       "piplus_IP_OWNPV",
                       "pplus_PIDp",
                       "kminus_M",
                       "kminus_P", 
                       "kminus_PT", 
                       "kminus_RAPIDITY",
                       "kminus_ETA",
                       "kminus_ProbNNk", 
                       "kminus_PIDK", 
                       "PVNTRACKS",
                       "piplus_PX", 
                       "pplus_PX", 
                       "kminus_PX", 
                       "piplus_PY", 
                       "pplus_PY", 
                       "kminus_PY", 
                       "piplus_PZ", 
                       "pplus_PZ", 
                       "kminus_PZ",
                       "pplus_IP_OWNPV",
                       "kminus_IP_OWNPV",
                       "kminus_IPCHI2_OWNPV",
                       "piplus_IPCHI2_OWNPV",
                       "pplus_IPCHI2_OWNPV",
                       "pplus_TRACK_PCHI2",
                       "piplus_TRACK_PCHI2",
		       "kminus_TRACK_PCHI2",
                       "lcplus_Hlt1TrackMVADecision_TOS"]

    x = 0
    for var in dataSample_vars:
        exec("dsvar"+str(x)+" = array.array(\"f\",[0])")
        exec("dataTree.SetBranchAddress(\""+var+"\", dsvar"+str(x)+")")
        x+=1

    MVAOutput = numpy.zeros(1, dtype = float)

    save_file = ROOT.TFile(saving_directory+"BDT_"+file_name, "RECREATE")
    tree = dataTree.CopyTree("0")

    output_vars = [    "lcplus_MM", 
                       "lcplus_P", 
                       "lcplus_PT", 
                       "lcplus_ETA",
                       "lcplus_RAPIDITY", 
                       "lcplus_TIP", 
                       "lcplus_IPCHI2_OWNPV", 
                       "lcplus_OWNPV_CHI2", 
                       "lcplus_TAU",
                       "lcplus_IP_OWNPV",
                       "lcplus_L0HadronDecision_TOS", 
                       "lcplus_FD_OWNPV",
                       "lcplus_ENDVERTEX_CHI2",
                       "pplus_M", 
                       "pplus_P", 
                       "pplus_PT",
                       "pplus_RAPIDITY", 
                       "pplus_ETA",
                       "pplus_ProbNNp",
                       "pplus_OWNPV_CHI2",
                       "kminus_OWNPV_CHI2",
                       "piplus_OWNPV_CHI2",
                       "piplus_M",
                       "piplus_P", 
                       "piplus_PT", 
                       "piplus_RAPIDITY",
                       "piplus_ETA",
                       "piplus_ProbNNpi",
                       "piplus_IP_OWNPV",
                       "pplus_PIDp",
                       "kminus_M",
                       "kminus_P", 
                       "kminus_PT", 
                       "kminus_RAPIDITY",
                       "kminus_ETA",
                       "kminus_ProbNNk", 
                       "kminus_PIDK", 
                       "PVNTRACKS",
                       "piplus_PX", 
                       "pplus_PX", 
                       "kminus_PX", 
                       "piplus_PY", 
                       "pplus_PY", 
                       "kminus_PY", 
                       "piplus_PZ", 
                       "pplus_PZ", 
                       "kminus_PZ",
                       "pplus_IP_OWNPV",
                       "kminus_IP_OWNPV",
                       "kminus_IPCHI2_OWNPV",
                       "piplus_IPCHI2_OWNPV",
                       "pplus_IPCHI2_OWNPV",
                       "pplus_TRACK_PCHI2",
                       "piplus_TRACK_PCHI2",
		       "kminus_TRACK_PCHI2",
                       "lcplus_Hlt1TrackMVADecision_TOS"]


    a = 0
    for ovar in output_vars:
        exec("output"+str(a)+" = numpy.zeros(1, dtype = float)")
        exec("dataTree.SetBranchAddress(\""+ovar+"\", output"+str(a)+")")
        exec("tree.Branch(\""+ovar+"\" , output"+str(a)+",\""+ovar+"/D\")")
        a+=1


    tree.Branch("BDT_output",MVAOutput,"BDT_response/D")

    b = 0
    c = dataTree.GetEntries()
    for i in range(dataTree.GetEntries()):

        if(b%1000==0):
            k = (b / c)*100
            sys.stdout.write('\r')
            sys.stdout.write("Progress: {0}%".format(str(int(k))))
            sys.stdout.flush()
        
        dataTree.GetEntry(i)
        
        m = 0
        for var in dataSample_vars:

            if "PVNTRACKS" in var:
                continue

            exec("dsvar"+str(m)+"[0] = tree."+var)
            m+=1

        MVAOutput[0] = reader.EvaluateMVA("BDT method")

        tree.Fill()

        b+=1

    sys.stdout.write('\r')
    sys.stdout.write("Progress: 100%")
    sys.stdout.flush()
    
    save_file.cd()
    save_file.Write("",ROOT.TObject.kOverwrite)
    tree.SetName("DecayTree")
    tree.Write("",ROOT.TObject.kOverwrite)

    save_file.Close()
    read_file.Close()


"""

There is an option to run it on one particular root file by entering the appropriate arguments after the python command.

Usage: >python BDT_script.py <path to root file> <saving directoy>

"""

if __name__ == '__main__':
    
    if(len(sys.argv) == 3):

        root_file = sys.argv[1]

        strings = root_file.split("/")
        index = len(strings)-1
        name = strings[index]

        saving_directory = sys.argv[2]

        wf = "/data/bfys/dwickrem/weights/BDT_BDT_BDT_Xic_pKpi_run21_100trees.weights.xml"

        runMVA(name, root_file, saving_directory, wf)

    else:
        run()


