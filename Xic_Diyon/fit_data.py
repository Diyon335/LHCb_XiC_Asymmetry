"""
fit_data.py

This script can be used to fit a signal with a shape and calculate its yield

Author: Diyon Wickremeratne
"""

import ROOT, sys, os
from fitting_dependencies import writeFile

"""

Global parameters. Change them here

"""
## Dictionary to save data ##
DICTIONARY = {}

## For paths and saving directories ##

TUPLES = "/data/bfys/dwickrem/root_outputs/blinded_random/run_2/2016_MagDown_blinded/"
PDF_OUTPUT = "/data/bfys/dwickrem/pdf_outputs/mass_fits/blinded_random/run_2/"
ASYMMETRY_FILE = "/data/bfys/dwickrem/pdf_outputs/mass_fits/blinded_random/run_2/asymmetry.txt"
SETS = ["dataset1", "dataset2"]
TUPLE_BINS = ["ptbins","ybins","y_ptbins"]

## For histogram ##
MEMORY = "/data/bfys/dwickrem/root_outputs/"

VAR = "lcplus_MM"
UNIT = "MeV/c^{2}"

BINS = 300

RANGE = [2400,2540]

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
                2,     #Gauss Width 
                1,      #Gauss Width - Min
                7]     #Gauss Width - Max

EXPONENTIAL_PARAMS = [-0.07, #Exponent
                      -0.08,    #Exponent - Min
                      -0.001]     #Exponent - Max

CB_PARAMS = [2,   #CB Width
             1,   #CB Width - Min
             7,   #CB Width - Max
             1 ,   #CB N
             0 ,   #CB N - Min
             15]   #CB N - Max

FIT_EXPO = True
FIT_CB = True

"""
These functions return the normalistation lists of the wanted shape

"""

def getGaussNormParams(N):
    gNormList = [N ,
                N/500 * 2, 
                 2*N]

    return gNormList

def getExpoNormParams(N):
    eNormList = [N * 0.5, 
                 N/1000, 
                 N * 2]

    return eNormList

def getCBNormParams(N):
    CBNormList = [N, N/500 * 2, N*2]
    
    return CBNormList


"""

The function used to fit signal

"""
def fit_signal(variable, root_file, out_directory, dset, bin_type):
    
    c = ROOT.TCanvas("c")

    print("Fitting...")
    print("Do not exit canvas")

    colours = [8, 46, 2]

    f = ROOT.TFile.Open(root_file, "READ")
    tree = f.Get("DecayTree")

    testFile = ROOT.TFile.Open(MEMORY+"temp.root","RECREATE")
    testFile.cd()

    if(CUTS != None) and (CUTS != ""):
        print("Applying cuts")
        cutTree = tree.CopyTree(CUTS)
        N = cutTree.GetEntries()
    else:
        N = tree.GetEntries()

    h =  histogram = ROOT.TH1F("h", T, BINS, RANGE[0], RANGE[1])

    if(CUTS != None) and (CUTS != ""):
        print("Drawing the cut tree")
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
    frame.SetMinimum(0)

    y = normArgList[0].getValV()
    e = normArgList[0].getError()

    legend = ROOT.TLegend(0.6, 0.6, 0.85 ,0.75)
    ROOT.SetOwnership(legend, False)
    legend.SetBorderSize(0)
    legend.SetShadowColor(2)
    legend.AddEntry(rHist, "Yield: {} +/- {}".format(int(y),int(e)), "")
    legend.AddEntry(rHist, "Chi2: {}".format(frame.chiSquare()), "")
    legend.SetTextSize(0.03)
    legend.SetTextColor(1)
    legend.Draw("same")
    
    frame.Draw("same")

    strings = root_file.split("/")
    name = strings[len(strings)-1].replace(".root","")
    outName = VAR+"_"+name+"_shapeFit.pdf"
    outFile = out_directory+outName

    DICTIONARY[dset][bin_type][strings[len(strings)-1]] = "{}:{}:{}".format(str(y) , str(e), str(frame.chiSquare()))

    c.Update()
    c.Draw()
    c.Print(outFile, "PDF")

    f.Close()
    testFile.Close()
    del testFile
    os.system("rm -rf {}".format(MEMORY+"temp.root"))
    print("Done for "+name)


def runFits():

    print("Running fits")

    if not os.path.exists(PDF_OUTPUT):
        os.makedirs(PDF_OUTPUT)

    #Build the dictionary
    for dset in SETS:

        bin_dict = {}
        for bin_type in TUPLE_BINS:

            root_dict = {}
            for root_file in os.listdir(TUPLES+"/"+dset+"/"+bin_type+"/"):
                root_dict[root_file] = ""

            bin_dict[bin_type] = root_dict

        DICTIONARY[dset] = bin_dict

    for dset in SETS:
        for bin_type in TUPLE_BINS:
            for root_file in os.listdir(TUPLES+"/"+dset+"/"+bin_type+"/"):
                

                outDir = PDF_OUTPUT+"/"+dset+"/"+bin_type+"/"
                if not os.path.exists(outDir):
                    os.makedirs(outDir)

                fit_signal(VAR, TUPLES+"/"+dset+"/"+bin_type+"/"+root_file , outDir, dset, bin_type)
                
    print("Writing file")
    
    writeFile(ASYMMETRY_FILE , DICTIONARY)

    print("Done")


if __name__ == '__main__':

    runFits()
