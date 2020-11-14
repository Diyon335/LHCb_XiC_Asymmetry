"""
This script is used to make a BDT based on tree files which contain signal
and background data. The script loads the trees in one by one (they are kept
in many different smaller files) and then makes use of the ROOT TMVA module
to train and test a BDT.

Author: Maris Koopmans
"""

from array import array
import psutil
import ROOT
import os

def train(bkgFile, sigFile, discriList, transfoList, MVAmethod, nTraining, label, cuts, numtrees, outDir):

    ROOT.TMVA.Tools.Instance()

    print(f'Started training BDT with {numtrees} trees')

    # Define the file to which the BDT will be written
    MVA_fileName = 'TMVA_'+MVAmethod+'_'+label+'.root'
    file_MVA = ROOT.TFile(outDir+MVA_fileName,'recreate')

    print('Will write MVA info in ', MVA_fileName)

    # Define the TMVA factory and dataloader
    factory = ROOT.TMVA.Factory(MVAmethod, file_MVA)
    dataloader = ROOT.TMVA.DataLoader(label)

    bkg_files = 1155
    sig_files = 13

    Nproc1 = 0
    Nproc2 = 0

    # Keep lists to keep the trees and and files 'active' in, so that the dataloader
    # still knows where to access them
    sig_files_list = [0 for i in range(sig_files)]
    sig_trees_list = [0 for i in range(sig_files)]

    bkg_files_list = [0 for i in range(bkg_files)]
    bkg_trees_list = [0 for i in range(bkg_files)]

    # Load in all background trees
    for num in range(bkg_files):

        print(num)

        bkg_files_list[num] = ROOT.TFile.Open(bkgFile + f'/background_cut_{num}.root', "READONLY")
        bkg_trees_list[num] = bkg_files_list[num].Get("DecayTree")

        ents_bkg = float(bkg_trees_list[num].GetEntries())
        bkg_weight = 1/ents_bkg
        Nproc1 += ents_bkg

        dataloader.AddBackgroundTree(bkg_trees_list[num], bkg_weight)

    # Load in all signal trees
    for num in range(sig_files):

        sig_files_list[num] = ROOT.TFile.Open(sigFile + f'/signal_cut_{num}.root', "READONLY")
        sig_trees_list[num] = sig_files_list[num].Get("DecayTree")

        ents_sig = float(sig_trees_list[num].GetEntries())
        sig_weight = 1/ents_sig
        Nproc2 += ents_sig

        dataloader.AddSignalTree(sig_trees_list[num], sig_weight)


    # Define variables
    for discriVar in discriList:
        dataloader.AddVariable(discriVar)

    for function, varname in transfoList:
        dataloader.AddVariable(function, varname, "", "F")



    print(f'Total number of signal events: {Nproc2}')
    print(f'Total number of background events: {Nproc1}')

    print('Loaded all background and signal trees')

    # add cuts here if necessary
    sigcut = ROOT.TCut(cuts)
    bkgcut = ROOT.TCut(cuts)

    # Prepare the training and testing trees with the number of events to be used
    # for each, and the way to split the selection of these events (random)
    dataloader.PrepareTrainingAndTestTree( ROOT.TCut( sigcut ), ROOT.TCut( bkgcut ),
                                      ':'.join([ 'nTrain_Signal={}'.format(int(nTraining * Nproc2)),     # Number of signal events used, 0 = ALL
                                               'nTrain_Background={}'.format(int(nTraining * Nproc1)), # Number of background events, 0 = ALL
                                               'nTest_Signal={}'.format(int((1 - nTraining) * Nproc2)),     # Number of signal events used, 0 = ALL
                                               'nTest_Background={}'.format(int((1 - nTraining) * Nproc1)), # Number of background events, 0 = ALL
                                               'SplitMode=Random',    # How are events chosen to be used for either training or testing
                                               'NormMode=NumEvents',  # Integral of datasets is given by number of events
                                                                      #   (could e.g. also be sum of weights or simply defined to be 1)
                                               '!V'                   # Don't print everything (i.e. not verbose) 
                                               ]))

    print('Prepared training and testing tree')

    # Configuration string for the BDT, can be modified
    BDTcfg = f'!H:!V:NTrees={numtrees}:MaxDepth=5:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning'

    factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, 'BDT_'+label,BDTcfg)

    # Train, test and evaluate the BDT
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
    file_MVA.Close()

    print("Done")
