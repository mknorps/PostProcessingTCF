# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: compute_stats.py
# Created by: gemusia
# Creation date: 12-01-2018
# Last modified: 15-01-2018 10:16:55
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def compute_stats(generator_function,files,*args):

    average = 0 
    try:
        average = sum(generator_function(files,*args))/len(files)

    except ZeroDivisionError:
        print("Empty argument - no files listed")

    return average


