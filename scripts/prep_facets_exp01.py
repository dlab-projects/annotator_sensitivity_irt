"""Creates Facets specification from hate speech data.

Experiment 01: Minimal preprocessing, split up data according to the target
identity of the comment: either black or white."""
import pandas as pd

from hatespeech.keys import race_to_col, items

# Define paths
data_path = "../data/clean_qualtrics_irt_rollout.feather"
groups = ["white", "black"]

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
data = data[~data[items].isna().any(axis=1)].astype({item: 'int64' for item in items})
# Item ID will support Facets spec
data['item_id'] = f'1-{len(items)}'

# Iterate over each racial group
for group in groups:
    data_path = f"exp01_data_{group}.txt"
    spec_path = f"exp01_spec_{group}.txt"
    scores_path = f"exp01_scores_{group}"
    output_path = f"exp01_out_{group}.txt"

    # Separate into black and white targeting comments
    subset = data[data[race_to_col[group]] == 1]
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
