set -euxo pipefail

mkdir -p sample_output/out_demog
mkdir -p sample_output/out_vitals
mkdir -p sample_output/out_meds
mkdir -p sample_output/out_labs
mkdir -p sample_output/out_flow

python '1-demog.py'

python '2-meds.py'
python '2-labs.py'
python '2-flow.py'

python '3-vitals.py'

python '4-combine.py'
