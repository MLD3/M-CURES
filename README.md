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
- `sample_cohort.csv` is the same as `windows_map.csv`, except it contains an additional column `y` specifying the outcome label. 
- `sample_cohort_outcome_past_2days.csv` is the same as `sample_cohort.csv`, except it only contains individuals who have the outcome after two days, and the `y` label specifies if the outcome occurs _ever_ (rather than within the first 5 days). 


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
