"""
fit_data.py

This script can be used to fit a signal with a shape and calculate its yield

Currently works on one year at a time

Author: Diyon Wickremeratne
"""

import ROOT, sys, os
from fitting_dependencies import writeFile


"""

Global parameters. Change them here

"""
#This will save any files that may need refitting
flags = []

## Dictionary to save data ##
DICTIONARY = {}

## For paths and saving directories ##
YEAR = "2016"

TUPLES = "/data/bfys/dwickrem/root_outputs/blinded_random/run_2/{}/".format(YEAR)
PDF_OUTPUT = "/data/bfys/dwickrem/pdf_outputs/mass_fits/blinded_random/run_2/{}/".format(YEAR)
ASYMMETRY_FILE = "/data/bfys/dwickrem/pdf_outputs/mass_fits/blinded_random/run_2/{}/asymmetry.txt".format(YEAR)
DICTIONARY_FILE = "/data/bfys/dwickrem/pdf_outputs/mass_fits/blinded_random/run_2/{}/fitting_dictionary.py".format(YEAR)
SETS = ["dataset1", "dataset2"]
TUPLE_BINS = ["ptbins","ybins","y_ptbins"]

sys.path.insert(0, "/data/bfys/dwickrem/pdf_outputs/mass_fits/blinded_random/run_2/{}/".format(YEAR))

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
def fit_signal(variable, root_file, out_directory, dset, bin_type, refit_dictionary = None):

    strings = root_file.split("/")

    ## For fit shape ##
    VAR_PARAMS = [2360, #Variable - Min
                  2570] #Variable - Max
    
    if(refit_dictionary == None):
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

    else:
        GAUSS_PARAMS = refit_dictionary[dset][bin_type][strings[len(strings)-1]]["gaussParams"]
        EXPONENTIAL_PARAMS = refit_dictionary[dset][bin_type][strings[len(strings)-1]]["expoParams"]
        CB_PARAMS = refit_dictionary[dset][bin_type][strings[len(strings)-1]]["cbParams"]

    FIT_EXPO = True
    FIT_CB = False
    
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

    h = ROOT.TH1F("h", T, BINS, RANGE[0], RANGE[1])

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

    if(refit_dictionary == None):
        GNP = getGaussNormParams(N)
    else:
        GNP = []
        for gparam in refit_dictionary[dset][bin_type][strings[len(strings)-1]]["gaussNormParams"]:
            GNP.append(gparam * N)

    gaussMean = ROOT.RooRealVar("gaussMean","gaussMean", GAUSS_PARAMS[0], GAUSS_PARAMS[1], GAUSS_PARAMS[2])
    gaussWidth = ROOT.RooRealVar("gaussWidth","gaussWidth", GAUSS_PARAMS[3], GAUSS_PARAMS[4], GAUSS_PARAMS[5])
    gaussNorm = ROOT.RooRealVar("gaussNorm","gaussNorm", GNP[0], GNP[1], GNP[2])

    gauss = ROOT.RooGaussian("gauss","gauss",var, gaussMean, gaussWidth)

    argList = ROOT.RooArgList(gauss)
    normArgList = ROOT.RooArgList(gaussNorm)
    components = ["gauss"]

    if (refit_dictionary == None):
        DICTIONARY[dset][bin_type][strings[len(strings)-1]]["gaussParams"] = GAUSS_PARAMS
        DICTIONARY[dset][bin_type][strings[len(strings)-1]]["gaussNormParams"] = [GNP[0]/N , GNP[1]/N , GNP[2]/N]

    if(FIT_EXPO):
        if(refit_dictionary == None):
            ENP = getExpoNormParams(N)
        else:
            ENP = []
            for eparam in refit_dictionary[dset][bin_type][strings[len(strings)-1]]["expoNormParams"]:
                ENP.append(eparam * N)

        e = ROOT.RooRealVar("e","e",EXPONENTIAL_PARAMS[0], EXPONENTIAL_PARAMS[1], EXPONENTIAL_PARAMS[2])
        bkgNorm = ROOT.RooRealVar("bkgNorm","bkgNorm", ENP[0], ENP[1], ENP[2])

        bkg = ROOT.RooExponential("bkg","bkg", var, e)

        argList.add(bkg)
        normArgList.add(bkgNorm)
        components.append("bkg")

        if (refit_dictionary == None):
            DICTIONARY[dset][bin_type][strings[len(strings)-1]]["expoParams"] = EXPONENTIAL_PARAMS
            DICTIONARY[dset][bin_type][strings[len(strings)-1]]["expoNormParams"] = [ENP[0]/N , ENP[1]/N , ENP[2]/N]

    if(FIT_CB):
        if (refit_dictionary == None):
            CBNP = getCBNormParams(N)
        else:
            CBNP = []
            for cbparam in refit_dictionary[dset][bin_type][strings[len(strings)-1]]["cbNormParams"]:
                CBNP.append(cbparam * N)

        cbw = ROOT.RooRealVar("cbw","cbw", CB_PARAMS[0], CB_PARAMS[1], CB_PARAMS[2])
        cba = ROOT.RooRealVar("cba","cba", EXPONENTIAL_PARAMS[0], EXPONENTIAL_PARAMS[1], EXPONENTIAL_PARAMS[2])
        cbn = ROOT.RooRealVar("cbn","cbn", CB_PARAMS[3], CB_PARAMS[4], CB_PARAMS[5])
        cbNorm = ROOT.RooRealVar("cbNorm","cbNorm", CBNP[0], CBNP[1], CBNP[2])

        CB = ROOT.RooCBShape("CB","CB", var, gaussMean, cbw, cba, cbn)

        argList.add(CB)
        normArgList.add(cbNorm)
        components.append("CB")

        if (refit_dictionary == None):
            cb_param_list = [CB_PARAMS[0], CB_PARAMS[1], CB_PARAMS[2], EXPONENTIAL_PARAMS[0], EXPONENTIAL_PARAMS[1], EXPONENTIAL_PARAMS[2], CB_PARAMS[3], CB_PARAMS[4], CB_PARAMS[5]]
            DICTIONARY[dset][bin_type][strings[len(strings)-1]]["cbParams"] = cb_param_list
            DICTIONARY[dset][bin_type][strings[len(strings)-1]]["cbNormParams"] = [ CBNP[0]/N , CBNP[1]/N, CBNP[2]/N]


    model = ROOT.RooAddPdf("model" , "model", argList, normArgList)
    rHist = ROOT.RooDataHist("rHist", "rHist", ROOT.RooArgList(var), h)
    rHist.SetNameTitle("rHist" , T)

    model.fitTo(rHist)

    frame = var.frame()

    rHist.plotOn(frame)

    for i in range(len(components)):
        model.plotOn(frame, ROOT.RooFit.Components(components[i]), ROOT.RooFit.LineColor(colours[i]), ROOT.RooFit.LineStyle(2))
    
    model.plotOn(frame)

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
    
    frame.SetAxisRange(0, 1600, "Y")
    frame.Draw("same")

    name = strings[len(strings)-1].replace(".root","")
    outName = VAR+"_"+name+"_shapeFit.pdf"
    outFile = out_directory+outName

    chi = frame.chiSquare()

    if(chi < 0.4) or (chi > 2):
        flags.append(outFile)
    
    if (refit_dictionary == None):
        DICTIONARY[dset][bin_type][strings[len(strings)-1]]["results"] = "{}:{}:{}".format(str(y) , str(e), str(frame.chiSquare()))
    else:
        refit_dictionary[dset][bin_type][strings[len(strings)-1]]["results"] = "{}:{}:{}".format(str(y) , str(e), str(frame.chiSquare()))

        writeDict(DICTIONARY_FILE, refit_dictionary)

    if (refit_dictionary != None):
        if os.path.isfile(outFile):
            os.system("rm -rf {}".format(outFile))

    c.Update()
    c.Draw()
    c.Print(outFile, "PDF")

    f.Close()
    testFile.Close()
    c.Close()

    ROOT.gDirectory.Delete("h")

    del c
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
            for root_file in os.listdir(TUPLES+dset+"/"+bin_type+"/"):

                file_dict = {"results" : ""}
                root_dict[root_file] = file_dict

            bin_dict[bin_type] = root_dict

        DICTIONARY[dset] = bin_dict

    for dset in SETS:
        for bin_type in TUPLE_BINS:
            for root_file in os.listdir(TUPLES+dset+"/"+bin_type+"/"):
                

                outDir = PDF_OUTPUT+dset+"/"+bin_type+"/"
                if not os.path.exists(outDir):
                    os.makedirs(outDir)

                fit_signal(VAR, TUPLES+dset+"/"+bin_type+"/"+root_file , outDir, dset, bin_type)
                
    print("Writing file")
    
    writeFile(ASYMMETRY_FILE , DICTIONARY, YEAR)

    writeDict(DICTIONARY_FILE, DICTIONARY)

    print("\nDone")
    print("\nTo refit, use >python fit_data.py <dataset>:<bin>:<root_file>")

