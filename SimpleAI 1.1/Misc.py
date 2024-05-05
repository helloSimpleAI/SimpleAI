#!/usr/bin/env python3

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def emptyFunc(img = None):
    return img

def setRange(x, x_min, x_max):
    tmp = x if x > x_min else x_min
    tmp = tmp if tmp < x_max else x_max
    return tmp
