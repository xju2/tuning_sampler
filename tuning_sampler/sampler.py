#!/usr/bin/env python
from __future__ import print_function

import json
import os
from functools import reduce

import numpy as np
import pandas as pd

import pyDOE2 as pyDOE


from tuning_sampler.parameter import Parameter

def least_runs(n):
    # n is the number of parameters
    # return number of coefficient to be fitted
    return 1 + n + n * (n + 1) / 2

class TuningSampler(object):
    """
    Manage tuned prameters and sampling of these parameters
    """
    def __init__(self, json_file):
        # avoid any duplicated variables from the input
        # two variables are the same, if they share the
        # same name
        self.para_list = set([])

        data = json.load(open(json_file))
        for value in data["variables"]:
            self.para_list.add(Parameter(**value))

        self.DOE = data.get("DOE", "one-to-one").lower()
        print("Try DOE:", self.DOE)

        self.summary()

    def minimum_runs_for_Prof(self):
        return least_runs(len(self.para_list))

    def runs_from_DOE(self):
        return 1

    def summary(self):
        print("\nBegin of parameter summary")
        print("  Design of Exp.:", self.DOE)
        print("  Total parameters: {}".format(len(self.para_list)))
        for para in sorted(self.para_list, key=lambda para: para.id_):
            print("\t", para)

        print("End of parameter summary")

    def append_factors(self, para, new_list):
        if len(new_list) > 0:
            para.run_values = para.values * reduce(lambda x, y: x * y, [len(z.values) for z in new_list])
        else:
            para.run_values = para.values

    def append_one2one(self, para):
        """use the values provided by the parameter itself.
        The ones with shorter value-list are filled by their nominal values
        """
        para.run_values = para.values + [para.nominal] * (self.max_len - len(para.values))

    def generate(self, out_name='parameters.csv'):
        if os.path.exists(out_name):
            self.df = pd.read_csv(out_name)
        else:
            doe_option = self.DOE
            if doe_option == "one-to-one":
                self.max_len = max([len(para.values) for para in self.para_list])
                map(self.append_one2one, self.para_list)

            elif doe_option == "factorial":
                index_array = pyDOE.fullfact(np.array([len(para.values) for para in self.para_list], dtype=np.int32))
                for ip, para in enumerate(self.para_list):
                    para.run_values = [para.values[int(x)] for x in index_array[:, ip]]

            elif "lhs" in doe_option:
                nsamples = int(doe_option.split(',')[1])
                scales = 5
                frac_array = pyDOE.lhs(len(self.para_list), samples=nsamples)   # CDF values for norm(0, 1)
                for ip, para in enumerate(self.para_list):
                    para.run_values = [round(para.min_val + x * (para.max_val - para.min_val), scales) for x in frac_array[:, ip]]
            else:
                print("I do nothing.")

            data = dict([(para.nickname, para.run_values) for para in self.para_list])
            self.df = pd.DataFrame(data=data)
            self.df.to_csv(out_name, index=False)
        print("\n****Generated List of Parameters***")
        print(self.df.head())
        print("\n")
        return self.df.shape[0]


    def get_config(self, irun):
        return "\n".join([para.config(self.df[para.nickname].iloc[irun])
                          for para in self.para_list if para.type_ == "pythia"])

    def get_tune(self, irun):
        return "\n".join([para.prof_config(self.df[para.nickname].iloc[irun]) for para in self.para_list])

    def update_nickname(self, detector_hists):
        for para in self.para_list:
            if para.type_ == "pythia":
                continue
            hist2D = detector_hists.get(para.name, None)
            if hist2D is not None:
                bin_2d = hist2D.binIndexAt(para.other_opt['eta'], para.other_opt['pT'])
                para.nickname = para.nickname + "_bin" + str(bin_2d)

    def update_detector(self, irun, detector_hists):
        new_hists = {}
        for key, value in detector_hists.iteritems():
            new_hists[key] = value.clone()

        for para in self.para_list:
            if para.type_ == "pythia":
                continue

            hist2D = new_hists.get(para.name, None)
            if hist2D is not None:
                bin_2d = hist2D.binIndexAt(para.other_opt['eta'], para.other_opt['pT'])
                # print("INFO: ",hist2D.bin(bin_2d).volume, hist2D.bin(bin_2d).height)
                # print("BIN Index: ", bin_2d)
                hist2D.fillBin(bin_2d, -1 * hist2D.bin(bin_2d).volume)
                hist2D.fillBin(bin_2d, self.df[para.nickname].iloc[irun])
                # print "After: ",hist2D.bin(bin_2d).volume, hist2D.bin(bin_2d).height
                # para.nickname = para.nickname+"_bin"+str(bin_2d)
                # print "bin index: ", hist2D.binIndexAt(para.other_opt['eta'], para.other_opt['pT'])
                # print "set to: ", self.df[para.nickname].iloc[irun]
            else:
                print(para.name, "is not in detector configuration")

        return new_hists

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(sys.argv[0], " json")
        exit(1)

    print(least_runs(1))
    print(least_runs(5))
    print(least_runs(6))
    print(least_runs(10))
    print(least_runs(100))
    print(least_runs(500))
    print(least_runs(1000))

    # sys.exit(0)
    tune = TuningSampler(sys.argv[1])

    tune.generate()
    irun = 0
    while irun < 1:
        try:
            print("--------begin config------------")
            print(tune.get_config(irun))
            print("--------end config------------\n")
            print("--------begin tune------------")
            print(tune.get_tune(irun))
            print("--------end tune------------\n")
        except IndexError:
            break
        irun += 1
