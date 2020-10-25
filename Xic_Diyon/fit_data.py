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

GAUSS_PARAMS = [2469,   #Gauss Mean 
                2460,   #Gauss Mean - Min
                2478,   #Gauss Mean - Max         
                20,     #Gauss Width 
                17,      #Gauss Width - Min
                23]     #Gauss Width - Max

EXPONENTIAL_PARAMS = [-0.05, #Exponent
                      -5,    #Exponent - Min
                      0]     #Exponent - Max

CB_PARAMS = [20,   #CB Width
             17,   #CB Width - Min
             23,   #CB Width - Max
             1 ,   #CB N
             0 ,   #CB N - Min
             15]   #CB N - Max

FIT_EXPO = True
FIT_CB = False

"""
These functions return the normalistation lists of the wanted shape

"""

def getGaussNormParams(N):
    gNormList = [N/500 *2 ,
                0.5 , 
                N * 2]

    return gNormList

def getExpoNormParams(N):
    eNormList = [N*200 /2 , 
                 0.5, 
                 N *2]

    return eNormList

def getCBNormParams(N):
    CBNormList = [N/200 * 3, 0, N*2]
    
    return CBNormList


"""

The function used to fit signal

"""
def fit_signal(variable, root_file, out_directory):
    
    c = ROOT.TCanvas("c")

    print("Fitting...")
    print("Do not exit canvas")

    colours = [8, 46, 2]

    f = ROOT.TFile.Open(root_file, "READ")
    tree = f.Get("DecayTree")

    testFile = ROOT.TFile.Open(MEMORY+"temp.root","RECREATE")
    testFile.cd()

    if(CUTS != None) and (CUTS != ""):
        cutTree = tree.CopyTree(CUTS)
        N = cutTree.GetEntries()
    else:
        N = tree.GetEntries()

    h =  histogram = ROOT.TH1F("h", T, BINS, RANGE[0], RANGE[1])

    if(CUTS != None) and (CUTS != ""):
        cutTree.Draw(variable+">>h("+str(BINS)+","+str(RANGE[0])+","+str(RANGE[1])+")")
    else:
        tree.Draw(variable+">>h("+str(BINS)+","+str(RANGE[0])+","+str(RANGE[1])+")")

    h = ROOT.gDirectory.Get("h")
    h.SetLineColor(4)
    h.GetXaxis().SetTitle(X)
    h.GetYaxis().SetTitle(Y)
    h.SetTitle(T)
    h.Draw()

    var = ROOT.RooRealVar(variable, variable, VAR_PARAMS[0], VAR_PARAMS[1], UNIT)

    GNP = getGaussNormParams(N)

    gaussMean = ROOT.RooRealVar("gaussMean","gaussMean", GAUSS_PARAMS[0], GAUSS_PARAMS[1], GAUSS_PARAMS[2])
    gaussWidth = ROOT.RooRealVar("gaussWidth","gaussWidth", GAUSS_PARAMS[3], GAUSS_PARAMS[4], GAUSS_PARAMS[5])
    gaussNorm = ROOT.RooRealVar("gaussNorm","gaussNorm", GNP[0], GNP[1], GNP[2])

    gauss = ROOT.RooGaussian("gauss","gauss",var, gaussMean, gaussWidth)

    argList = ROOT.RooArgList(gauss)
    normArgList = ROOT.RooArgList(gaussNorm)
    components = ["gauss"]

    if(FIT_EXPO):

        ENP = getExpoNormParams(N)

        e = ROOT.RooRealVar("e","e",EXPONENTIAL_PARAMS[0], EXPONENTIAL_PARAMS[1], EXPONENTIAL_PARAMS[2])
        bkgNorm = ROOT.RooRealVar("bkgNorm","bkgNorm", ENP[0], ENP[1], ENP[2])

        bkg = ROOT.RooExponential("bkg","bkg", var, e)

        argList.add(bkg)
        normArgList.add(bkgNorm)
        components.append("bkg")

    if(FIT_CB):

        CBNP = getCBNormParams(N)

        cbw = ROOT.RooRealVar("cbw","cbw", CB_PARAMS[0], CB_PARAMS[1], CB_PARAMS[2])
        cba = ROOT.RooRealVar("cba","cba", EXPONENTIAL_PARAMS[0], EXPONENTIAL_PARAMS[1], EXPONENTIAL_PARAMS[2])
        cbn = ROOT.RooRealVar("cbn","cbn", CB_PARAMS[3], CB_PARAMS[4], CB_PARAMS[5])
        cbNorm = ROOT.RooRealVar("cbNorm","cbNorm", CBNP[0], CBNP[1], CBNP[2])

        CB = ROOT.RooCBShape("CB","CB", var, gaussMean, cbw, cba, cbn)

        argList.add(CB)
        normArgList.add(cbNorm)
        components.append("CB")


    model = ROOT.RooAddPdf("model" , "model", argList, normArgList)
    rHist = ROOT.RooDataHist("rHist", "rHist", ROOT.RooArgList(var), h)
    rHist.SetNameTitle("rHist" , T)

    model.fitTo(rHist)

    frame = var.frame()

    rHist.plotOn(frame)

    for i in range(len(components)):
        model.plotOn(frame, ROOT.RooFit.Components(components[i]), ROOT.RooFit.LineColor(colours[i]), ROOT.RooFit.LineStyle(2))
    
    model.plotOn(frame)

    y = 0
    e = 0
    
    for pdf in range(len(normArgList)):
        y += normArgList[pdf].getValV()
        e += normArgList[pdf].getError()

    legend = ROOT.TLegend(0.6, 0.6, 0.85 ,0.75)
    ROOT.SetOwnership(legend, False)
    legend.SetBorderSize(0)
    legend.SetShadowColor(2)
    legend.AddEntry(rHist, "Yield: {} +/- {}".format(int(y),int(e)), "L")
    legend.AddEntry(rHist, "Chi2: {}".format(frame.chiSquare()), "L")
    legend.SetTextSize(0.03)
    legend.SetTextColor(1)
    legend.Draw("same")

    frame.Draw("same")

    strings = root_file.split("/")
    outName = VAR+"_"+strings[len(strings)-1]+"_massFit.pdf"
    outFile = out_directory+outName

    c.Update()
    c.Draw()
    c.Print(outFile, "PDF")

    f.Close()
    testFile.Close()
    del testFile
    os.system("rm -rf {}".format(MEMORY+"temp.root"))
    print("Done")

    return

if __name__ == '__main__':

    if(len(sys.argv)==3):

        fit_signal(VAR , sys.argv[1], sys.argv[2])
