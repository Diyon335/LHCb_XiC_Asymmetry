import ROOT


filename = "B2HHH_MagnetUp.root"

df = ROOT.RDataFrame("DecayTree", filename)

P_tot_str = "+".join(["pow("+f"+".join([f"H{i}_P{j}" for i in range(1, 4)])+", 2)" for j in ["X", "Y", "Z"]])

df = df.Define("P_tot_sq", P_tot_str)

columns = df.GetColumnNames()

print(len(columns))

# num_events = df.Count().GetValue()

# H1_ProbK > 0.75 && H2_ProbPi > 0.75 && H3_ProbPi > 0.75) || \
# H2_ProbK > 0.75 && H1_ProbPi > 0.75 && H3_ProbPi > 0.75) || \
# H3_ProbK > 0.75 && H2_ProbPi > 0.75 && H1_ProbPi > 0.75)) && \


# filter_str = "((H1_ProbPi > H1_ProbK && H2_ProbK > H2_ProbPi && H3_ProbK > H3_ProbPi &&\
# H1_ProbPi > 0.75 && H2_ProbK > 0.75 && H3_ProbK > 0.75) ||\
# (H2_ProbPi > H2_ProbK && H1_ProbK > H1_ProbPi && H3_ProbK > H3_ProbPi &&\
# H2_ProbPi > 0.75 && H2_ProbK > 0.75 && H3_ProbK > 0.75) ||\
# (H3_ProbPi > H3_ProbK && H2_ProbK > H2_ProbPi && H1_ProbK > H1_ProbPi &&\
# H3_ProbPi > 0.75 && H2_ProbK > 0.75 && H3_ProbK > 0.75)) &&\
# (H1_isMuon == false && H2_isMuon == false && H3_isMuon == false)"

# def get_collision(df):

# 	return df.Filter(filter_str, "The data belongs to a KKP collision")

# df2 = get_collision(df)
# df3 = df.Filter("!(" + filter_str + ")", "The data is background signal")

# df_label = [[df2, "signal"], [df3, "background"]]

# for d, s in df_label:
# 	print(f"Number of datapoints in the {s} signal: {d.Count().GetValue()}")
# 	d.Snapshot("Events", f"KKP_{s}.root", columns)

# report = df2.Report()
# report.Print()
