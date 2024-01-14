from aircraft.problem import *
import os
import pickle

problems = ['101', '102', '103', '201', '202', '203', '204', '205', '301', '302', '303', '304', '305', '401', '402', '403', '501', '502', '601', '901', \
            '131', '142', '143', '241', '222', '233', '244', '245', '341', '322', '333', '344', '345', '441', '422', '443', '541', '542', '641', '941']
levels = [0,1,2]
path_func = 'function/'

if not os.path.exists(path_func):
    os.makedirs(path_func)

for prob in problems:
    for level in levels:
        func = eval('HPA' + prob + '(n_div=4, level=' + str(level) + ', NORMALIZED=True)')
        with open(os.path.join(path_func , 'hpa' + prob + '-' + str(level) + '.pickle'), mode='wb') as f:
            pickle.dump(func, f)