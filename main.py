import pandas as pd

# Load data
df = pd.read_excel("demog.xls")

# Calculate age
df["age"] = 2022 - df["byear"]

# Filter data
df = df[(df["sex"] != 0) & (df["age"] >= 18)]

# Define weights
sex_weights = {1: 0.487, 2: 0.513}
age_weights = {
    "20-24": 0.110,
    "25-29": 0.103,
    "30-34": 0.099,
    "35-39": 0.094,
    "40-44": 0.101,
    "45-49": 0.090,
    "50-54": 0.082,
    "55-59": 0.065,
    "60-64": 0.068,
    "65-74": 0.117,
    "75+": 0.073,
}
edu_group_weights = {
    "No high school diploma": 0.247,
    "High school diploma with matriculation": 0.220,
    "Post-high school, nonacademic diploma": 0.167,
    "Academic degree - BA": 0.202,
    "Academic degree - MA or higher": 0.144,
}
rel_weights = {1: 0.803, 2: 0.121, 3: 0.025, 4: 0.024, 5: 0.003, 6: 0.022}
relid_weights = {1: 0.377, 2: 0.301, 3: 0.221, 4: 0.094}


# Categorize age into ranges
def categorize_age(age):
    if age < 20:
        return None
    for start in range(20, 75, 5):
        if age < start + 5:
            return f"{start}-{start+4}"
    return "75+"


df["age_range"] = df["age"].apply(categorize_age)


# Categorize education into groups
def categorize_education(edu):
    if edu in [1, 2, 3, 4]:
        return "No high school diploma"
    elif edu == 5:
        return "High school diploma with matriculation"
    elif edu in [6, 7]:
        return "Post-high school, nonacademic diploma"
    elif edu in [8, 9]:
        return "Academic degree - BA"
    elif edu in [10, 11, 12, 13]:
        return "Academic degree - MA or higher"
    else:
        return None


df["edu_group"] = df["edu"].apply(categorize_education)

# Map weights to age ranges, sex, education groups, religion, and religious identity
df["edu_weight"] = df["edu_group"].map(edu_group_weights)
df["rel_weight"] = df["rel"].map(rel_weights)
df["relid_weight"] = df["relid"].map(relid_weights)
df["combined_weight"] = (
    df["age_range"].map(age_weights)
    * df["sex"].map(sex_weights)
    * df["edu_weight"]
    * df["rel_weight"]
    * df["relid_weight"]
)

# Calculate and sum the weighted votes
df["weighted_vote"] = df["combined_weight"] * df["vote2022"]
df_filtered = df[~df["vote2022"].isin([15, 16])]
party_weighted_votes = df_filtered.groupby("vote2022")["weighted_vote"].sum()
total_weighted_votes = party_weighted_votes.sum()
party_proportions = party_weighted_votes / total_weighted_votes

# Output the proportion of votes for each party
print(party_proportions)
