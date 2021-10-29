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
target_col_to_identity = {
    'target_identities_1': 'race',
    'target_identities_2': 'religion',
    'target_identities_3': 'national_origin',
    'target_identities_4': 'gender',
    'target_identities_5': 'sexual_orientation',
    'target_identities_6': 'age',
    'target_identities_7': 'disability',
    'target_identities_9': 'other'}
target_identity_to_col = swap_key_val(target_col_to_identity)

# Target identity race column
target_col_to_race = {
    'target_race_1': 'black',
    'target_race_2': 'latinx',
    'target_race_3': 'asian',
    'target_race_8': 'middle_eastern',
    'target_race_4': 'native_american',
    'target_race_5': 'pacific_islander',
    'target_race_6': 'white',
    'target_race_7': 'other_race'}
target_race_to_col = swap_key_val(target_col_to_race)
# For transformed data
target_race_cols = [
    'target_race_asian',
    'target_race_black',
    'target_race_latinx',
    'target_race_middle_eastern',
    'target_race_native_american',
    'target_race_pacific_islander',
    'target_race_white',
    'target_race_other'
]

# Target identity religion column
target_col_to_religion = {
    'target_religion_1': 'jewish',
    'target_religion_2': 'christian',
    'target_religion_4': 'buddhist',
    'target_religion_5': 'hindu',
    'target_religion_6': 'other',
    'target_religion_8': 'mormon',
    'target_religion_9': 'atheist',
    'target_religion_10': 'muslim'}
target_religion_to_col = swap_key_val(target_col_to_religion)
# For transformed data
target_religion_cols = [
    'target_religion_atheist',
    'target_religion_buddhist',
    'target_religion_christian',
    'target_religion_hindu',
    'target_religion_jewish',
    'target_religion_mormon',
    'target_religion_muslim',
    'target_religion_other',
]

# Target identity citizenship column
target_col_to_origin = {
    'target_citizen_1': 'immigrant',
    'target_citizen_2': 'migrant_worker',
    'target_citizen_3': 'undocumented',
    'target_citizen_4': 'other',
    'target_citizen_5': 'specific_country'}
target_origin_to_col = swap_key_val(target_col_to_origin)
# For transformed data
target_origin_cols = [
    'target_origin_immigrant',
    'target_origin_migrant_worker',
    'target_origin_specific_country',
    'target_origin_undocumented',
    'target_origin_other'
]

# Target identity gender column
target_col_to_gender = {
    'target_gender_1': 'men',
    'target_gender_2': 'non-binary',
    'target_gender_3': 'women',
    'target_gender_4': 'other_gender',
    'target_gender_5': 'transgender_women',
    'target_gender_6': 'transgender_men',
    'target_gender_7': 'transgender_unspecified'}
target_gender_to_col = swap_key_val(target_col_to_gender)
# For transformed data
target_gender_cols = [
    'target_gender_men',
    'target_gender_non_binary',
    'target_gender_transgender_men',
    'target_gender_transgender_unspecified',
    'target_gender_transgender_women',
    'target_gender_women',
    'target_gender_other'
]

# Target identity sexuality column
target_col_to_sexuality = {
    'target_sexuality_1': 'bisexual',
    'target_sexuality_2': 'gay',
    'target_sexuality_3': 'lesbian',
    'target_sexuality_6': 'straight',
    'target_sexuality_5': 'other'}
target_sexuality_to_col = swap_key_val(target_col_to_sexuality)
# For transformed data
target_sexuality_cols = [
    'target_sexuality_bisexual',
    'target_sexuality_gay',
    'target_sexuality_lesbian',
    'target_sexuality_straight',
    'target_sexuality_other'
]

# Target identity age column
target_col_to_age = {
    'target_age_1': 'children',
    'target_age_2': 'teenagers',
    'target_age_3': 'young_adults',
    'target_age_4': 'middle_aged',
    'target_age_5': 'seniors',
    'target_age_6': 'other'
}
target_age_to_col = swap_key_val(target_col_to_age)
# For transformed data
target_age_cols = [
    'target_age_children',
    'target_age_teenagers',
    'target_age_young_adults',
    'target_age_middle_aged',
    'target_age_seniors',
    'target_age_other'
]

