import ROOT

method = 'BDT'
label = 'BDT_Xic_pKpi_run1'

data_file = f'TMVA_{method}_{label}.root'
ROOT.TMVA.TMVAGUI(data_file, label)
input("Press enter to continue")