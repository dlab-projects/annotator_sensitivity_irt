"""Creates Facets specification from hate speech data.

Experiment 03: Remove non-quality raters, recode responses, and split up data
according to the target identity of the comment: either black or white."""
import pandas as pd

from hatespeech import utils
from hatespeech.keys import gender_to_col, items

# Define paths
exp = "07"
data_path = "~/data/hatespeech/clean_qualtrics_irt_rollout.feather"
rater_quality_path = "~/data/hatespeech/rater_quality_check.csv"
groups = ["men", "women"]
# Column names
comment_col = 'comment_id'
labeler_col = 'labeler_id'
# Facets specification file inputs
title = "Facets Rollout Scaling"
model = "?, ?, #, R"
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

# Item ID will support Facets spec
data['item_id'] = f'1-{len(items)}'

# Iterate over each racial group
for group in groups:
    data_path = f"exp{exp}_data_{group}.txt"
    spec_path = f"exp{exp}_spec_{group}.txt"
    scores_path = f"exp{exp}_scores_{group}"
    output_path = f"exp{exp}_out_{group}.txt"

    # Separate into black and white targeting comments
    subset = data[data[gender_to_col[group]] == 1]
    # Generate Facets input
    facets = subset[[comment_col, labeler_col, "item_id"] + items]
    facets.to_csv(data_path, sep=',', header=False, index=False)

    # Create strings for Facets specification
    comment_ids = "=\n".join(facets[comment_col].drop_duplicates().values.astype('str'))
    annotator_ids = "=\n".join(facets[labeler_col].drop_duplicates().values.astype('str'))
    item_ids = "\n".join([f"{idx+1}={item}" for idx, item in enumerate(items)])

    # Write Facets specification file
    with open(spec_path, 'w') as spec:
        spec.write(
            f"Title = {title}\n"
            "Facets = 3\n"
            f"Model = {model}\n"
            "Noncenter = 1\n"
            "Positive = 1\n"
            "Arrange = N\n"
            "Subset detection = No\n"
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
