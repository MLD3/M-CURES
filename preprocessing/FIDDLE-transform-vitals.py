from config import *
import pickle
import pandas as pd
import numpy as np
import time
import os

import argparse
from helpers import str2bool

parser = argparse.ArgumentParser(description='')
parser.add_argument('--T',               type=float,   required=True)
parser.add_argument('--dt',              type=float,   required=True)
parser.add_argument('--theta_1',         type=float,   default=0.001)
parser.add_argument('--theta_2',         type=float,   default=0.001)
parser.add_argument('--theta_freq',      type=float,   default=1.0)
parser.add_argument('--stats_functions', nargs='+',    default=['min', 'max', 'mean'])
parser.add_argument('--binarize',        type=str2bool, default=True, nargs='?', const=True)

parser.add_argument('--data_path',       type=str,     required=True)
parser.add_argument('--input_fname',     type=str,     required=False)
parser.add_argument('--population',      type=str,     required=True)
parser.add_argument('--N',               type=int,     required=False)
parser.add_argument('--Ds',              nargs='+',    type=int)

parser.add_argument('--no_prefilter',    dest='prefilter',  action='store_false')
parser.add_argument('--no_postfilter',   dest='postfilter', action='store_false')
parser.set_defaults(prefilter=True, postfilter=True)

args = parser.parse_args([
    "--data_path=./out_vitals/", 
    "--input_fname=./data_input/vitals.p", 
    "--population=./data_input/pop.csv", 
    "--T=240", "--dt=240", 
    "--no_prefilter", "--no_postfilter", "--theta_freq=1",
    "--stats_functions", 'min', 'max', 'mean',
])
args.variables = sorted(pd.read_csv('/data/covid/process_data/FIDDLE_2018-2019/out_vitals/value_types.csv')['variable_name'])
args.variables_num_freq = ['respiratoryrate', 'heartrate', 'temperature', 'sbp', 'dbp', 'spo2']

#########
data_path = args.data_path
if not data_path.endswith('/'):
    data_path += '/'

population = args.population
T = int(args.T)
dt = args.dt
theta_1 = args.theta_1
theta_2 = args.theta_2
theta_freq = args.theta_freq
stats_functions = args.stats_functions
binarize = args.binarize

df_population = pd.read_csv(population).set_index('ID')
N = args.N or len(df_population)
df_population = df_population.iloc[:args.N]
L = int(np.floor(T/dt))

args.df_population = df_population
args.N = N
args.L = L
args.parallel = parallel

if args.input_fname and os.path.isfile(args.input_fname):
    input_fname = args.input_fname
    if input_fname.endswith('.p' or '.pickle'):
        df_data = pd.read_pickle(input_fname)
    elif input_fname.endswith('.csv'):
        df_data = pd.read_csv(input_fname)
    else:
        assert False
else:
    raise NotImplementedError

if df_data['ID'].isnull().sum():
    print('Some IDs are NULL')
    df_data = df_data.dropna(subset=['ID'], axis=0)

##########
from steps_2 import *

print('Input data file:', input_fname)
print()
print('Input arguments:')
print('    {:<6} = {}'.format('T', T))
print('    {:<6} = {}'.format('dt', dt))
print('    {:<6} = {}'.format('\u03B8\u2081', theta_1))
print('    {:<6} = {}'.format('\u03B8\u2082', theta_2))
print('    {:<6} = {}'.format('\u03B8_freq', theta_freq))
print('    {:<6} = {} {}'.format('k', len(stats_functions), stats_functions))
print('{} = {}'.format('binarize', {False: 'no', True: 'yes'}[binarize]))
print()
print('N = {}'.format(N))
print('L = {}'.format(L))
print('', flush=True)

#######
df_data = df_data[df_data['variable_name'].isin(args.variables)]
df_time_series = df_data

print_header('2-B) Transform time-dependent data', char='-')
dir_path = data_path + '/'
start_time = time.time()

# Create NxLxD^ table
df_time_series, dtypes_time_series = transform_time_series_table(df_time_series, args)
print('Time elapsed: %f seconds' % (time.time() - start_time), flush=True)

##############
joblib.dump(dtypes_time_series, args.data_path + 'dtypes_time_series.joblib')
joblib.dump(df_time_series, args.data_path + 'df_time_series.joblib')
##############
