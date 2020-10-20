import ROOT, sys

#Minimal configurisation for this method
def plotSimpleHist(variable, root_file, out_directory):
    print("Plotting...")
    bins = 300
    hRange = [2360,2570]
    lineCol = 4
    xTitle = "Mass MeV/c^2"
    yTitle = "Events"
    hTitle = "Plot of {}".format(variable)

    rfile = ROOT.TFile.Open(root_file, "READ")
    tree = rfile.Get("DecayTree")

    strings = root_file.split("/")
    index = len(strings)-1
    outName = strings[index]+"_histPlot.pdf"
    outFile = out_directory+outName

    c = ROOT.TCanvas("c")
    
    print("Do not exit canvas")

    histogram = ROOT.TH1F("histogram", hTitle, bins, hRange[0], hRange[1])
    tree.Draw(variable+">>histogram("+str(bins)+","+str(hRange[0])+","+str(hRange[1])+")")
    histogram = ROOT.gDirectory.Get("histogram")
    histogram.SetLineColor(lineCol)
    histogram.GetXaxis().SetTitle(xTitle)
    histogram.GetYaxis().SetTitle(yTitle)
    histogram.SetTitle(hTitle)
    histogram.Draw()

    c.Update()
    c.Draw()
    c.Print(outFile, "PDF")
    print("Done!")
    return

if __name__ == '__main__':
    
    if(len(sys.argv) == 4):
        plotSimpleHist(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python <script> <varName> <root_file> <output_directory>")
