"""
plot_histogram.py

This script is a minimal configuration/automated script to plot a histogram. Many things can/must be added/changed manually

The script can be used when you want to plot one variable of a particular root file

Usage: >python plot_histogram.py <varName> <root_file> <output_directory> [bins] [From] [To] [xTitle] [yTitle] [hTitle] [cuts]

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

"""
This function was made to compare the invariant mass distributions of your prepped tuples before and after being passed through the BDT

Since this thesis only worked on 2016 MD data, this function was made to only run on this year's data
"""

def runBDTComparison():
    #These lists are needed so that the function works in proper order
    sets = ["dataset1","dataset2"]
    bins = ["ptbins","ybins","y_ptbins"]
    tot_files = ["BDT_Xic_total.root"]
    
    BDT_outputs = "/data/bfys/dwickrem/root_outputs/blinded_random/run_2/2016/"
    save_directory = "/data/bfys/dwickrem/pdf_outputs/BDT_comparison/BDT_1/"
    textFile = "/data/bfys/dwickrem/pdf_outputs/BDT_comparison/BDT_1/afterHistograms.txt"

    variable = "lcplus_MM"

    cuts = "BDT_response > 0"
    saveName = "BDT_response_"

    hBins = 300
    hRange = [2360,2570]
    x = "Mass MeV/c^{2}"
    y = "Candidates"

    h1T = "Plot of {} before and after BDT (2016 MagDown)".format(variable)
    h2T = "Plot of {} before and after BDT (2016 MagDown)".format(variable)

    print("Beginning to plot histograms")
    print("For total root files")

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    txtFile = open(textFile, "w")
    txtFile.close()

    for tot_file in tot_files:
        tot_path = BDT_outputs+tot_file
        tot_name = tot_file.replace(".root","")
        tot_outFile = save_directory+saveName+tot_name+".pdf"
        plotAndSave(textFile, tot_path, tot_outFile, variable, cuts, h1T, h2T, hBins, hRange, x, y)

    for dset in sets:
        print("Working on {}".format(dset))
        for btype in bins:
            print("For the {}".format(btype))
            for root_file in os.listdir(BDT_outputs+dset+"/"+btype+"/"):

                print(root_file)

                if not os.path.exists(save_directory+dset+"/"+btype+"/"):
                    os.makedirs(save_directory+dset+"/"+btype+"/")
                
                path = BDT_outputs+dset+"/"+btype+"/"+root_file
                name = root_file.replace(".root","")
                outFile = save_directory+dset+"/"+btype+"/"+saveName+name+".pdf"

                plotAndSave(textFile, path, outFile, variable, cuts, h1T, h2T, hBins, hRange, x, y)
                
    print("Done")


def plotAndSave(textfile, rootFilePath, outFileName, variable, Cuts, h1T, h2T, Bins, rangeList, xT, yT):
     rfile = ROOT.TFile.Open(rootFilePath, "READ")
     tempFile = ROOT.TFile.Open("/data/bfys/dwickrem/root_outputs/temp.root","RECREATE")
     
     tempFile.cd()
     tree = rfile.Get("DecayTree")
     cutTree = tree.CopyTree(Cuts)
     
     c = ROOT.TCanvas("c")
     
     h1 = ROOT.TH1F("BEFORE", h1T, Bins, rangeList[0], rangeList[1])
     tree.Draw(variable+">>BEFORE("+str(Bins)+","+str(rangeList[0])+","+str(rangeList[1])+")")
     h1 = ROOT.gDirectory.Get("BEFORE")
     h1.SetLineColor(4)
     h1.GetXaxis().SetTitle(xT)
     h1.GetYaxis().SetTitle(yT)
     h1.SetTitle(h1T)
     
     h2 = ROOT.TH1F("AFTER", h2T, Bins, rangeList[0], rangeList[1])
     cutTree.Draw(variable+">>AFTER("+str(Bins)+","+str(rangeList[0])+","+str(rangeList[1])+")")
     h2 = ROOT.gDirectory.Get("AFTER")
     h2.SetLineColor(3)
     h2.GetXaxis().SetTitle(xT)
     h2.GetYaxis().SetTitle(yT)
     h2.SetTitle(h2T)

     tfile = open(textfile, "a")
     tfile.write("\nFor: "+rootFilePath)
     tfile.write("\nTITLE: "+h2T)
     tfile.write("\nENTRIES: "+str(h2.GetEntries()))
     tfile.write("\nMEAN: "+str(h2.GetMean()))
     tfile.write("\nSTD DEV: "+str(h2.GetRMS()))
     tfile.close()
     
     h1.Draw()
     h2.Draw("same")
     
     legend = ROOT.TLegend(0.8, 0.5, 0.95, 0.65)
     ROOT.SetOwnership(legend, False)
     legend.SetBorderSize(1)
     legend.SetShadowColor(2)
     legend.AddEntry(h1, "Before", "l")
     legend.AddEntry(h2, "After", "l")
     legend.SetTextSize(0.03)
     legend.SetTextColor(1)
     legend.Draw("same")
     c.Update()
     
     c.Draw()
     c.Print(outFileName,"PDF")
     
     rfile.Close()
     tempFile.Close()
     
     c.Close()
     del c

     del tempFile
     os.system("rm -rf {}".format("/data/bfys/dwickrem/root_outputs/temp.root"))
                

if __name__ == '__main__':
    
    if(len(sys.argv) == 4):
        plotSimpleHist(sys.argv[1], sys.argv[2], sys.argv[3])
    elif(len(sys.argv) == 11):
        plotSimpleHist(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4], sys.argv[5], sys.argv[6],sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
    else:
        #print("Usage: python plot_histogram.py <varName> <root_file> <output_directory> [bins] [From] [To] [xTitle] [yTitle] [hTitle] [cuts]")
        
        runBDTComparison()
