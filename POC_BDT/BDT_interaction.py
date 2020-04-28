import ROOT, sys
import train_BDT

#### define signal and background trees + selection to be applied ###

bkgTree = 'KKP_background.root'
sigTree = 'KKP_signal.root'

file_proc1 = ROOT.TFile(bkgTree)    
file_proc2 = ROOT.TFile(sigTree)   

tree_proc1 = file_proc1.Get('Events')
tree_proc2 = file_proc2.Get('Events')


#### input variables to be used for training ###
variables = [
    'P_tot_sq',
    'B_FlightDistance',
    'B_VertexChi2'
]

# Apply no cuts just yet
cuts = ''

#### define MVA method ###

method = 'BDT'
nTrain = 0
label = 'Collision_KKP'


#### train the MVA ####
train_BDT.train(tree_proc1, tree_proc2, variables, method, nTrain, label, cuts)


#### check the output with the TMVAGUI ####

outFileName = 'TMVA_{}_{}.root'.format(method, label)
ROOT.TMVA.TMVAGui(outFileName, label)
input('Press Enter to continue...')