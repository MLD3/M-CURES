# M-CURES

## Usage
- Refer to `requirements.txt` for the necessary pip packages. 
- **preprocessing**: Run `./run.sh`.
- **preprocessing_notebooks**: alternatively, run the notebooks in alphanumeric order. 
- **evaluation**: Run the `Eval.ipynb` notebook. 

## Input
An example usage of the pipeline is provided with fake input data in `preprocessing/sample_input` and `evaluation/sample_cohort.csv`. The easiest way to use the code is to create local copies of `preprocessing` -> `preprocessing_UM` and `evaluation` -> `evaluation_UM` and replace the input files with real data. Please refer to the sample input files (and descriptions below) for formatting requirements. 


### Cohort specification
These will be streamlined and cleaned up in a future version. 
- `windows_map.csv` contains all 4h windows for all `hosp_id`s. 
    - hosp_id column is the unique identifier for the encounter
    - window_id column is the index of 4h windows for the current encounter
    - ID column is "{hosp_id}-{window_id}"
- `windows.csv` has the same content as the `ID` column in `windows_map.csv`
- `sample_cohort.csv` is used by `Evaluation_UseCase1.ipynb`: predicting composite outcome that happens within the first 5 days. It has the same `ID`, `hosp_id`, and `window_id` columns as in `windows_map.csv`, and it contains an additional column `y` specifying the outcome label. The labels "y" for each window are defined as follows: 
    - If a patient encounter experiences the outcome, then windows after the outcome window are not used for prediction and should not be included. Only windows before the outcome window are included and they have a label of 1. 
    - If a patient does not have an outcome then all of their windows have a label of 0, and we only include up to the first 30 windows (first 5 days). 
    
    Every encounter should have no more than 30 windows. 
    
- `sample_cohort_outcome_past_2days.csv` is used by `Evaluation_UseCase2.ipynb`: predicting composite outcome that happens after 48h using the first 48h data. It has the same format as `sample_cohort.csv`, except it only contains encounters who have the outcome after two days, and the `y` label specifies if the outcome occurs _ever_ (rather than within the first 5 days). Every encounter should have exactly 12 windows (48h worth of data). 


### Data
For details on the expected values of each variable, please refer to `preprocessing/metadata/out_*/{discretization|feature_names}.json`. 

- `demog.csv` contains three columns:
    - age_value: numeric
    - sex_value: ['M', 'F']
    - race_value: 
        - "African American"
        - "American Indian or Alaska Native"
        - "Asian"
        - "Caucasian"
        - "Native Hawaiian and Other Pacific Islander"
        - "Other"
        - "Patient Refused"
        - "Unknown"

The other input data files all have four columns: ['ID', 't', 'variable_name', 'variable_value']. 
- The `ID` column specifies a 4h window of a specific encounter and should be contained in the `windows_map.csv` file. 
- The `t` column is measured in minutes relative to the start of the current 4h window. 

Below are the expected `variable_name`s in each file:
- `vitals.csv`
    - heartrate
    - temperature
    - sbp
    - dbp
    - respiratoryrate
    - spo2
- `flow.csv`: (note the underscore prefix)
    - '_307928' for "O2 flow rate"
    - '_313030' for "Pulse Oximetry type"
    - '_314689' for "BP: Patient Position"
    - '_355444' for "Head of Bed Position"
- `labs.csv`
    - pH (Ven Blood Gas): '81723_value' and '81723_hilonormal_flag'
    - pCO2 (Art Blood Gas): '84066_value' and '84066_hilonormal_flag'
    - ~~Hct (Art Blood Gas): '81799_value' and '81799_hilonormal_flag'~~
- `meds.csv`
    - currently none supported
