import ROOT

hist1 = ROOT.TH1F("MyHist", "TestTitle", 64, -4, 4)
hist1.fillRandom("gaus")
hist1.Draw()

# Add another diagram