# Target identity disability column
target_col_to_disability = {
    'target_disability_1': 'physical',
    'target_disability_2': 'cognitive',
    'target_disability_3': 'neurological',
    'target_disability_4': 'visually_impaired',
    'target_disability_5': 'hearing_impaired',
    'target_disability_6': 'other',
    'target_disability_9': 'unspecific'
}
target_disability_to_col = swap_key_val(target_col_to_disability)
# For transformed data
target_disability_cols = [
    'target_disability_physical',
    'target_disability_cognitive',
    'target_disability_neurological',
    'target_disability_visually_impaired',
    'target_disability_hearing_impaired',
    'target_disability_unspecific',
    'target_disability_other'
]

# Target identity politics column
target_col_to_politics = {
    'q39_1': 'republican',
    'q39_2': 'conservative',
    'q39_3': 'alt_right',
    'q39_4': 'democrat',
    'q39_5': 'liberal',
    'q39_6': 'green_party',
    'q39_7': 'socialist',
    'q39_8': 'communist',
    'q39_9': 'leftist',
    'q39_10': 'libertarian',
    'q39_11': 'other'
}
target_politics_to_col = swap_key_val(target_col_to_politics)
# For transformed data
target_politics_cols = [
    'target_politics_alt_right',
    'target_politics_communist',
    'target_politics_conservative',
    'target_politics_democrat',
    'target_politics_green_party',
    'target_politics_leftist',
    'target_politics_liberal',
    'target_politics_libertarian',
    'target_politics_republican',
    'target_politics_socialist',
    'target_politics_other'
]

"""
Annotator columns
"""
# Annotator gender
annotator_gender_col = 'demo_gender'
annotator_gender = {
    'female': 1.0,
    'male': 2.0,
    'non-binary': 3.0,
    'self-describe': 4.0,
    'prefer_not_to_say': 5.0}

# Is annotator transgender?
annotator_trans_col = 'demo_trans'
annotator_trans = {
    'yes': 1.0,
    'no': 2.0,
    'prefer_not_to_say': 4}

# Annotator education status
annotator_educ_col = 'demo_educ'
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
annotator_col_to_race = {
    'demo_race_ethnicitie_1': 'native_american',
    'demo_race_ethnicitie_2': 'asian',
    'demo_race_ethnicitie_3': 'black',
    'demo_race_ethnicitie_4': 'latinx',
    'demo_race_ethnicitie_5': 'pacific_islander',
    'demo_race_ethnicitie_6': 'white',
    'demo_race_ethnicitie_7': 'other_race',
    'demo_race_ethnicitie_8': 'middle_eastern'}
annotator_race_to_col = swap_key_val(annotator_col_to_race)
# For transformed data
annotator_race_cols = [
    'annotator_race_asian',
    'annotator_race_black',
    'annotator_race_latinx',
    'annotator_race_middle_eastern',
    'annotator_race_native_american',
    'annotator_race_pacific_islander',
    'annotator_race_white',
    'annotator_race_other'
]

# Annotator age
annotator_age_col = 'demo_age'


def annotator_year_converter(code):
    if code == 1:
        return 2002
    else:
        return 2002 - (code - 102)


def annotator_age_converter(code):
    year = annotator_year_converter(code)
    return 2019 - year


# Annotator income
annotator_income_col = 'demo_income'
annotator_income = {
    '<10k': 1.0,
    '10k-50k': 2.0,
    '50k-100k': 3.0,
    '100k-200k': 4.0,
    '>200k': 5.0}

# Annotator religion
annotator_col_to_religion = {
    'demo_religion_1': 'atheist',
    'demo_religion_2': 'buddhist',
    'demo_religion_4': 'hindu',
    'demo_religion_5': 'jewish',
    'demo_religion_7': 'mormon',
    'demo_religion_8': 'muslim',
    'demo_religion_9': 'nothing',
    'demo_religion_10': 'other',
    'demo_religion_11': 'christian'}
annotator_religion_to_col = swap_key_val(annotator_col_to_religion)

# Annotator sexual orientation
annotator_col_to_sexual_orientation = {
    'demo_sexual_orien_1': 'straight',
    'demo_sexual_orien_2': 'gay',
    'demo_sexual_orien_3': 'bisexual',
    'demo_sexual_orien_4': 'other',
    'demo_sexual_orien_5': 'prefer_not_to_say'}
annotator_sexual_orientation_to_col = swap_key_val(annotator_col_to_sexual_orientation)

# Annotator ideology
annotator_ideology_col = 'demo_ideology'
annotator_ideology = {
    'extremely_liberal': 1,
    'liberal': 2,
    'slightly_liberal': 3,
    'neutral': 4,
    'slightly_conservative': 5,
    'conservative': 6,
    'extremely_conservative': 7,
    'no_opinion': 8}
