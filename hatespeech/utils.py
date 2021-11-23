import numpy as np

from hatespeech.keys import items as item_names, target_race_to_col, target_gender_to_col


def get_annotator_subsets(data, subsets):
    """Subset the hate speech data by different annotator identity groups.

    Parameters
    ----------
    data : pd.DataFrame
        Hate speech dataset.
    subsets : list of lists, or list of strings
        A list containing each identity group subset. Each entry of the list is
        either a string, denoting a single identity in the subset, or a list of
        strings, denoting a group of identities.

    Returns
    -------
    annotators : list of np.ndarrays
        A list containing the labeler IDs of each annotator within the provided
        subsets.
    """
    annotators_temp = []
    # Iterate over the subsets, matching annotators
    for idx, subset in enumerate(subsets):
        # Turn subset into list if it is a string
        if isinstance(subset, str):
            subsets[idx] = [subset]
        # Get the unique annotators matching to the subset
        annotators_temp.append(np.unique(data[data[subsets[idx]].any(axis=1)]['labeler_id'].values))

    # Remove annotators that are common amongst groups
    annotators = []
    for idx, annotator in enumerate(annotators_temp):
        # Concatenate remaining groups
        remaining = np.concatenate(annotators_temp[:idx] + annotators_temp[idx+1:])
        # Remove shared annotators
        annotators.append(np.setdiff1d(annotator, remaining))
    return annotators


def get_annotator_diffs(data, target1, target2, subsets):
    """Calculate the annotator severity differences between two target groups,
    across annotator subsets.

    Parameters
    ----------
    data : pd.DataFrame
        Hate speech dataset.
    target1, target2 : pd.DataFrame
        The Facets dataframe corresponding to each annotators' severity on
        the Facets run targeting identity group 1 (target1) or identity group
        2 (target2).
    subsets : list of lists, or list of strings
        A list containing each identity group subset. Each entry of the list is
        either a string, denoting a single identity in the subset, or a list of
        strings, denoting a group of identities.

    Returns
    -------
    diffs : list of np.ndarrays
        A list containing the severity differences for each annotator group
        provided in subsets.
    """
    diffs = []
    # Obtain annotator subsets
    annotators = get_annotator_subsets(data, subsets)
    # Iterate over the annotator groups
    for idx, annotator in enumerate(annotators):
        target1_sevs = target1[target1['Judges'].isin(annotator)]['Measure'].values
        target2_sevs = target2[target2['Judges'].isin(annotator)]['Measure'].values
        diffs.append(target1_sevs - target2_sevs)

    return diffs


def filter_missing_items(data):
    """Filters the hate speech dataset according to missing data in the survey
    items.

    Parameters
    ----------
    data : pd.DataFrame
        Hate speech dataset.

    Returns
    -------
    data : pd.DataFrame
        Hate speech dataset with rows that contain a missing item removed.
    """
    types = {item: 'int64' for item in item_names}
    return data[~data[item_names].isna().any(axis=1)].astype(types)


def filter_annotator_quality(
    data, annotator_quality, annotator_col='labeler_id', quality_col='quality_check'
):
    """Filters the hate speech dataset according to rater quality.

    Parameters
    ----------
    data : pd.DataFrame
        Hate speech dataset.
    annotator_quality : pd.DataFrame
        A dataframe containing two columns: one with the annotator ID, and the
        other with a bool indicating whether the annotator is a quality annotator,
        or not.
    annotator_col : string
        The column denoting the annotator ID.
    quality_col : string
        The column denoting the quality flag.

    Returns
    -------
    data : pd.DataFrame
        Hate speech dataset with rows that only contain quality annotators.
    """
    quality_annotators = annotator_quality[annotator_quality[quality_col]][annotator_col].values
    return data[data[annotator_col].isin(quality_annotators)]


def recode_responses(
    data, items=None, sentiment={}, respect={}, insult={}, humiliate={},
    status={}, dehumanize={}, violence={}, genocide={}, attack_defend={},
    hatespeech={}
):
    """Recodes the item responses.

    Parameters
    ----------
    data : pd.DataFrame
        Hate speech dataset.
    items : dict of dicts
        A dict whose keys must be the item names, and whose values are additional
        dicts containing the recoding. If this is not provided, it is created
        from the remaining arguments.
    sentiment, respect, insult, humiliate, status, dehumanize, violence, genocide,
    attack_defend, hatespeech : dict
        The recoding for each hate speech item as a dict, with keys denoting
        the values to replace, and values denoting what to replace them with.
    """
    if items is None:
        items = dict(zip(item_names,
                         [sentiment, respect, insult, humiliate, status,
                          dehumanize, violence, genocide, attack_defend, hatespeech]))
    return data.replace(items)


