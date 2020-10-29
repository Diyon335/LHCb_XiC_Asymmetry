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
    
    BDT_outputs = "/data/bfys/dwickrem/root_outputs/blinded_random/run_2/2016_MagDown_blinded/"
    save_directory = "/data/bfys/dwickrem/pdf_outputs/BDT_comparison/"

    variable = "lcplus_MM"

    cuts = "BDT_response > 0"

    hBins = 300
    hRange = [2360,2570]
    x = "Mass MeV/c^{2}"
    y = "Candidates"

    h1T = "Plot of {} before and after BDT (2016 MagDown)".format(variable)
    h2T = "Plot of {} before and after BDT (2016 MagDown)".format(variable)
    

    print("Beginning to plot histograms")
    for dset in sets:
        print("Working on {}".format(dset))
        for btype in bins:
            print("For the {}".format(btype))
            for root_file in os.listdir(BDT_outputs+dset+"/"+btype+"/"):

                print(root_file)

                if not os.path.exists(save_directory+dset+"/"+btype+"/"):
                    os.makedirs(save_directory+dset+"/"+btype+"/")
                
                rfile = ROOT.TFile.Open(BDT_outputs+dset+"/"+btype+"/"+root_file, "READ")
                tempFile = ROOT.TFile.Open("/data/bfys/dwickrem/root_outputs/temp.root","RECREATE")
                name = root_file.replace(".root","")
                outFile = save_directory+dset+"/"+btype+"/"+"BDT_responseCheck_"+name+".pdf"

                tempFile.cd()
                tree = rfile.Get("DecayTree")
                cutTree = tree.CopyTree(cuts)

                c = ROOT.TCanvas("c")

                h1 = ROOT.TH1F("H1", h1T, hBins, hRange[0], hRange[1])
                tree.Draw(variable+">>H1("+str(hBins)+","+str(hRange[0])+","+str(hRange[1])+")")
                h1 = ROOT.gDirectory.Get("H1")
                h1.SetLineColor(4)
                h1.GetXaxis().SetTitle(x)
                h1.GetYaxis().SetTitle(y)
                h1.SetTitle(h1T)

                h2 = ROOT.TH1F("H2", h2T, hBins, hRange[0], hRange[1])
                cutTree.Draw(variable+">>H2("+str(hBins)+","+str(hRange[0])+","+str(hRange[1])+")")
                h2 = ROOT.gDirectory.Get("H2")
                h2.SetLineColor(3)
                h2.GetXaxis().SetTitle(x)
                h2.GetYaxis().SetTitle(y)
                h2.SetTitle(h2T)

                h1.Draw()
                h2.Draw("same")

                legend1 = ROOT.TLegend(0.8, 0.5 , 0.95, 0.65)
                legend1.SetHeader("H2","C")
                ROOT.SetOwnership(legend1,False)
                legend1.SetBorderSize(1)
                legend1.SetShadowColor(2)
                legend1.AddEntry("entries","Entries   "+str(cutTree.GetEntries()), "")
                legend1.SetTextSize(0.04)
                legend1.SetTextColor(1)
                legend1.Draw("same")
                
                legend = ROOT.TLegend(0.8, 0.3, 0.95, 0.45)
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
                c.Print(outFile,"PDF")

                rfile.Close()
                tempFile.Close()

                c.Close()
                del c

                del tempFile
                os.system("rm -rf {}".format("/data/bfys/dwickrem/root_outputs/temp.root"))
                break
            break
        break
                
    print("Done")
                

    
    

if __name__ == '__main__':
    
    if(len(sys.argv) == 4):
        plotSimpleHist(sys.argv[1], sys.argv[2], sys.argv[3])
    elif(len(sys.argv) == 11):
        plotSimpleHist(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4], sys.argv[5], sys.argv[6],sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
    else:
        #print("Usage: python plot_histogram.py <varName> <root_file> <output_directory> [bins] [From] [To] [xTitle] [yTitle] [hTitle] [cuts]")
        
        runBDTComparison()
