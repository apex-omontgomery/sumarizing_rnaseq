#!/usr/bin/python
"""
Run DESeq and EdgeR
"""

import os,sys,re,csv
import numpy as np
from htsint import run_subprocess


class Associative():
    """
    A generic class
    """

    def __init__(self):
        """
        Constructor

        """

    def create_filtered(self, countsPath):
        if not os.path.exists(countsPath):
            raise Exception("Cannot find counts path")

        filteredCountsPath = re.sub("\.csv","-filtered.csv",countsPath)
        fid1 = open(countsPath,'r')
        fid2 = open(filteredCountsPath,'w')
        reader = csv.reader(fid1)
        writer = csv.writer(fid2)
        header = next(reader)
        writer.writerow(header)

        for linja in reader:
            if np.array([float(i) for i in linja[1:]]).sum() > 1:
                writer.writerow(linja)
        fid1.close()
        fid2.close()
        return filteredCountsPath

    def run_deseq(self,countsPath,outFile):
        cmd = "Rscript runDESeq.R %s %s"%(countsPath,outFile)
        print("running...\n%s"%cmd)
        run_subprocess(cmd)

if __name__ == "__main__":

    ## specify the locations
    homeDir = os.path.join("..")
    readsDir = os.path.join(homeDir, "reads")

    featuresDir = os.path.join(homeDir,"examples", "pieris")
    countsPath = os.path.join(featuresDir,"data", "est_counts.csv")
    outDirectory = os.path.join(featuresDir, "results")
    outFile = os.path.join(outDirectory, "deseq.csv")

    # check if results directory exists, if !exist create one
    try:
        os.stat(outDirectory)
    except:
        os.mkdir(outDirectory)


    associative = Associative()
    filteredCountsPath = associative.create_filtered(countsPath)
    associative.run_deseq(filteredCountsPath,outFile)
