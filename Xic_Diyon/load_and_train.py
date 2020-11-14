"""
This script is the 'interface' for the training of the BDT; here the
variables and number of events to train on are defined.

Author: Maris Koopmans 
"""

import time
import ROOT
import os, sys
from Train_BDT import train


def main(run_num, numtrees, outDir):

	start_time = time.time()

	# Define paths to the signal and background folder
	sig_folder = '/data/bfys/mkoopmans/data/signal_finalvars_sigsmall'
	bkg_folder = '/data/bfys/mkoopmans/data/background_finalvars_sigsmall'
                

	# Define the MVA method, fraction of events to be used for training
	# (0 = all) and name of the BDT
	method = 'BDT'
	cuts = ''
	numevents = 0.8
	label = f'BDT_Xic_pKpi_run{run_num}_{numtrees}trees'

	# List of all variables to be used for training the BDT
	raw_variables = ["lcplus_RAPIDITY",
		"piplus_RAPIDITY",
		"pplus_RAPIDITY",
		"kminus_RAPIDITY",
		# "lcplus_TIP",
		# 'lcplus_FD_OWNPV',
		'lcplus_ENDVERTEX_CHI2',
		'lcplus_IPCHI2_OWNPV',
		'pplus_OWNPV_CHI2',
		'kminus_OWNPV_CHI2',
		'piplus_OWNPV_CHI2',
		# 'pplus_PT',
		'lcplus_IP_OWNPV',
		# 'piplus_IP_OWNPV',
		# 'pplus_IP_OWNPV',
		# 'kminus_IP_OWNPV',
		# 'kminus_PT',
		# 'piplus_PT',
		# 'lcplus_PT',
		# 'kminus_IPCHI2_OWNPV',
		# 'piplus_IPCHI2_OWNPV',
		# 'pplus_IPCHI2_OWNPV',
		'piplus_ProbNNpi',
		'pplus_ProbNNp',
		'kminus_ProbNNk',
		'pplus_TRACK_PCHI2',
		'piplus_TRACK_PCHI2',
		'kminus_TRACK_PCHI2']

	transfor_variables = []

	transfor_variables = [("log(lcplus_FD_OWNPV)", "lcplus_FD_OWNPV_log"),\
	# 					  ("log(lcplus_ENDVERTEX_CHI2)", "lcplus_ENDVERTEX_CHI2_log"),\
	# 					  ("log(lcplus_IPCHI2_OWNPV)", "lcplus_IPCHI2_OWNPV_log"),\
	# 					  ("log(pplus_OWNPV_CHI2)", "pplus_OWNPV_CHI2_log"),\
	# 					  ("log(kminus_OWNPV_CHI2)", "kminus_OWNPV_CHI2_log"),\
	# 					  ("log(piplus_OWNPV_CHI2)", "piplus_OWNPV_CHI2_log"),\
						  ("log(pplus_PT)", "pplus_PT_log"),\
	# 					  ("exp(lcplus_IP_OWNPV)", "lcplus_IP_OWNPV_exp"),\
						  ("log(piplus_IP_OWNPV)", "piplus_IP_OWNPV_log"),\
						  ("log(pplus_IP_OWNPV)", "pplus_IP_OWNPV_log"),\
						  ("log(kminus_IP_OWNPV)", "kminus_IP_OWNPV_log"),\
						  ("log(kminus_PT)", "kminus_PT_log"),\
						  ("log(piplus_PT)", "piplus_PT_log"),\
						  ("log(lcplus_PT)", "lcplus_PT_log"),\
						  ("log(kminus_IPCHI2_OWNPV)", "kminus_IPCHI2_OWNPV_log"),\
						  ("log(piplus_IPCHI2_OWNPV)", "piplus_IPCHI2_OWNPV_log"),\
						  ("log(pplus_IPCHI2_OWNPV)", "pplus_IPCHI2_OWNPV_log")]
						  # ("log(lcplus_DIRA_OWNPV)", "lcplus_DIRA_OWNPV_log")]
	# 					  ("1 - sqrt(1 - piplus_ProbNNpi)", "piplus_ProbNNpi_trans"),\
	# 					  ("1 - sqrt(1 - pplus_ProbNNp)", "pplus_ProbNNpi_trans"),\
	# 					  ("1 - sqrt(1 - kminus_ProbNNk)", "kminus_ProbNNpi_trans")]

	# Actually train the BDT
	train(bkg_folder, sig_folder, raw_variables, transfor_variables, method, numevents, label, cuts, numtrees, outDir)

	print(f'This run finished in t = {time.time() - start_time} s\n')


run_num = sys.argv[1]
ntrees = sys.argv[2]
outDir = sys.argv[3]
main(run_num, ntrees, outDir)
