"""Runs Facets Scaling Experiment 10.

Experiment 15:
    - Separate calibration on women vs. men
    - Use the streamlined dataset
    - Filter out missing ratings
    - Filter out by rater quality
    - Recode responses
    - Use chosen targets without any additional checking
    - Comments are non-centered
    - Item difficulties are anchored to preprint values
"""
import pandas as pd

from hatespeech import keys, utils

# Define paths
exp = "15"
data_path = "~/data/hatespeech/unfiltered_ratings.feather"
rater_quality_path = "~/data/hatespeech/rater_quality_check.csv"
groups = ["men", "women"]
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
# Only get comments targeting on the basis of male or female identity
data = data[data['target_gender_men'] | data['target_gender_women']]

# Item ID will support Facets spec
data['item_id'] = f'1-{len(keys.items)}'

# Iterate over each racial group
for group in groups:
    data_path = f"exp{exp}_data_{group}.txt"
    spec_path = f"exp{exp}_spec_{group}.txt"
    scores_path = f"exp{exp}_scores_{group}"
    output_path = f"exp{exp}_out_{group}.txt"

    # Separate into male and female targeting comments
    subset = data[data[f'target_gender_{group}'] == 1]
    # Generate Facets input
    facets = subset[[comment_col, labeler_col, "item_id"] + keys.items]
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
            f"Title = Experiment {exp}\n"
            "Facets = 3\n"
            # Facet 1: Comments
            # Facet 2: Judges
            # Facet 3: Items (Partial Credit)
            f"Model = ?, ?, #, R\n"
            # Facet 1, the comments, is noncentered
            "Noncenter = 1\n"
            # Which parameters are positive in the model (only the comments)
            "Positive = 1 \n"
            # How to arrange the ordering of elements: do so by (N)umber
            "Arrange = N\n"
            # Whether to perform subset detection: likely not necessary
            "Subset detection = No\n"
            # In the data, do we use the numeric or string labels?
            # We always use the numeric labels, so these should always end in N
            "Delements = 1N, 2N, 3N\n"
            f"Scorefile = {scores_path}\n"
            f"Output file = {output_path}\n"
            "CSV = Tab\n\n"
            "Labels =\n"
            "1,Comments\n"
            f"{comment_ids}=\n*\n"
            "2,Judges\n"
            f"{annotator_ids}=\n*\n"
            "3,Items,A\n"
            f"{item_ids}\n*\n\n"
            f"Data = {data_path}")
