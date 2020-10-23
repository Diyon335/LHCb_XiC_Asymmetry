"""
plot_histogram.py

This script is a minimal configuration/automated script to plot a histogram. Many things can/must be added/changed manually

The script can be used when you want to plot one variable of a particular root file

Usage: >python plot_histogram.py  <var> <file> <saving directory>

Author: Diyon Wickremeratne
"""
import ROOT, sys, os

"""

This function needs a variable name, a root file to get this variable from and a directory to which the resulting plot will be saved (PDF format)

"""
def plotSimpleHist(variable, root_file, out_directory, bins = None, From = None, To = None, xTitle = None, yTitle = None, hTitle = None, cuts = None):
    print("Plotting...")
    
    if(bins != None):
        hBins = int(bins)
    else:
        hBins = 200

    if (From != None) and (To != None):
        hRange = [int(From),int(To)]
    else:
        hRange = [2360,2570]

    lineCol = 4
    
    if (xTitle != None):
        xtitle = xTitle
    else:
        xtitle = "Mass MeV/c^{2}"

    if (yTitle != None):
        ytitle = yTitle
    else:
        yTitle = "Candidates"

    if (hTitle != None):
        htitle = hTitle
    else:
        htitle = "Plot of {}".format(variable)

    rfile = ROOT.TFile.Open(root_file, "READ")
    tree = rfile.Get("DecayTree")
    
    testFile = ROOT.TFile.Open(out_directory+"temp.root","RECREATE")
    testFile.cd()
    
    if (cuts != None):
        cutTree = tree.CopyTree(cuts)

    strings = root_file.split("/")
    index = len(strings)-1
    outName = variable+"_"+strings[index]+"_histPlot.pdf"
    outFile = out_directory+outName

    c = ROOT.TCanvas("c")
    
    print("Do not exit canvas")

    histogram = ROOT.TH1F("histogram", htitle, hBins, hRange[0], hRange[1])
    
    if(cuts != None):
        cutTree.Draw(variable+">>histogram("+str(hBins)+","+str(hRange[0])+","+str(hRange[1])+")")
    else:
        tree.Draw(variable+">>histogram("+str(hBins)+","+str(hRange[0])+","+str(hRange[1])+")")

    histogram = ROOT.gDirectory.Get("histogram")
    histogram.SetLineColor(lineCol)
    histogram.GetXaxis().SetTitle(xtitle)
    histogram.GetYaxis().SetTitle(ytitle)
    histogram.SetTitle(htitle)
    histogram.Draw()

    c.Update()
    c.Draw()
    c.Print(outFile, "PDF")

    rfile.Close()
    testFile.Close()

    del testFile
    os.system("rm -rf {}".format(out_directory+"temp.root"))

    print("Done!")
    return

if __name__ == '__main__':
    
    if(len(sys.argv) == 4):
        plotSimpleHist(sys.argv[1], sys.argv[2], sys.argv[3])
    elif(len(sys.argv) == 11):
        plotSimpleHist(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4], sys.argv[5], sys.argv[6],sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
    else:
        print("Usage: python plot_histogram.py <varName> <root_file> <output_directory> [bins] [From] [To] [xTitle] [yTitle] [hTitle] [cuts]")
