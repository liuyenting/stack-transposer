# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 15:15:33 2016

@author: Andy Liu
"""

import argparse
import os        
import sys
import glob
import re
from libtiff import TIFFfile, TIFFimage

# Pattern of the target sorting sequence, *_stackXXXXX_*
seqPat = re.compile(r".*_stack([0-9]+)_.*")

def sortKey(it) :
    mat = seqPat.match(it)
    return int(mat.group(1))

def listFiles(d) :
    print('Search in "', d, '"...', sep='', end=' ')
    
    targetPath = os.path.join(d, '*_stack*_*.tif*')
    lst = glob.glob(targetPath)
    # Sort the files according to the stack ID.
    lst.sort(key=sortKey)
    
    print(len(lst), 'stacks found')    
    return lst
    
def transposeInit(dname, fname, prefix) :
    with TiffFile(fname) as tiff :
        ti = tiff.asarray()
        for pg in ti :
            
    ti = TIFFfile(fname)
    samples, sample_names = tiff.get_samples()
    # Create all the files by iterating through directories.
    for idx, img in enumerate(ti) :
        newfname = os.path.join(dname, prefix + str(idx))
        to = TIFFimage(data, description='')
        to = TIFF.open(newfname, 'w')
        to.write_image(img)
        to.close()
    ti.close()
        
def transpose(indir, outdir, prefix) :
    lst = listFiles(indir)
    
    transposeInit(indir, lst(0), prefix)
    #for p in lst(1:) :
    
def constructParser() :
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-p', '--prefix',
                        help='Prefix of transposed stacks, default to "layer_"',
                        default='layer_');
    parser.add_argument('-o', '--output',
                        help='Output directory, default to input directory')
    parser.add_argument('input', 
                        help='The directory that holds the stacks');   
    return parser
    
if __name__ == '__main__' :
    parser = constructParser()
    args = parser.parse_args()
    
    # Validate the folders.
    if not os.path.isdir(args.input) :
        print('Input is not a valid directory.')
        sys.exit(1)
    if not args.output :
        args.output = args.input
    elif os.path.isfile(args.output) :
        print('Output is not a valid directory.')
        sys.exit(1)
    elif os.path.exists(args.output) and os.listdir(args.output) :
        choice = input('Output directory is not empty. Continue? [Y/n] ') or 'y'
        if choice != 'Y' and choice != 'y' :
            sys.exit()
            
    transpose(args.input, args.output, args.prefix)