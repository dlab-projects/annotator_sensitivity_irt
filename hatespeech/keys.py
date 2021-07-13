def swap_key_val(dic):
    """Swaps key, value pairs in a dictionary."""
    return {val: key for key, val in dic.items()}


# Hate speech construct items
items = [
    "sentiment",
    "respect",
    "insult",
    "humiliate",
    "status",
    "dehumanize",
    "violence",
    "genocide",
    "attack_defend",
    "hatespeech"]

"""
Target identities
"""
# Target identity columns
col_to_identity = {
    'target_identities_1': 'race',
    'target_identities_2': 'religion',
    'target_identities_3': 'national_origin',
    'target_identities_4': 'gender',
    'target_identities_5': 'sexual_orientation',
    'target_identities_6': 'age',
    'target_identities_7': 'disability',
    'target_identities_9': 'other'}
identity_to_col = swap_key_val(col_to_identity)

# Target identity race column
col_to_race = {
    'target_race_1': 'black',
    'target_race_2': 'latinx',
    'target_race_3': 'asian',
    'target_race_8': 'middle_eastern',
    'target_race_4': 'native_american',
    'target_race_5': 'pacific_islander',
    'target_race_6': 'white',
    'target_race_7': 'other_race'}
race_to_col = swap_key_val(col_to_race)

col_to_gender = {
    'target_gender_1': 'men',
    'target_gender_2': 'non-binary',
    'target_gender_3': 'women',
    'target_gender_4': 'other_gender',
    'target_gender_5': 'transgender_women',
    'target_gender_6': 'transgender_men',
    'target_gender_7': 'transgender_unspecified'}
gender_to_col = swap_key_val(col_to_gender)

"""
Annotator columns
"""
# Annotator gender
annotator_gender = {
    'female': 1.0,
    'male': 2.0,
    'non-binary': 3.0,
    'self-describe': 4.0,
    'prefer_not_to_say': 5.0}

# Is annotator transgender?
annotator_trans = {
    'yes': 1.0,
    'no': 2.0,
    'prefer_not_to_say': 4}

# Annotator education status
annotator_educ = {
    'some_high_school': 1,
    'high_school_grad': 2,
    'some_college': 3,
    'college_grad_aa': 5,
    'college_grad_ba': 6,
    'masters': 7,
    'professional_degree': 8,
    'phd': 9}

# Annotator race
col_to_annotator_race = {
    'demo_race_ethnicitie_1': 'native_american',
    'demo_race_ethnicitie_2': 'asian',
    'demo_race_ethnicitie_3': 'black',
    'demo_race_ethnicitie_4': 'latinx',
    'demo_race_ethnicitie_5': 'pacific_islander',
    'demo_race_ethnicitie_6': 'white',
    'demo_race_ethnicitie_7': 'other race',
    'demo_race_ethnicitie_8': 'middle eastern'}
annotator_race_to_col = swap_key_val(col_to_annotator_race)

# Annotator age
# TODO

# Annotator income
annotator_income = {
    '<10k': 1.0,
    '10k-50k': 2.0,
    '50k-100k': 3.0,
    '100k-200k': 4.0,
    '>200k': 5.0}

# Annotator religion
annotator_religion = {
    'atheist': 1.0,
    'buddhist': 2.0,
    'christian': 11.0,
    'hindu': 4.0,
    'jewish': 5.0,
    'mormon': 7.0,
    'muslim': 8.0,
    'nothing': 9.0,
    'other': 10}
col_to_annotator_religion = {
    'demo_religion_1': 'atheist',
    'demo_religion_2': 'buddhist',
    'demo_religion_4': 'hindu',
    'demo_religion_5': 'jewish',
    'demo_religion_7': 'mormon',
    'demo_religion_8': 'muslim',
    'demo_religion_9': 'nothing',
    'demo_religion_10': 'other',
    'demo_religion_11': 'christian'}
annotator_religion_to_col = swap_key_val(col_to_annotator_religion)

# Annotator sexual orientation
annotator_sexual_orientation = {
    'straight': 1.0,
    'gay': 2.0,
    'bisexual': 3.0,
    'other': 4.0,
    'prefer_not_to_say': 5.0}
col_to_annotator_sexual_orientation = {
    'demo_sexual_orien_1': 'straight',
    'demo_sexual_orien_2': 'gay',
    'demo_sexual_orien_3': 'bisexual',
    'demo_sexual_orien_4': 'other',
    'demo_sexual_orien_5': 'prefer_not_to_say'}
annotator_sexual_orientation_to_col = swap_key_val(col_to_annotator_sexual_orientation)

# Annotator ideology
annotator_ideology = {
    'extremely_liberal': 1,
    'liberal': 2,
    'slightly_liberal': 3,
    'neutral': 4,
    'slightly_conservative': 5,
    'conservative': 6,
    'extremely_conservative': 7,
    'no_opinion': 8}
