#!/usr/bin/python
"""
Run DESeq and EdgeR
"""

import os,sys,re,csv
import numpy as np
import subprocess


class Associative():
    """
    A generic class
    """

    def __init__(self):
        """
        Constructor

        """

    def run_subprocess(self,cmd):
        proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        try:
            outs, errs = proc.communicate(timeout=22000)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()

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
        self.run_subprocess(cmd)

if __name__ == "__main__":

    ## specify the locations
    homeDir = os.path.join("..")
    readsDir = os.path.join(homeDir, "reads")

    parentDir = os.path.join(homeDir,"examples", "pieris")
    countsPath = os.path.join(parentDir,"data", "est_counts.csv")
    outDirectory = os.path.join(parentDir, "results")
    outFile = os.path.join(outDirectory, "deseq.csv")

    # check if results directory exists, if !exist create one
    if not os.path.exists(outDirectory):
        os.mkdir(outDirectory)


    associative = Associative()
    filteredCountsPath = associative.create_filtered(countsPath)
    associative.run_deseq(filteredCountsPath,outFile)
