# M-CURES

M-CURES is a risk stratification model to predict clinical deterioration in hospitalized COVID-19 patients developed in response to the pandemic. Our objective was to create a simple and and transferable machine learning model using demographic (personal characteristic) and clinical variables from electronic health record data. Through the use of a novel paradigm for model development and code sharing, including both a data-driven and clinician-driven feature selection technique, M-CURES was built at a single institution, and achieved strong internal and external validation results across 13 medical centers in the United States. The model was validated in both detecting patients at risk of clinical deterioration, as well as detecting patients who were low-risk and could potentially be safely discharged. Our full paper is available at: https://doi.org/10.1136/bmj-2021-068576.

To assist other institutions in the validation and use of this model, all code and documentation are available here. 

If you use M-CURES in your research, please cite the following publication:
```
@article{MCURES,
    author = {Kamran, Fahad and Tang, Shengpu and Ötleş, Erkin and McEvoy, Dustin S and Saleh, Sameh N and Gong, Jen and Li, Benjamin Y and Dutta, Sayon and Liu, Xinran and Medford, Richard J and Valley, Thomas S and West, Lauren R and Singh, Karandeep and Blumberg, Seth and Donnelly, John P and Shenoy, Erica S and Ayanian, John Z and Nallamothu, Brahmajee K and Sjoding, Michael W and Wiens, Jenna},
    title = "{Early identification of patients admitted to hospital for covid-19 at risk of clinical deterioration: model development and multisite external validation study}",
    journal = {The BMJ},
    publisher = {BMJ Publishing Group Ltd},
    year = {2022},
    volume = {376},
    doi = {10.1136/bmj-2021-068576},
}
```


## Usage
- Refer to `requirements.txt` for the necessary pip packages. 
- **preprocessing**: Run `./run.sh`.
- **evaluation**: Run the `Evaluation_Primary.ipynb` and `Evaluation_Secondary.ipynb` notebook to evaluate M-CURES. To save model predictions for a set of input data, run `calculate_score.py`.  

## Input
An example usage of the pipeline is provided with dummy input data in `preprocessing/sample_input` and `evaluation/sample_cohort.csv`. The easiest way to use the code is to create local copies of `preprocessing` -> `preprocessing_UM` and `evaluation` -> `evaluation_UM` and replace the input files with real data. Please refer to the sample input files (and descriptions below) for formatting requirements. 


### Cohort specification
- `windows_map.csv` contains all 4h windows for all `hosp_id`s. 
    - hosp_id column is the unique identifier for the encounter
    - window_id column is the index of 4h windows for the current encounter
    - ID column is "{hosp_id}-{window_id}"
- `windows.csv` has the same content as the `ID` column in `windows_map.csv`
- `sample_cohort.csv` is used by `Evaluation_Primary.ipynb`: predicting composite outcome that happens within the first 5 days. It has the same `ID`, `hosp_id`, and `window_id` columns as in `windows_map.csv`, and it contains an additional column `y` specifying the outcome label. The labels "y" for each window are defined as follows: 
    - If a patient encounter experiences the outcome, then windows after the outcome window are not used for prediction and should not be included. Only windows before the outcome window are included and they have a label of 1. 
    - If a patient does not have an outcome then all of their windows have a label of 0, and we only include up to the first 30 windows (first 5 days). 
    
    Every encounter should have no more than 30 windows. 
    
- `sample_cohort_outcome_ever_past_2days.csv` is used by `Evaluation_Secondary.ipynb`: predicting composite outcome that happens after 48h using the first 48h data. It has the same format as `sample_cohort.csv`, except it only contains encounters who have the outcome after two days, and the `y` label specifies if the outcome occurs _ever_ (rather than within the first 5 days). Every encounter should have exactly 12 windows (48h worth of data). 


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
        - "Intermittent"
        - "Continuous"
    - '_314689' for "BP: Patient Position"
        - "Lying"
        - "Sitting"
        - "Standing"
    - '_355444' for "Head of Bed Position"
        - "HOB at 15 degrees"
        - "HOB at 30 degrees"
        - "HOB at 45 degrees"
        - "HOB at 60 degrees"
        - "HOB at 90 degrees"
        - "HOB flat (medical condition)"
        - "Reverse Trendelenberg"
        - "other (see comments)"
- `labs.csv`
    - pH (Ven Blood Gas): '81723_value' and '81723_hilonormal_flag'
    - pCO2 (Art Blood Gas): '84066_value' and '84066_hilonormal_flag'
- `meds.csv`
    - currently none supported