def writeDict(path, dictionary):
    python_file = open(path,"w")
    python_file.write("fitting_dictionary = {")

    ds_n = 0
    for ds in dictionary:
        
        python_file.write("\n\t\""+ds+"\":{")

        b_n = 0
        for b in dictionary[ds]:
            
            python_file.write("\n\t\t\""+b+"\":{")
                
            fi_n = 0
            for fi in dictionary[ds][b]:

                python_file.write("\n\t\t\t\""+fi+"\":{")
            
                n = 0
                for r in dictionary[ds][b][fi]:
                    if (n==0):
                        python_file.write("\n\t\t\t\t\"{}\":\"{}\",".format(r , dictionary[ds][b][fi][r]))
                    else:
                        if(n+1 == len(dictionary[ds][b][fi])):
                            python_file.write("\n\t\t\t\t\""+r+"\":"+ str(dictionary[ds][b][fi][r])+" }")
                        else:
                            python_file.write("\n\t\t\t\t\"{}\":{} ,".format(r , dictionary[ds][b][fi][r]))
                    n+=1

                if (fi_n+1 == len(dictionary[ds][b])):
                    python_file.write("\n\t\t\t }")
                else:
                    python_file.write("\n\t\t\t ,")

                fi_n+=1

            if (b_n+1 == len(dictionary[ds])):
                python_file.write("\n\t\t }")
            else:
                python_file.write("\n\t\t ,")

            b_n+=1
        
        if(ds_n +1 == len(dictionary)):
           python_file.write("\n\t}")
        else:
           python_file.write("\n\t,")

        ds_n+=1
    
    python_file.close()
    


