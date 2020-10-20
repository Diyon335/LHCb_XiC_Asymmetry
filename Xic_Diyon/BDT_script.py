import ROOT, os, sys, array, numpy
from ROOT import TFile, TTree

ROOT.TMVA.Tools.Instance()

#Where you store your tuples
TUPLES = "/data/bfys/dwickrem/tuples/"

#True if running on randomised data, else on regular data
random_data = True

#Specify the run you want to apply the BDT to
run_number = "run_1"

weights_file = "/data/bfys/dwickrem/weights/BDT_BDT_BDT_Xic_pKpi_run21_100trees.weights.xml"

def getList(length):
    aList = []
    for i in range(length-1):
        aList.append(0)
    return aList

def run():

    print("\nBeginning the BDT script")
    
    for i in os.listdir(TUPLES+run_number+"/"):

        #Ignore folders of clusters that may have not been deleted
        if "cluster" in i:
            continue

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

        


#Takes in a root file, and runs through the BDT
def runMVA(file_name, root_file, saving_directory, weights_file):

    read_file = ROOT.TFile(root_file, "READ")
    dataTree = read_file.Get("DecayTree")

    save_file = ROOT.TFile(saving_directory+"BDT_"+file_name, "RECREATE")
    tree = dataTree.CloneTree(0)

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

    
    branches = {}
    for var in variables:
        branch = var
        branches[branch] = array.array("f",[0])
        reader.AddVariable(branch, branches[branch])

    reader.BookMVA("BDT method", weights_file)
    
    bdt_vars = {}
    for v in variables:
        bdt_var = v
        bdt_vars[bdt_var] = array.array("f",[0])
        dataTree.SetBranchAddress(v, bdt_vars[bdt_var])

    #The variables you want in the output file to be viewed later. The BDT response must be in this list (maybe at the end)
    output_vars =     ["lcplus_MM", 
                       "lcplus_P", 
                       "lcplus_PT", 
                       "lcplus_ETA",
                       "lcplus_RAPIDITY", 
                       "lcplus_TIP", 
                       "lcplus_IPCHI2_OWNPV", 
                       "lcplus_OWNPV_CHI2", 
                       "lcplus_TAU",
                       "lcplus_L0HadronDecision_TOS", 
                       "lcplus_FD_OWNPV",
                       "pplus_M", 
                       "pplus_P", 
                       "pplus_PT",
                       "pplus_RAPIDITY", 
                       "pplus_ETA",
                       "pplus_ProbNNp",
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
                       "BDT_response"]

    output_branches = {}
    for variable in output_vars:
        output_branch = variable
        output_branches[output_branch] = array.array("f",[0])

        print(output_branch)
        print(output_branches[output_branch]) 
        
        if(variable != "BDT_response"):
            dataTree.SetBranchAddress(output_branch , output_branches[output_branch])

        tree.Branch(output_branch, output_branches[output_branch])

    
    #Evaluate BDT response for all entries
    read_file.cd()
    x = 0
    n = dataTree.GetEntries()
    for i in dataTree.GetEntries():

        if(x%1000==0):
            j = (x / n)*100
            sys.stdout.write('\r')
            sys.stdout.write("{0}%".format(str(int(j))))
            sys.stdout.flush()
        
        dataTree.GetEntry(i)

        output_brances["BDT_response"] = reader.EvaluateMVA("BDT method")

        save_file.cd()
        tree.Fill()

    sys.stdout.write('\r')
    sys.stdout.write("100%")
    sys.stdout.flush()
    
    save_file.cd()
    tree.SetName("DecayTree")
    tree.Write("",ROOT.TObject.kOverwrite)

    save_file.Close()
    read_file.Close()




if __name__ == '__main__':
    
    if(len(sys.argv) == 3):

        root_file = sys.argv[1]

        strings = root_file.split("/")
        index = len(strings)-1
        name = strings[index]

        saving_directory = sys.argv[2]

        wf = weights_file

        runMVA(name, root_file, saving_directory, wf)

    else:
        run()


