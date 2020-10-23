"""
fit_data.py

This script can be used to fit a signal with a shape and calculate its yield

Author: Diyon Wickremeratne
"""

import ROOT, sys, os

"""
Global parameters. Change them here
"""

## For histogram ##
MEMORY = "/data/bfys/dwickrem/root_outputs/"

VAR = "lcplus_MM"
UNIT = "MeV/c^{2}"

BINS = 300

RANGE = [2360,2570]

X = "Mass MeV/c^{2}"
Y = "Events"
T = "Plot of {}".format(VAR)

CUTS = "BDT_response > 0"

## For fit shape ##
VAR_PARAMS = [2360, #Variable - Min
              2570] #Variable - Max

GAUSS_PARAMS = [2465,   #Gauss Mean 
                2450,   #Gauss Mean - Min
                2480,   #Gauss Mean - Max         
                30,     #Gauss Width 
                20,     #Gauss Width - Min
                40]     #Gauss Width - Max

EXPONENTIAL_PARAMS = [-0.5, #Exponent
                      -1,   #Exponent - Min
                      -1.5] #Exponent - Max

FIT_EXPO = True



"""

This function returns a histogram of the desired variable. It needs a directory to store temporary root files in order to handle memory properly

"""
def getHistogram(variable, root_file,  memory_directory, bins = None, From = None, To = None, xTitle = None, yTitle = None, hTitle = None, cuts = None):
    
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
    
    testFile = ROOT.TFile.Open(memory_directory+"temp.root","RECREATE")
    testFile.cd()
    
    if (cuts != None) and (cuts != ""):
        cutTree = tree.CopyTree(cuts)

    histogram = ROOT.TH1F("histogram", htitle, hBins, hRange[0], hRange[1])
    
    if(cuts != None) and (cuts != ""):
        cutTree.Draw(variable+">>histogram("+str(hBins)+","+str(hRange[0])+","+str(hRange[1])+")")
    else:
        tree.Draw(variable+">>histogram("+str(hBins)+","+str(hRange[0])+","+str(hRange[1])+")")

    histogram = ROOT.gDirectory.Get("histogram")
    histogram.SetLineColor(lineCol)
    histogram.GetXaxis().SetTitle(xtitle)
    histogram.GetYaxis().SetTitle(ytitle)
    histogram.SetTitle(htitle)
    histogram.Draw()

    rfile.Close()
    testFile.Close()

    del testFile
    os.system("rm -rf {}".format(memory_directory+"temp.root"))

    return histogram


"""

The function used to fit signal

"""
def fit_signal(variable, root_file, out_directory):
    
    c = ROOT.TCanvas("c")

    print("Fitting...")

    colours = [8, 46, 2]

    f = ROOT.TFile.Open(root_file, "READ")
    tree = f.Get("DecayTree")
    N = tree.GetEntries()

    h = getHistogram(VAR , root_file , MEMORY , bins = BINS, From = RANGE[0], To = RANGE[1], xTitle = X, yTitle = Y, hTitle = T, cuts = CUTS)

    var = ROOT.RooRealVar(variable, variable, VAR_PARAMS[0], VAR_PARAMS[1], UNIT)

    gaussMean = ROOT.RooRealVar("gaussMean","gaussMean", GAUSS_PARAMS[0], GAUSS_PARAMS[1], GAUSS_PARAMS[2])
    gaussWidth = ROOT.RooRealVar("gaussWidth","gaussWidth", GAUSS_PARAMS[3], GAUSS_PARAMS[4], GAUSS_PARAMS[5])
    gaussNorm = ROOT.RooRealVar("gaussNorm","gaussNorm", N/500 * 2, 0.5, N*2)

    gauss = ROOT.RooGaussian("gauss","gauss",var, gaussMean, gaussWidth)

    argList = ROOT.RooArgList(gauss)
    normArgList = ROOT.RooArgList(gaussNorm)
    components = ["gauss"]

    if(FIT_EXPO):
        e = ROOT.RooRealVar("e","e",EXPONENTIAL_PARAMS[0], EXPONENTIAL_PARAMS[1], EXPONENTIAL_PARAMS[2])
        bkgNorm = ROOT.RooRealVar("bkgNorm","bkgNorm", N/200 * 3, 0 , N*2)

        bkg = ROOT.RooExponential("bkg","bkg", var, e)

        argList.add(bkg)
        normArgList.add(bkgNorm)
        components.append("bkg")

    #CB Maybe?


    model = ROOT.RooAddPdf("model" , "model", argList, normArgList)
    h = ROOT.gDirectory.Get("histogram")
    rHist = ROOT.RooDataHist("rHist", "rHist", ROOT.RooArgList(var), h)

    model.fitTo(rHist)

    frame = var.frame()

    rHist.plotOn(frame)

    for i in range(len(components)):
        model.plotOn(frame, ROOT.RooFit.Components(components[i]), ROOT.RooFit.LineColor(colours[i]), ROOT.RooFit.LineStyle(2))
    
    model.plotOn(frame)

    frame.Draw()

    strings = root_file.split("/")
    outName = VAR+"_"+strings[len(strings)-1]+"_massFit.pdf"
    outFile = out_directory+outName

    print("Do not exit canvas")

    c.Update()
    c.Draw()
    c.Print(outFile, "PDF")

    f.Close()
    print("Done")

    return

if __name__ == '__main__':

    if(len(sys.argv)==3):

        fit_signal(VAR , sys.argv[1], sys.argv[2])
