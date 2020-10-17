import ROOT, os, sys, array
from ROOT import TFile, TTree

ROOT.TMVA.Tools.Instance()

#Where you store your tuples
TUPLES = "/dcache/bfys/dwickrem/test1/"

#True if running on randomised data, else on regular data
random_data = True

#If you run it multiple times
run_number = "2"

if(random_data):
    run_number += "_(randomised)"

weights_file = "TMVAClassification.weights.xml"

def run():

    print("\nBeginning the BDT script")
    
    for i in os.listdir(TUPLES):

        #Ignore folders of clusters that may have not been deleted
        if "cluster" in i:
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

    save_file = ROOT.TFile(saving_directory+file_name, "RECREATE")
    tree = ROOT.TTree("DecayTree","DecayTree")

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
		 "kminus_TRACK_PCHI2"]

    branches = {}
    for var in variables:
        branch = var
        branches[branch] = array("f",[0])
        reader.AddVariable(branch, branches[branch])

    reader.BookMVA("BDT method", weights_file)

    for var in variables:
        dataTree.SetBranchAddress(var, branches[var])

    #The variables you want in the output file to be viewed later. The BDT response must be in this list
    output_vars = ["lcplus_MM","BDT_response"]

    output_branches = {}
    for variable in output_vars:
        output_branch = variable
        output_branches[output_branch] = array("f",[0])
        
        if(variable != "BDT_response"):
            read_file.cd()
            dataTree.SetBranchAddress(output_branch , output_branches[output_branch])

        save_file.cd()
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

        reader.EvaluateMVA("BDT method")

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
    
    run()


