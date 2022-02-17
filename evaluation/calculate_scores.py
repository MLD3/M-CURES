import pickle
import pandas as pd
import numpy as np
import scipy
import joblib

# A csv file to output scores in, change to any file
output_file = 'score.csv'


### Load necessary files

# Load the trained M-CURES model
print('Load Model')
models_dict = joblib.load('models_dict.joblib')
mcures_clfs = models_dict['M-CURES']

# Load the input data. The data should be formatted similar to the sample_cohort.csv. More information can be found in the README
print('Load Data')
df_cohort = pd.read_csv('sample_cohort.csv')
df_mcures = pd.read_csv('../preprocessing/sample_output/mcures.csv').set_index('ID')

test_hosp, test_window, test_y = df_cohort['hosp_id'], df_cohort['window_id'], df_cohort['y']
cohort_IDs = df_cohort.set_index('ID')[[]]


### Calculate scores

# Run each model of the ensemble on the data
eval_matrix = scipy.sparse.csr_matrix(cohort_IDs.join(df_mcures).values.astype(float))
all_y = np.array([clf.predict_proba(eval_matrix)[:,1] for clf in mcures_clfs])

# Average results over all 500 ensemble models 
y_scores = all_y.mean(0)

# Collect all scores and associate them with each patient and window
df_Yte_all = pd.DataFrame({'hosp_id': test_hosp, 'window_id': test_window, 'y_score': y_scores})


# Save scores to output file
df_Yte_all.to_csv(output_file)
print('Scores saved at {}'.format(output_file))
