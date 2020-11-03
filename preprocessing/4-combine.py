import json
import sparse
import pandas as pd
import numpy as np
import scipy.sparse
import joblib

def load_IDs(fname):
    IDs = pd.read_csv(fname, header=0, names=['ID'])
    IDs.index.name = 'i'
    IDs = IDs.reset_index()
    return IDs

def _get_feature_set(df, X_ALL, IDs_ALL):
    IDs = df.set_index('ID')[[]]
    idx = IDs.join(IDs_ALL.set_index('ID')).astype(float)
    X = [X_ALL[int(i),:] if not np.isnan(i) else sparse.zeros(X_ALL.shape[1]) for i in idx.values]
    return sparse.stack(X)

def get_features(df, feature_sets):
    features = []
    feature_names = []
    if 'demog' in feature_sets:
        X_d = df.set_index('hosp_id')[['ID']].join(df_demog).reset_index(drop=True).set_index('ID').loc[df['ID']]
        X_d = sparse.as_coo(X_d.values)
        features.append(X_d)
        feature_names.append(names_demog)
        print('demog - Done')
    if 'vitals' in feature_sets:
        X_v = _get_feature_set(df, X_vitals, IDs_vitals)
        features.append(X_v)
        feature_names.append(names_vitals)
        print('vitals - Done')
    if 'meds' in feature_sets:
        X_m = _get_feature_set(df, X_meds, IDs_meds)
        features.append(X_m)
        feature_names.append(names_meds)
        print('meds - Done')
    if 'labs' in feature_sets:
        X_l = _get_feature_set(df, X_labs, IDs_labs)
        features.append(X_l)
        feature_names.append(names_labs)
        print('labs - Done')
    if 'flow' in feature_sets:
        print('flow', end='')
        X_f = _get_feature_set(df, X_flow, IDs_flow)
        features.append(X_f)
        feature_names.append(names_flow)
        print(' - Done')
    X = sparse.concatenate(features, axis=1).tocsr()
    feature_names = sum(feature_names, [])
    return X, np.array(feature_names)


df_demog = pd.read_csv('sample_output/out_demog/static-features.csv').set_index('hosp_id')
names_demog = list(df_demog.columns)
print('demog - Loaded')

X_vitals = sparse.load_npz('sample_output/out_vitals/X_all.npz')
IDs_vitals = load_IDs('sample_output/out_vitals/X_all.IDs.csv')
names_vitals = json.load(open('metadata/vitals/X_all.feature_names.json', 'r'))
print('vitals - Loaded')

X_meds = sparse.load_npz('sample_output/out_meds/X_all.npz')
IDs_meds = load_IDs('sample_output/out_meds/X_all.IDs.csv')
names_meds = json.load(open('metadata/meds/X_all.feature_names.json', 'r'))
print('meds - Loaded')

X_labs = sparse.load_npz('sample_output/out_labs/X_all.npz')
IDs_labs = load_IDs('sample_output/out_labs/X_all.IDs.csv')
names_labs = json.load(open('metadata/labs/X_all.feature_names.json', 'r'))
print('labs - Loaded')

X_flow = sparse.load_npz('sample_output/out_flow/X_all.npz')
IDs_flow = load_IDs('sample_output/out_flow/X_all.IDs.csv')
names_flow = json.load(open('metadata/flow/X_all.feature_names.json', 'r'))
print('flow - Loaded')

df_cohort = pd.read_csv('sample_input/windows_map.csv')
X, names = get_features(df_cohort, ['demog', 'vitals', 'meds', 'labs', 'flow'])
df_features = pd.DataFrame(X.todense(), columns=names, index=df_cohort['ID'])
pd.Series(names).rename('feature_name').to_csv('./sample_output/feature_names.csv', index=False)

## Full feature matrix
joblib.dump(df_features, 'sample_output/full.joblib')

## Baseline features
baseline_cols = pd.read_csv('metadata/Baseline_Feature_Names.txt', sep='\t', header=None)[0].values
df_baseline = df_features[baseline_cols]
df_baseline.to_csv('sample_output/baseline.csv')

## M-CURES (lite)
mcures_cols = pd.read_csv('metadata/MCURES_Feature_Names.txt', sep='\t', header=None)[0].values
df_mcures = df_features[mcures_cols]
df_mcures.to_csv('sample_output/mcures.csv')
