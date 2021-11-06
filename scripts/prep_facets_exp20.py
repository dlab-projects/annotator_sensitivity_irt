"""Runs Facets Scaling Experiment 19.

Experiment 19:
    - Annotator/target facet interaction term.
    - Use the streamlined dataset
    - Filter out missing ratings
    - Filter out by rater quality
    - Recode responses
    - Assign all comments to a particular identity by reverse size.
    - Comments are non-centered
    - Item difficulties are anchored to preprint values.
"""
import numpy as np
import pandas as pd

from hatespeech import keys, utils

# Define paths
exp = "19"
data_path = "~/data/hatespeech/unfiltered_ratings.feather"
rater_quality_path = "~/data/hatespeech/rater_quality_check.csv"
# Column names
comment_col = 'comment_id'
labeler_col = 'labeler_id'

# Read in hate speech data
data = pd.read_feather(data_path)
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
# Only get comments targeting on the basis of race
data = data[data[keys.target_race_cols].sum(axis=1) == 1]
target_ordering = ['native_american',
                   'pacific_islander',
                   'asian',
                   'latinx',
                   'middle_eastern',
                   'white',
                   'black']
annotator_ordering = ['pacific_islander',
                      'middle_eastern',
                      'native_american',
                      'asian',
                      'latinx',
                      'black',
                      'white']
labels = {
    'asian': 1,
    'black': 2,
    'latinx': 3,
    'middle_eastern': 4,
    'native_american': 5,
    'pacific_islander': 6,
    'white': 7,
    'other': 8
}
# Label annotator race
data['annotator_race'] = np.where(
    data[f'annotator_race_{annotator_ordering[0]}'],
    labels[annotator_ordering[0]],
    np.where(
        data[f'annotator_race_{annotator_ordering[1]}'],
        labels[annotator_ordering[1]],
        np.where(
            data[f'annotator_race_{annotator_ordering[2]}'],
            labels[annotator_ordering[2]],
            np.where(
                data[f'annotator_race_{annotator_ordering[3]}'],
                labels[annotator_ordering[3]],
                np.where(
                    data[f'annotator_race_{annotator_ordering[4]}'],
                    labels[annotator_ordering[4]],
                    np.where(
                        data[f'annotator_race_{annotator_ordering[5]}'],
                        labels[annotator_ordering[5]],
                        np.where(
                            data[f'annotator_race_{annotator_ordering[6]}'],
                            labels[annotator_ordering[6]],
                            labels['other'])))))))
# Label target identity race
data['target_race'] = np.where(
    data[f'target_race_{target_ordering[0]}'],
    labels[target_ordering[0]],
    np.where(
        data[f'target_race_{target_ordering[1]}'],
        labels[target_ordering[1]],
        np.where(
            data[f'target_race_{target_ordering[2]}'],
            labels[target_ordering[2]],
            np.where(
                data[f'target_race_{target_ordering[3]}'],
                labels[target_ordering[3]],
                np.where(
                    data[f'target_race_{target_ordering[4]}'],
                    labels[target_ordering[4]],
                    np.where(
                        data[f'target_race_{target_ordering[5]}'],
                        labels[target_ordering[5]],
                        np.where(
                            data[f'target_race_{target_ordering[6]}'],
                            labels[target_ordering[6]],
                            labels['other'])))))))
# Item ID will support Facets spec
data['item_id'] = f'1-{len(keys.items)}'

# Iterate over each racial group
data_path = f"exp{exp}.txt"
spec_path = f"exp{exp}_spec.txt"
scores_path = f"exp{exp}_scores"
output_path = f"exp{exp}_out.txt"

# Generate Facets input
facets = data[[comment_col, labeler_col, "target_race", "annotator_race", "item_id"] + keys.items]
facets.to_csv(data_path, sep=',', header=False, index=False)

# Create strings for Facets specification
comment_ids = "=\n".join(facets[comment_col].drop_duplicates().values.astype('str'))
annotator_ids = "=\n".join(facets[labeler_col].drop_duplicates().values.astype('str'))
item_anchors = [-2.62, -2.26, -0.94, 0.63, -0.51, 0.61, 2.22, 3.11, -1.10, 0.86]
item_ids = "\n".join([f"{idx+1}={item},{item_anchors[idx]}"
                      for idx, item in enumerate(keys.items)])
anchors = "\n".join([f"{val}={key},0" for key, val in labels.items()])

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
        "3,TargetRace,A\n"
        f"{anchors}\n"
        "*\n"
        "4,AnnotatorRace,A\n"
        f"{anchors}\n"
        "*\n"
        "5,Items,A\n"
        f"{item_ids}\n*\n\n"
        f"Data = {data_path}")
