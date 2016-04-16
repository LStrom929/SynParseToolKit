# This program is used to find a median sentence length from a given directory of .txt files
# The median for the corpus (directory) is then a median of medians, each taken from single files
# Runs on Python 2.7+ (not 3)
#------------------------------------------------------------------------------------

import glob
from nltk import tokenize
import numpy as np
import sys  
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib.mlab as mlab

# encode for unusual characters in medical text
reload(sys) 
sys.setdefaultencoding('utf8')

# sequentially extract each file from given directory
glob_input = str(input("Please enter a directory of files to use: "))
filelist = glob.glob(glob_input)
terminate = False

while not terminate:
    median_list = []

    i = 0
    while i < len(filelist):
        
        file = filelist[i]
        with open(file, "rt") as ofile:
            rfile = ofile.read()
        
        tokenized_file = tokenize.sent_tokenize(rfile) # separate by sentences
        
        new_list = [] # this will be a list of lists of sentences split by words
        for elem in tokenized_file:
            sent = elem.split()
            new_list.append(sent)

        lengths_list = []
        for elem in new_list:
            length = len(elem)
            lengths_list.append(length)

        lengths_list.sort()

        median = np.median(np.array(lengths_list))
        median_list.append(median)
        
        i += 1

    overall_median = np.median(np.array(median_list))

    print "Overall median is: ", overall_median, " From", len(filelist), "files (and therefore medians!)"
    median_list = np.asarray(median_list)
    overall_median = np.asarray(overall_median)
    hist_input = str(raw_input("Would you like to see a histogram of the medians [y/n]?: "))
    while hist_input != 'y' and hist_input != 'n':
        print "[y/n] please"
        hist_input = str(raw_input("Would you like to see a histogram of the medians [y/n]?: "))

    if hist_input == 'y':
        # do a distribution with median_list
        # Remember that this distribution represents medians of medians!!!
        # So each x-value is a median of sentence length medians from one FILE
        
        overall_mean = np.mean(median_list)
        overall_std = np.std(median_list)
        
        plt.hist(median_list, bins=range(int(min(median_list)), int(max(median_list)) + 1, 1),normed=True)
        # curve = stats.norm.pdf(hist, overall_mean, overall_std)
        plt.xlim((min(median_list), max(median_list)))
        
        line = np.linspace(min(median_list), max(median_list),len(median_list))
        plt.plot(line, mlab.normpdf(line,overall_mean,overall_std)) # THIS NEEDS REPAIR
        
        plt.title("Medians of Median Sent Lengths")
        plt.xlabel("Sent Length")
        plt.ylabel("Frequency")
        plt.show()
    elif hist_input == 'n':
        terminate = True
     
        