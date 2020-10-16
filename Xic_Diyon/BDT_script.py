import ROOT, os, sys
from ROOT import TFile, TTree

ROOT.TMVA.Tools.Instance()

#Where you store your tuples
TUPLES = "/dcache/bfys/dwickrem/test1/"

#True if running on randomised data, else on regular data
random_data = False

def run():

    print("\nBeginning the BDT script")
    
    for i in os.listdir(TUPLES):

        #Ignore folders of clusters that may have not been deleted
        if "cluster" in i:
            continue

        if not os.path.exists(TUPLES+i+"/BDT_outputs/"):
            os.makedirs(TUPLES+i+"/BDT_outputs/")

        saving_directory = TUPLES+i+"/BDT_outputs/"

        if(random_data):
            for dset in os.listdir(TUPLES+i+"/random_data/"):

                print("\nWorking on: "+dset)

                for bin_type in os.listdir(TUPLES+i+"/random_data/"+dset+"/"):

                    print("\nFor the "+bin_type)

                    for root_file in os.listdir(TUPLES+i+"/random_data/"+dset+"/"+bin_type+"/"):

                        print(root_file)
        else:
            for bin_type in os.listdir(TUPLES+i+"/bins/"):

                print("\nFor the "+bin_type)

                for root_file in os.listdir(TUPLES+i+"/bins/"+bin_type+"/"):

                    print(root_file)

        


#Takes in a root file, and runs through the BDT
def runMVA():
    return None




if __name__ == '__main__':
    
    run()


