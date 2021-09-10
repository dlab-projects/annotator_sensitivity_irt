from hatespeech.keys import items as item_names


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
