"""
This script appends efficiency values to a run's description file
"""

import ROOT, os, sys
import write_descriptions
from write_descriptions import appendEfficiency

RUN = "2"
ASYMMETRY_FILE = "/data/bfys/dwickrem/pdf_outputs/mass_fits/blinded_random/run_{}/".format(RUN)
MC = "/data/bfys/dwickrem/mc_tuples/"
BDT_MC = "/data/bfys/dwickrem/root_outputs/mc_blinded/"
CUT = "BDT_response > 0"

HANDLES = ["bdt"]

def computeBDTEfficiency():

    name = "BDT"

    for folder in os.listdir(MC):
        year = folder.split("_")[0]
        
        outDir = BDT_MC+year+"/"
        
        if not os.path.exists(outDir):
            os.makedirs(outDir)

        mc_file = MC+folder+"/Xic_MC_total.root"

        os.system("python BDT_script.py {} {}".format(mc_file,outDir))

        root_file = ROOT.TFile.Open(outDir+"BDT_Xic_MC_total.root","READ")
        temp_file = ROOT.TFile.Open(outDir+"temp.root","RECREATE")

        tree = root_file.Get("DecayTree")
        temp_file.cd()
        cut_tree = tree.CopyTree(CUT)

        value = str(cut_tree.GetEntries() / tree.GetEntries())

        appendEfficiency(ASYMMETRY_FILE,name, value, year)

        root_file.Close()
        temp_file.Close()
        del temp_file
        os.system("rm {}".format(outDir+"temp.root"))

if __name__ == '__main__':
    
    if(len(sys.argv) !=  2):
        print("\nPlease use one handle: >python compute_efficiencies.py <handle>")
        print("\nAvailable handles are: ")
        print(HANDLES)
        sys.exit()

    if(sys.argv[1] == HANDLES[0]):
        computeBDTEfficiency()


        
