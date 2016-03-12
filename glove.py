import annoy
import time
import sys
import random
import operator
import numpy as np
import sklearn.decomposition
import json



phase = None
startTime = None


def logger(*ss):
    s = " ".join(map(str,ss))
    sys.stderr.write(s+"\n")


def start(s):
    global startTime
    global phase
    phase = s
    logger(phase+".")
    startTime = time.clock()


def end(s=None):
    global startTime
    global phase
    if s is not None:
        phase = s
    endTime = time.clock()
    logger(phase,"finished in",endTime-startTime,"seconds.")


def read(f):
    m = {}
    words = []
    d = None
    errorCount = 0
    for l in f:
        a = l.strip("\n").split(" ")
        try:
            w = a[0].decode("utf-8")
        except:
            errorCount +=1
            continue
        words.append(w)
        v = map(float, a[1:])
        if d is not None:
            assert d==len(v)
        d = len(v)
        m[w] = v
   return m, words, d