if __name__ == '__main__':
    
    if(len(sys.argv) == 2):
        argument = sys.argv[1]
        arguments = argument.split(":")

        if (len(arguments) != 3):
            print("\nInsufficient arguments")
            print("\nTo refit, use >python fit_data.py <dataset>:<bin>:<root_file>")
            print("\nFor example, >python fit_data.py dataset1:ybin:BDT_Xic_ybin_2.0-2.5.root")
            sys.exit()
        elif not arguments[0] in SETS:
            print("\nIncorrect dataset. Check again")
            sys.exit()
        elif not arguments[1] in TUPLE_BINS:
            print("\nIncorrect bin type. Check again")
            sys.exit()
        elif not os.path.isfile(DICTIONARY_FILE):
            print("\nYou have no fitting dictionary. Run script without arguments")
            sys.exit()
        else:
            from fitting_dictionary import fitting_dictionary as refitting_dictionary

            outDir = PDF_OUTPUT+arguments[0]+"/"+arguments[1]+"/"

            fit_signal(VAR, TUPLES+arguments[0]+"/"+arguments[1]+"/"+arguments[2] , outDir, arguments[0] , arguments[1] , refit_dictionary = refitting_dictionary)

            from fitting_dictionary import fitting_dictionary as rd

            writeFile(ASYMMETRY_FILE , rd, YEAR)
            print("\nDone refitting")
            
    else:
        runFits()

        if(len(flags) > 0):
            print("These files were flagged and might need refitting:")
            for j in flags:
                print("\n"+j)
