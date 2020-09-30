# M-CURES

## Preprocessing

- The data is transformed from/into roughly three different formats. 

- Notebooks starting with "1" transform each of "Raw" demog/flow/meds/labs into the unified "Intermediate" format. 

- Notebooks starting with "2a" "2b" etc are FIDDLE code that transforms "Intermediate" to "Features". 

**Raw**
- See the specification document we previously sent out. The format can vary a lot depending on the different feature subsets. 


**Intermediate**

- with four columns: ID, t, variable_name, variable_value
    - ID: {hosp_id}-{window_id}, a particular 4h window for a particular hosp_id. 
    - t: time in minutes relative to the start of the current 4h window (a value between 0 and 240)
    - variable_name: e.g. heartrate
    - variable_value: e.g. 117

- This will be used as input to FIDDLE which outputs the features.

**Features**

- Each row corresponds to an ID

- Each column is a binary feature, corresponding to missingness, categories, or ranges of different variable_name.
