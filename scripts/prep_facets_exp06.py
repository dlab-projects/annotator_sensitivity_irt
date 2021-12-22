"""Creates Facets specification from hate speech data.

Experiment 04: Remove non-quality raters, recode responses, and split up data
according to the target identity of the comment. Apply bias-interaction term."""
import numpy as np
import pandas as pd

from hatespeech import utils
from hatespeech.keys import items, race_to_col, annotator_race_to_col

# Define paths
exp = "06"
data_path = "~/data/hatespeech/clean_qualtrics_irt_rollout.feather"
rater_quality_path = "~/data/hatespeech/rater_quality_check.csv"
# Column names
comment_col = 'comment_id'
labeler_col = 'labeler_id'

# Read in hate speech data
data = pd.read_feather(data_path).rename(columns={'violence_phys': 'violence'})
# Remove all rows in which some item is missing
data = utils.filter_missing_items(data)
# Remove all rows in which the rater is not up to sufficient quality
rater_quality = pd.read_csv(rater_quality_path)
data = utils.filter_annotator_quality(data, rater_quality)
# Recode item responses
data = utils.recode_responses(
    data,
    insult={1: 0, 2: 1, 3: 2, 4: 3},
    humiliate={1: 0, 2: 0, 3: 1, 4: 2},
    status={1: 0, 2: 0, 3: 1, 4: 1},
    dehumanize={1: 0, 2: 0, 3: 1, 4: 1},
    violence={1: 0, 2: 0, 3: 1, 4: 1},
    genocide={1: 0, 2: 0, 3: 1, 4: 1},
    attack_defend={1: 0, 2: 1, 3: 2, 4: 3},
    hatespeech={1: 0, 2: 1})
# Only get comments targeting black / white people
data = data[(data[race_to_col['black']] == 1)
            | (data[race_to_col['white']] == 1)]
data['target_black'] = np.where(data[race_to_col['black']] == 1, 2, 1)
# Add annotator race
data['annotator_race'] = np.where(
    data[annotator_race_to_col['pacific_islander']] == 1, 5,
    np.where(
        data[annotator_race_to_col['middle_eastern']] == 1, 8,
        np.where(
            data[annotator_race_to_col['native_american']] == 1, 1,
            np.where(
                data[annotator_race_to_col['asian']] == 1, 2,
                np.where(
                    data[annotator_race_to_col['latinx']] == 1, 4,
                    np.where(
                        data[annotator_race_to_col['black']] == 1, 3,
                        np.where(
                            data[annotator_race_to_col['white']] == 1, 6, 7)))))))
# Item ID will support Facets spec
data['item_id'] = f'1-{len(items)}'

# Iterate over each racial group
data_path = f"exp{exp}.txt"
spec_path = f"exp{exp}_spec.txt"
scores_path = f"exp{exp}_scores"
output_path = f"exp{exp}_out.txt"

# Generate Facets input
facets = data[[comment_col, labeler_col, "target_black", "annotator_race", "item_id"] + items]
facets.to_csv(data_path, sep=',', header=False, index=False)

# Create strings for Facets specification
comment_ids = "=\n".join(facets[comment_col].drop_duplicates().values.astype('str'))
annotator_ids = "=\n".join(facets[labeler_col].drop_duplicates().values.astype('str'))
item_ids = "\n".join([f"{idx+1}={item}" for idx, item in enumerate(items)])

# Write Facets specification file
with open(spec_path, 'w') as spec:
    spec.write(
        f"Title = Facets Rollout Scaling\n"
        "Facets = 5\n"
        f"Model = ?, ?, ?B, ?B, #, R\n"
        "Noncenter = 1\n"
        "Positive = 1\n"
        "Arrange = N\n"
        "Subset detection = No\n"
        "Delements = 1N, 2N, 3N, 4N, 5N\n"
        f"Scorefile = {scores_path}\n"
        f"Output file = {output_path}\n"
        "CSV = Tab\n\n"
        "Labels =\n"
        "1,Comments\n"
        f"{comment_ids}=\n*\n"
        "2,Judges\n"
        f"{annotator_ids}=\n*\n"
        "3,Race\n"
        "1=white,0\n"
        "2=black,0\n"
        "*\n"
        "4,AnnotatorRace\n"
        "1=nativeamerican,0\n"
        "2=asian,0\n"
        "3=black,0\n"
        "4=latinx,0\n"
        "5=pacificislander,0\n"
        "6=white,0\n"
        "7=other,0\n"
        "8=middleeastern,0\n"
        "*\n"
        "5,Items\n"
        f"{item_ids}\n*\n\n"
        f"Data = {data_path}")
