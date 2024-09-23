import ROOT
import itertools
import numpy as np

class HistManager:

    def __init__(self, path=None):
        self.data = dict()
        if path is not None:
            self.load(path)

        self.weight = 1.0

        self.bins = dict()
        self.binned_histograms = dict()

    def set_weight(self, w):
        self.weight = w

    def set_bins(self, name, bins):
        if name in self.bins:
            print(f'Bins for {name} already defined as {bins}')
        else:
            self.bins[name] = bins

    def add_hist(self, name, nxbins, xmin, xmax, bins=None):
        self.data[name] = ROOT.TH1F(name, name, nxbins, xmin, xmax)
        self.data[name].Sumw2()

    def add_binned_hist(self, name, binning_vars, nxbins, xmin, xmax, xbins=None):

        self.binned_histograms[name] = {
            'binning_vars': binning_vars,
        }

        for binning_comb in itertools.product(*[ [ i for i in range(len(self.bins[var])) ] for var in binning_vars ]):
            hname = f'h__{name}'
            for var_name, var_bin in zip(binning_vars, binning_comb):
                hname += f'__{var_name}{var_bin}'

            self.add_hist(hname, nxbins, xmin, xmax, xbins)

    def fill_binned_hist(self, name, binning_vars, binning_values, value, weight=None):

        #binning_vars = self.binned_histograms[name]['binning_vars']

        bin_tag = ''
        for var_name, var_value in zip(binning_vars, binning_values):
            _bin = np.searchsorted(self.bins[var_name], var_value) - 1
            bin_tag += f'__{var_name}{_bin}'

        if isinstance(name, list):
            for n, v in zip(name, value):
                hname = f'h__{n}{bin_tag}'
                self.fill_hist(hname, v, weight)
        else:
            hname = f'h__{name}{bin_tag}'
            self.fill_hist(hname, value, weight)

    def add_hist2d(self, name, xbins, xmin, xmax, ybins, ymin, ymax):
        self.data[name] = ROOT.TH2F(name, name, xbins, xmin, xmax, ybins, ymin, ymax)
        self.data[name].Sumw2()

    def add_hist_profile(self, name, xbins, xmin, xmax, ymin, ymax):
        self.data[name] = ROOT.TProfile(name, name, xbins, xmin, xmax, ymin, ymax)
        self.data[name].Sumw2()

    def fill_hist(self, name, value, weight=None):
        if weight is not None:
            self.data[name].Fill(value, weight)
        else:
            self.data[name].Fill(value, self.weight)

    def fill_hist_2d(self, name, value_x, value_y, weight=None):
        if weight is not None:
            self.data[name].Fill(value_x, value_y, weight)
        else:
            self.data[name].Fill(value_x, value_y, self.weight)

    def fill_profile(self, name, value_x, value_y, weight=None):
        if weight is not None:
            self.data[name].Fill(value_x, value_y, weight)
        else:
            self.data[name].Fill(value_x, value_y, self.weight)

    def save(self, path):
        f = ROOT.TFile(path, 'recreate')
        f.cd()
        for name, hist in sorted(self.data.iteritems()):
            hist.Write(name)

    def load(self, path):
        f = ROOT.TFile.Open(path)
        for key in f.GetListOfKeys():
            name = key.GetName()
            self.data[name] = f.get(name)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __iter__(self):
        return self.data.iteritems()
