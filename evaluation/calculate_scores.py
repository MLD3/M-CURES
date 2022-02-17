import pickle
import pandas as pd
import numpy as np
import scipy
import joblib

# Where to save scores
output_file = 'score.csv'

print('Load Model')
models_dict = joblib.load('models_dict.joblib')
mcures_clfs = models_dict['M-CURES']


print('Load Data')
df_cohort = pd.read_csv('sample_cohort.csv')
test_hosp, test_window, test_y = df_cohort['hosp_id'], df_cohort['window_id'], df_cohort['y']
cohort_IDs = df_cohort.set_index('ID')[[]]

df_mcures = pd.read_csv('../preprocessing/sample_output/mcures.csv').set_index('ID')


### Calculate scores

eval_matrix = scipy.sparse.csr_matrix(cohort_IDs.join(df_mcures).values.astype(float))
all_y = np.array([clf.predict_proba(eval_matrix)[:,1] for clf in mcures_clfs])

y_scores = all_y.mean(0)
df_Yte_all = pd.DataFrame({'hosp_id': test_hosp, 'window_id': test_window, 'y_score': y_scores})


df_Yte_all.to_csv(output_file)
print('Scores saved at {}'.format(output_file))
