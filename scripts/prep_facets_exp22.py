"""Runs Facets Scaling Experiment 22.

Experiment 22:
    - Annotator/target facet interaction term.
    - Use the streamlined dataset
    - Filter out missing ratings
    - Filter out by rater quality
    - Recode responses
    - Bias-interaction term between target race and annotator
    - Comments are non-centered
    - Item difficulties are anchored to preprint values.
"""
import numpy as np
import pandas as pd

from hatespeech import keys, utils

# Define paths
exp = "22"
data_path = "~/data/hatespeech/unfiltered_ratings.feather"
rater_quality_path = "~/data/hatespeech/rater_quality_check.csv"
# Column names
comment_col = 'comment_id'
labeler_col = 'labeler_id'
# Facets specification file inputs
title = "Facets Rollout Scaling"
# Comment, Labeler, Race, Item
model = "?, ?B, ?B, #, R"
noncenter = "1"

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
data = data[data['target_race_white'] | data['target_race_black']]
data = data[data[keys.target_race_cols].sum(axis=1) == 1]
data['target_race'] = np.where(data['target_race_white'], 1, 2)

# Item ID will support Facets spec
data['item_id'] = f'1-{len(keys.items)}'

# Iterate over each racial group
data_path = f"exp{exp}.txt"
spec_path = f"exp{exp}_spec.txt"
scores_path = f"exp{exp}_scores"
output_path = f"exp{exp}_out.txt"

# Generate Facets input
facets = data[[comment_col, labeler_col, "target_race", "item_id"] + keys.items]
facets.to_csv(data_path, sep=',', header=False, index=False)

# Create strings for Facets specification
comment_ids = "=\n".join(facets[comment_col].drop_duplicates().values.astype('str'))
annotator_ids = "=\n".join(facets[labeler_col].drop_duplicates().values.astype('str'))
item_anchors = [-2.62, -2.26, -0.94, 0.63, -0.51, 0.61, 2.22, 3.11, -1.10, 0.86]
item_ids = "\n".join([f"{idx+1}={item},{item_anchors[idx]}"
                      for idx, item in enumerate(keys.items)])

# Write Facets specification file
with open(spec_path, 'w') as spec:
    spec.write(
        f"Title = {title}\n"
        "Facets = 4\n"
        f"Model = {model}\n"
        "Noncenter = 1\n"
        "Positive = 1\n"
        "Arrange = N\n"
        "Subset detection = No\n"
        "Delements = 1N, 2N, 3N, 4N\n"
        f"Scorefile = {scores_path}\n"
        f"Output file = {output_path}\n"
        "CSV = Tab\n\n"
        "Labels =\n"
        "1,Comments\n"
        f"{comment_ids}=\n*\n"
        "2,Judges\n"
        f"{annotator_ids}=\n*\n"
        "3,Race,A\n"
        "1=white,0\n"
        "2=black,0\n"
        "*\n"
        "4,Items,A\n"
        f"{item_ids}\n*\n\n"
        f"Data = {data_path}")
