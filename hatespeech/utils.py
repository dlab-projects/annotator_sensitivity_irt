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
    "hatespeech"
]

col_to_identity = {
    'target_identities_1': 'race',
    'target_identities_2': 'religion',
    'target_identities_3': 'national_origin',
    'target_identities_4': 'gender',
    'target_identities_5': 'sexual_orientation',
    'target_identities_6': 'age',
    'target_identities_7': 'disability',
    'target_identities_9': 'other'
}
identity_to_col = {val: key for key, val in col_to_identity.items()}

col_to_race = {
    'target_race_1': 'black',
    'target_race_2': 'latinx',
    'target_race_3': 'asian',
    'target_race_8': 'middle_eastern',
    'target_race_4': 'native_american',
    'target_race_5': 'pacific_islander',
    'target_race_6': 'white',
    'target_race_7': 'other_race',
}
race_to_col = {val: key for key, val in col_to_race.items()}

col_to_annotator_race = {
    'demo_race_ethnicitie_1': 'native_american',
    'demo_race_ethnicitie_2': 'asian',
    'demo_race_ethnicitie_3': 'black',
    'demo_race_ethnicitie_4': 'latinx',
    'demo_race_ethnicitie_5': 'pacific_islander',
    'demo_race_ethnicitie_6': 'white',
    'demo_race_ethnicitie_7': 'other race',
    'demo_race_ethnicitie_8': 'middle eastern',
}
annotator_race_to_col = {val: key for key, val in col_to_annotator_race.items()}
