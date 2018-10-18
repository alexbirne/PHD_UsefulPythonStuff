#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""ComparisonPlots.

Example:
"""

__author__ = "Alex Birnkraut, Vanessa Müller, Julian Wishahi"
__credits__ = ["Alex Birnkraut", "Vanessa Müller", "Julian Wishahi"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "LHCb Flavour Tagging PPWG"
__email__ = "lhcb-phys-flavour-tagging@cern.ch"
__status__ = "Production"

import os
import argparse, ConfigParser
import math
# from ROOT import gROOT, TFile, TTree, TCanvas, TH1D, TLatex, TLegend, TLegendEntry, TLine
from ROOT import *
import style


def create_general_dict(config):
    return {
        'label': config.get('general', 'label'),
        'output_dir': config.get('general', 'output_dir'),
        'separate_dirs': config.getboolean('general', 'separate_dirs')
    }


def create_input_dicts(config):
    input_secs = [ sec for sec in config.sections() if sec.startswith('input.')]
    input_dicts = []
    for input_sec in input_secs:
        file_name = config.get(input_sec, 'file')
        tree_name = config.get(input_sec, 'tree')
        tfile = TFile(file_name, "READ")
        if tfile is None:
            print("Could not find file " + file_name)
        ttree = tfile.Get(tree_name)
        if ttree is None:
            print("Could not open tree " + tree_name + " in file " + file_name)

        input_dict = {
            'name':   input_sec.lstrip('input.'),
            'file':   tfile,
            'tree':   ttree,
            'weight': config.get(input_sec, 'weight_branch'),
            'cut':    config.get(input_sec, 'cut'),
            'colour': config.getint(input_sec, 'colour'),
            'legend': config.get(input_sec, 'legend')
        }
        input_dicts.append(input_dict)
    return input_dicts


def create_plot_dicts(config, input_dicts):
    plot_secs  = [sec for sec in config.sections() if sec.startswith('plot.')]
    plot_dicts = []
    for plot_sec in plot_secs:
        x_range_min = config.getfloat(plot_sec, 'x_range_min')
        x_range_max = config.getfloat(plot_sec, 'x_range_max')
        if x_range_min >= x_range_max:
            print("Range definition for plot " + name + " is strange. Min >= Max.")
        cuts = {}
        binnings = {}
        branches = {}
        for input_data in input_dicts:
            input_name = input_data['name']
            cuts[input_name] = config.get(plot_sec, 'cut.' + input_name)
            binnings[input_name] = config.getint(plot_sec, 'binning.' + input_name)
            branches[input_name] = config.get(plot_sec, 'branch.' + input_name)

        plot_dict = {
                'name' :                plot_sec.lstrip('plot.'),
                'x_range_min':          x_range_min,
                'x_range_max':          x_range_max,
                'x_axis_unit':          config.get(plot_sec, 'x_axis_unit'),
                'x_axis_title':         config.get(plot_sec, 'x_axis_title'),
                'y_range_min':          config.getfloat(plot_sec, 'y_range_min'),
                'y_range_max_scale':    config.getfloat(plot_sec, 'y_range_max_scale'),
                'y_axis_log':           config.getboolean(plot_sec, 'y_axis_log'),
                'normalise':            config.getboolean(plot_sec, 'normalise'),
                'cuts':                 cuts,
                'branches':             branches,
                'binnings':             binnings
        }
        plot_dicts.append(plot_dict)
    return plot_dicts


def create_plots(general_dict, input_dicts, plot_dicts):
    for plot_dict in plot_dicts:
        canvas = TCanvas("canv", "canv", 2000, 1200)
        pad = canvas.cd()
        pad.SetPad(0.02, 0, 0.98, 0.98)
        pad.SetLeftMargin(0.14)
        pad.SetRightMargin(0.09)
        pad.SetBottomMargin(0.16)
        pad.SetTopMargin(0.06)
        pad.SetLogy(plot_dict['y_axis_log'])
        create_plot(general_dict, input_dicts, plot_dict, canvas)
        canvas.Destructor()


def create_plot(general_dict, input_dicts, plot_dict, canvas):
    tlegend = TLegend(0.18, 0.22, 0.4, 0.33)
    tlegend.SetTextFont(132)
    tlegend.SetTextSize(0.06)
    tlegend.SetEntrySeparation(0.)

    plot_name = plot_dict['name']
    hist_array = []
    for input_dict in input_dicts:
        input_name = input_dict['name']
        cut_complete = create_cut(input_dict['cut'], input_dict['weight'], plot_dict['cuts'][input_name])
        plot_hist(input_dict['tree'],
                  input_name,
                  plot_dict['branches'][input_name],
                  cut_complete,
                  plot_dict['binnings'][input_name],
                  plot_dict['x_range_min'],
                  plot_dict['x_range_max'],
                  plot_dict['x_axis_unit'],
                  plot_dict['x_axis_title'],
                  plot_dict['y_range_min'],
                  plot_dict['y_range_max_scale'],
                  plot_dict['normalise'],
                  input_dict['colour'],
                  input_dict['legend'],
                  hist_array,
                  tlegend)

    hist_array.sort(key=get_max, reverse=True)
    hist_array[0].Draw("E1")
    for hist in hist_array[1:]:
        hist.Draw("Same E1")

    # label generation
    labelarray = []
    label_x = 0.75
    label_y = 0.84
    label = TLatex(0, 0, general_dict['label'])
    xsize = label.GetXsize()
    if xsize > 0.25:
        label_x = 0.65 - (max(0.0, xsize - 0.25) * 0.8)
    label.SetX(label_x)
    label.SetY(label_y)
    label.SetTextSize(0.08)
    label.SetNDC()
    label.Draw()

    # ymin = hist_array[0].GetMinimum()
    # ymax = hist_array[0].GetMaximum()
    # line = TLine(1840,ymin,1840,ymax)
    # line.SetLineColor(2)
    # line.Draw("Same")
    # line2 = TLine(1900,ymin,1900,ymax)
    # line2.SetLineColor(2)
    # line2.Draw("Same")

    # gPad.RedrawAxis()

    # canvas.SetLogy(True)
    # tlegend.Draw()

    save_plot(canvas, plot_name, general_dict)
    canvas.Clear()


def save_plot(canvas, plot_name, general_dict):
    import os
    output_dir = general_dict['output_dir']
    if general_dict['separate_dirs']:
        output_dir = os.path.join(output_dir, plot_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    save_dir = os.path.join(output_dir, plot_name)

    canvas.SaveAs(save_dir + '.pdf')
    canvas.SaveAs(save_dir + '.tex')
    canvas.SaveAs(save_dir + '.C')


def plot_hist(tree, input_name, varname, cut, binning,
              x_range_min, x_range_max, x_unit, x_title,
              y_range_min, y_range_max_scale, drawnorm,
              color, legend_desc,
              hist_list, tlegend):

    hits_name = "hist" + input_name + varname
    hist = TH1D(hits_name, hits_name, binning, x_range_min, x_range_max)
    tree.Draw(varname + ">>" + hits_name, cut)


    if drawnorm:
        norm = hist.GetSumOfWeights()
        hist.Sumw2()
        hist.Scale(1. / norm)

    hist.SetLineColor(color)
    hist.SetMarkerColor(color)

    hist.GetXaxis().SetTitle(create_x_axis_label(x_title, x_unit))
    hist.GetYaxis().SetTitle(create_y_axis_label(x_range_min, x_range_max, binning, x_unit, drawnorm))

    hist.GetYaxis().SetTitleOffset(1.1)
    hist.SetMinimum(y_range_min)
    hist.SetMaximum(get_max(hist) * y_range_max_scale)
    hist.SetLabelSize(0.06, "y")
    hist.SetTitleSize(0.066, "y")

    hist_list.append(hist)
    tlegend.AddEntry(hist,legend_desc, 'ep')


def create_x_axis_label(x_title, x_unit):
    x_axis_title = x_title
    if x_unit:
        x_axis_title += " [" + x_unit + "]"
    return x_axis_title


def create_y_axis_label(x_range_min, x_range_max, binning, x_unit, drawnorm):
    bin_width_label = get_bin_width_label(x_range_min, x_range_max, binning)
    if x_unit:
       bin_width_label = "(" + bin_width_label +  " " + x_unit + ")"
    return_string = "Candidates / " + bin_width_label
    # return_string = "Candidates (arbitrary scale)"
    if drawnorm:
        return_string = "Candidates (arbitrary scale)"
    return return_string


def get_bin_width_label(x_range_min, x_range_max, binning):
    normbinwidth = (x_range_max - x_range_min) / binning
    if normbinwidth < 1:
      normbinwidth = round(normbinwidth, 3)
    elif normbinwidth < 10:
      normbinwidth = round(normbinwidth, 2)
    elif normbinwidth < 100:
      normbinwidth = round(normbinwidth, 1)
    else:
      normbinwidth = round(normbinwidth, 0)

    bin_width_label = 0
    if math.log10(normbinwidth) < 0:
      bin_width_label = '%.3f' % normbinwidth # taking the digit before the comma, the comma itself and three behind it
    elif math.log10(normbinwidth) < 1:
      bin_width_label = '%.2f' % normbinwidth # taking the digit before the comma, the comma itself and two behind it
    elif math.log10(normbinwidth) < 2:
      bin_width_label = '%.1f' % normbinwidth # taking the digits before the comma, the comma itself and one behind it
    else:
      bin_width_label = '%.0f' % normbinwidth
    return bin_width_label


def get_max(hist):
    """Get the maximum value of the histogram hist"""
    return hist.GetBinContent(hist.GetMaximumBin())


def create_cut(input_cut, weight_var, plot_cut):
    """Transform cuts and weight variables into a ROOT TTree->Draw compatible selection string"""
    cuts = [input_cut, plot_cut]
    cuts = filter(None, cuts)
    cuts = ['(' + cut + ')' for cut in cuts]
    and_comb = '&&'
    cut_complete = and_comb.join(cuts)
    if weight_var:
        if cut_complete:
            cut_complete = '(' + cut_complete + ')*(' + weight_var + ')'
        else:
            cut_complete = weight_var

    return cut_complete


def main(argv=None):

    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(description='compares two distributions by plotting them normalised')
    parser.add_argument('--Configfile', '-f', help='file name')
    args = parser.parse_args()

    config = ConfigParser.RawConfigParser()
    config.read(args.Configfile)

    # prepare input dictionaries
    general_dict = create_general_dict(config)
    input_dicts  = create_input_dicts(config)
    plot_dicts   = create_plot_dicts(config, input_dicts)

    # make ROOT silent
    gROOT.SetBatch(True)
    style.setLHCbStyle()

    create_plots(general_dict, input_dicts, plot_dicts)


if __name__ == "__main__":
    import sys
    sys.exit(main())
