def swap_key_val(dic):
    """Swaps key, value pairs in a dictionary."""
    return {val: key for key, val in dic.items()}


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

col_to_gender = {
    'target_gender_1': 'men',
    'target_gender_2': 'non-binary',
    'target_gender_3': 'women',
    'target_gender_4': 'other_gender',
    'target_gender_5': 'transgender_women',
    'target_gender_6': 'transgender_men',
    'target_gender_7': 'transgender_unspecified'}
gender_to_col = swap_key_val(col_to_gender)

annotator_gender = {
    'female': 1.0,
    'male': 2.0,
    'non-binary': 3.0,
    'self-describe': 4.0,
    'prefer_not_to_say': 5.0}

annotator_ideology = {
    'extremely_liberal': 1,
    'liberal': 2,
    'slightly_liberal': 3,
    'neutral': 4,
    'slightly_conservative': 5,
    'conservative': 6,
    'extremely_conservative': 7,
    'no_opinion': 8
}
