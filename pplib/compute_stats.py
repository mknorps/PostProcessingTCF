# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: compute_stats.py
# Created by: gemusia
# Creation date: 12-01-2018
# Last modified: 12-01-2018 09:46:30
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def compute_stats(generator_function,files):

    average = 0 
    try:
        average = sum(generator_function(files))/len(files)

    except ZeroDivisionError:
        print("Empty argument - no files listed")

    return average


