"""
plot_histogram.py

This script is a minimal configuration/automated script to plot a histogram. Many things can/must be added/changed manually

The script can be used when you want to plot one variable of a particular root file

Usage: >python plot_histogram.py  <var> <file> <saving directory>

Author: Diyon Wickremeratne
"""


import ROOT, sys

"""

This function takes in a variable name, a root file to get this variable from and a directory to which the resulting plot will be saved (PDF format)

"""
def plotSimpleHist(variable, root_file, out_directory):
    print("Plotting...")
    bins = 300
    hRange = [-0.7,0.5]
    lineCol = 4
    xTitle = "Mass MeV/c^{2}"
    yTitle = "Candidates"
    hTitle = "Plot of {}".format(variable)

    rfile = ROOT.TFile.Open(root_file, "READ")
    tree = rfile.Get("DecayTree")

    cutTree = tree.CopyTree("BDT_response > -0.18")

    strings = root_file.split("/")
    index = len(strings)-1
    outName = variable+"_"+strings[index]+"_histPlot.pdf"
    outFile = out_directory+outName

    c = ROOT.TCanvas("c")
    
    print("Do not exit canvas")

    histogram = ROOT.TH1F("histogram", hTitle, bins, hRange[0], hRange[1])
    cutTree.Draw(variable+">>histogram("+str(bins)+","+str(hRange[0])+","+str(hRange[1])+")")
    histogram = ROOT.gDirectory.Get("histogram")
    histogram.SetLineColor(lineCol)
    histogram.GetXaxis().SetTitle(xTitle)
    histogram.GetYaxis().SetTitle(yTitle)
    histogram.SetTitle(hTitle)
    histogram.Draw()

    c.Update()
    c.Draw()
    c.Print(outFile, "PDF")

    rfile.Close()

    print("Done!")
    return

if __name__ == '__main__':
    
    if(len(sys.argv) == 4):
        plotSimpleHist(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python plot_histogram.py <varName> <root_file> <output_directory>")
