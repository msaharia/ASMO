#!/usr/bin/env python

from __future__ import division, print_function, absolute_import
import os
import sys
sys.path.append('../src')
import ASMO
import numpy as np
import util
import cPickle

# model name
modelname = 'SAC'
model = __import__(modelname)

# result path
respath = '../../UQ-res/%s' % modelname
if not os.path.exists(respath):
    os.makedirs(respath)

# load parameter name and range
pf = util.read_param_file('%s.txt' % modelname)
bd = np.array(pf['bounds'])
print('bd')
print(bd)
nInput = pf['num_vars']
print('nInput')
print(nInput)
xlb = bd[:,0]
print('xlb')
print(xlb)
xub = bd[:,1]
print('xub')
print(xub)

# run ASMO
niter = 5
bestx, bestf, x, y = ASMO.optimization(model, nInput, xlb, xub, niter)

print('Optimum found by ASMO:')
print('bestx:')
print('bestf:')

# save results to bin file
with open('%s/SAC_ASMO.bin' % respath, 'w') as f:
    cPickle.dump({'bestx': bestx, 'bestf': bestf, 'x': x, 'y': y}, f)