def filter_annotator_identity(data, annotators, omit_multiracial=True):
    """Filter the dataset according to annotator identity.

    Parameters
    ----------
    data : pd.DataFrame
        The hate speech dataset.
    annotators : list of strings
        The annotator identities to filter by. This list should contain the
        column names.
    omit_multiracial : bool
        If True, removes annotators that identify as one or more of the
        provided columns.

    Returns
    -------
    subset : pd.DataFrame
        A subset of the original dataframe containing only comments annotated
        by annotators in the identity group.
    """
    subset = data[data[annotators].any(axis=1)]
    if omit_multiracial:
        subset = subset[subset[annotators].sum(axis=1) == 1]
    return subset.copy()


def get_annotator_agreement(data, targets):
    subset = data[data[targets].any(axis=1)]
    proportions = subset.groupby(
        'comment_id'
        ).agg(
            {target: 'mean' for target in targets}
        ).reset_index()
    return proportions


def get_comments_w_agreement(data, targets, threshold):
    proportions = get_annotator_agreement(data, targets)
    agreed_comments = proportions[proportions[targets].ge(threshold).any(axis=1)]
    agreed_comments = agreed_comments[~agreed_comments[targets].ge(threshold).all(axis=1)]
    # Threshold the agreement fraction
    thresholded_comments = agreed_comments.copy()
    thresholded_comments[targets] = thresholded_comments[targets].ge(threshold)
    samples_w_agreement = data.merge(thresholded_comments,
                                     how='right',
                                     on='comment_id',
                                     suffixes=('', '_agreed'))
    
    return agreed_comments, samples_w_agreement


def filter_comments_targeting_bw(data, threshold=0.5):
    """Filter out comments not targeting on the basis on black/white identity.

    Parameters
    ----------
    data : pd.DataFrame
        Hate speech dataset.
    threshold : float
        The fraction of annotators that have to agree on the target identity.
    """
    # Determine which annotators agree on target identity
    proportions = data.fillna(
        {target_race_to_col['black']: 0,
         target_race_to_col['white']: 0}
    ).groupby(
        'comment_id'
    ).agg(
        {target_race_to_col['black']: 'mean',
         target_race_to_col['white']: 'mean'}
    ).rename(
        {target_race_to_col['black']: 'target_black',
         target_race_to_col['white']: 'target_white'},
        axis=1
    ).reset_index()
    # Get comments satisfying threshold
    valid_comments = proportions[
        (proportions['target_black'] > threshold)
        | (proportions['target_white'] > threshold)
    ]
    valid_ids = valid_comments['comment_id']
    filtered = data[data['comment_id'].isin(valid_ids)].copy().merge(
        valid_comments[['comment_id', 'target_black']],
        on='comment_id')
    filtered['target_black'] = filtered['target_black'] >= 0.5
    return filtered


def filter_comments_targeting_mw(data, threshold=0.5):
    """Filter out comments not targeting on the basis on male/female identity.

    Parameters
    ----------
    data : pd.DataFrame
        Hate speech dataset.
    threshold : float
        The fraction of annotators that have to agree on the target identity.
    """
    # Determine which annotators agree on target identity
    proportions = data.fillna(
        {target_gender_to_col['men']: 0,
         target_gender_to_col['women']: 0}
    ).groupby(
        'comment_id'
    ).agg(
        {target_gender_to_col['men']: 'mean',
         target_gender_to_col['women']: 'mean'}
    ).rename(
        {target_gender_to_col['men']: 'target_men',
         target_gender_to_col['women']: 'target_women'},
        axis=1
    ).reset_index()
    # Get comments satisfying threshold
    valid_comments = proportions[
        (proportions['target_men'] > threshold)
        | (proportions['target_women'] > threshold)
    ]
    valid_ids = valid_comments['comment_id']
    filtered = data[data['comment_id'].isin(valid_ids)].copy().merge(
        valid_comments[['comment_id', 'target_women']],
        on='comment_id')
    filtered['target_women'] = filtered['target_women'] >= 0.5
    return filtered


def filter_comments_by_count(data, threshold=50, comment_id_col='comment_id'):
    """Filters comments in the reference set, defined as those that """
    n_labelers = data[comment_id_col].value_counts()
    reference_ids = n_labelers[n_labelers > threshold].index
    reference_set = data[data[comment_id_col].isin(reference_ids)].copy()
    return reference_set
