import ROOT

bkg_tree = ROOT.RDataFrame('Events', 'KKP_background.root')
sig_tree = ROOT.RDataFrame('Events', 'KKP_signal.root')

names = bkg_tree.GetColumnNames()


ips_list = [n for n in names if ("IPChi2" in n or n == "P_tot_sq")]
no_scale_list = [n for n in names if ("isMuon" in n or "Charge" in n)]
rest = [n for n in names if (n not in ips_list and n not in no_scale_list)]


N_bkg = bkg_tree.Count().GetValue()
N_sig = sig_tree.Count().GetValue()
bkg_sig_ratio = N_bkg / N_sig 


norm = 1


c = ROOT.TCanvas()


# Plot the IPChi2 lists with a very smally cropped x-axis
for n in ips_list:

	temp_hist_bkg = bkg_tree.Histo1D((f"{n}_sigHist", n, 200, sig_tree.Min(n).GetValue(), sig_tree.Max(n).GetValue() / 40), n)
	temp_hist_bkg.Scale(norm/N_bkg, "height")

	temp_hist_bkg.SetFillStyle(3007)

	temp_hist_bkg.SetStats(False)
	temp_hist_bkg.SetFillColor(ROOT.kBlue)

	temp_hist_sig = sig_tree.Histo1D((f"{n}_sigHist", n, 200, sig_tree.Min(n).GetValue(), sig_tree.Max(n).GetValue() / 40), n)
	temp_hist_sig.Scale(norm/N_sig, "height")

	temp_hist_sig.SetFillStyle(3007)

	temp_hist_sig.SetStats(False)
	temp_hist_sig.SetFillColor(ROOT.kRed)

	temp_hist_bkg.Draw("HIST")
	temp_hist_sig.Draw("SAME HIST")

	c.Update()

	c.SaveAs(f"test_data_dist_plots/{n}.png")


# Plot the Boolean charge/isMuon not on a cropped axis
for n in no_scale_list:

	temp_hist_bkg = bkg_tree.Histo1D((f"{n}_sigHist", n, 200, sig_tree.Min(n).GetValue(), sig_tree.Max(n).GetValue()), n)
	temp_hist_bkg.Scale(norm/N_bkg, "height")

	temp_hist_bkg.SetFillStyle(3007)


	temp_hist_bkg.SetStats(False)
	temp_hist_bkg.SetFillColor(ROOT.kBlue)

	temp_hist_sig = sig_tree.Histo1D((f"{n}_sigHist", n, 200, sig_tree.Min(n).GetValue() / 5, sig_tree.Max(n).GetValue() / 5), n)
	temp_hist_sig.Scale(norm/N_sig, "height")

	temp_hist_sig.SetFillStyle(3007)

	temp_hist_sig.SetStats(False)
	temp_hist_sig.SetFillColor(ROOT.kRed)

	temp_hist_bkg.Draw("HIST")
	temp_hist_sig.Draw("SAME HIST")

	c.Update()

	c.SaveAs(f"test_data_dist_plots/{n}.png")


# Plot the res
for n in rest:

	temp_hist_bkg = bkg_tree.Histo1D((f"{n}_sigHist", n, 200, sig_tree.Min(n).GetValue() / 5, sig_tree.Max(n).GetValue() / 5), n)

	temp_hist_bkg.Scale(norm/N_bkg, "height")

	temp_hist_bkg.SetFillStyle(3007)

	temp_hist_bkg.SetStats(False)
	temp_hist_bkg.SetFillColor(ROOT.kBlue)

	temp_hist_sig = sig_tree.Histo1D((f"{n}_sigHist", n, 200, sig_tree.Min(n).GetValue() / 5, sig_tree.Max(n).GetValue() / 5), n)
	temp_hist_sig.Scale(norm/N_sig, "height")

	temp_hist_sig.SetFillStyle(3007)

	temp_hist_sig.SetStats(False)
	temp_hist_sig.SetFillColor(ROOT.kRed)

	temp_hist_bkg.Draw("HIST")
	temp_hist_sig.Draw("SAME HIST")

	c.Update()

	c.SaveAs(f"test_data_dist_plots/{n}.png")


input("Enter")