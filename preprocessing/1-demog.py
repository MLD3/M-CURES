import json
import sparse
import pandas as pd
import numpy as np
import joblib

df_static = pd.read_csv('sample_input/demog.csv').set_index('hosp_id')
discretization_bins = json.load(open('metadata/demog/discretization.json', 'r'))
feature_names = json.load(open('metadata/demog/s_all.feature_names.json', 'r'))

cols_useful = list(discretization_bins.keys())
df_static = df_static[cols_useful]

##### FIDDLE
from FIDDLE_steps_2 import *
from FIDDLE_helpers import *

df = df_static
df_by_cols = [df[col] for col in df.columns]
out_0 = [smart_qcut_bins((x, discretization_bins[x.name])) for x in tqdm(df_by_cols, desc='pd.qcut')]
cols_data, dis_bins = zip(*out_0)
out = [dummify(z) for z in tqdm(cols_data, desc='dummify')]
df_features = pd.concat(out, axis=1).sort_index(axis=1)

# Drop any values='missing'
df_features = df_features.loc[:, [col for col in df_features.columns if 'missing' not in col]]

# Make sure same features
assert set(df_features.columns) <= set(feature_names)

df_features = df_features.reindex(columns=feature_names, fill_value=0)
sdf = df_features.astype(pd.SparseDtype(int, fill_value=0))
X_all = sparse.COO(sdf.sparse.to_coo())

sparse.save_npz('sample_output/out_demog/X_all.npz', X_all)
df_features[[]].to_csv('sample_output/out_demog/X_all.IDs.csv')

import sparse, json
s = sparse.load_npz('sample_output/out_demog/X_all.npz').todense()
cols = feature_names
df_s = pd.DataFrame(s, columns=cols)
df_s.index = df_static.index
df_s.to_csv('sample_output/out_demog/static-features.csv')
