import pandas as pd
import numpy as np

# Load data
df = pd.read_excel("demog.xls")

# Calculate age
df["age"] = 2022 - df["byear"]

# Filter data
df = df[(df["sex"] != 0) & (df["age"] >= 18)]


# Categorize age into ranges
def categorize_age(age):
    if age < 20:
        return None
    age_ranges = [
        (20, 24),
        (25, 29),
        (30, 34),
        (35, 39),
        (40, 44),
        (45, 49),
        (50, 54),
        (55, 59),
        (60, 64),
        (65, 74),
        (75, float("inf")),
    ]
    for start, end in age_ranges:
        if start <= age <= end:
            if end == float("inf"):
                return "75+"
            else:
                return f"{start}-{end}"
    return None


df["age_range"] = df["age"].apply(categorize_age)


# Categorize aliyah year
def categorize_alyayear(year):
    if year == 0:
        return "Didn't make Aliyah"
    elif year <= 1947:
        return "Up to 1947"
    elif 1948 <= year <= 1954:
        return "1948 - 1954"
    elif 1955 <= year <= 1960:
        return "1955 - 1960"
    elif 1961 <= year <= 1971:
        return "1961 - 1971"
    elif 1972 <= year <= 1979:
        return "1972 - 1979"
    elif 1980 <= year <= 1989:
        return "1980 - 1989"
    elif 1990 <= year <= 1995:
        return "1990 - 1995"
    elif year >= 1996:
        return "1996 and forward"


df["alyayear_group"] = df["alyayear"].apply(categorize_alyayear)


# Categorize education
def categorize_education(edu):
    if edu in [1, 2, 3, 4]:
        return "No high school diploma"
    elif edu == 5:
        return "High school diploma with matriculation"
    elif edu in [6, 7]:
        return "Post-high school, nonacademic diploma"
    elif edu in [8, 9]:
        return "Academic degree - BA"
    elif edu in [10, 11]:
        return "Academic degree - MA or higher"


df["education_group"] = df["edu"].apply(categorize_education)

# Define target distributions (these should be based on known population data)
targets = {
    "sex": {1: 0.487, 2: 0.513},
    "age_range": {
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
    },
    "education_group": {
        "No high school diploma": 0.247,
        "High school diploma with matriculation": 0.220,
        "Post-high school, nonacademic diploma": 0.167,
        "Academic degree - BA": 0.202,
        "Academic degree - MA or higher": 0.144,
    },
    "alyayear_group": {
        "Didn't make Aliyah": 0.745,
        "Up to 1947": 0.002,
        "1948 - 1954": 0.020,
        "1955 - 1960": 0.015,
        "1961 - 1971": 0.028,
        "1972 - 1979": 0.015,
        "1980 - 1989": 0.016,
        "1990 - 1995": 0.072,
        "1996 and forward": 0.089,
    },
    "rel": {1: 0.803, 2: 0.121, 3: 0.025, 4: 0.024, 5: 0.003, 6: 0.022},
    "relid": {1: 0.377, 2: 0.301, 3: 0.221, 4: 0.094},
    "vote2022": {
        1: 0.2341,
        2: 0.1779,
        3: 0.1084,
        4: 0.0908,
        5: 0.0825,
        6: 0.0588,
        7: 0.0448,
        8: 0.0407,
        9: 0.0375,
        10: 0.0369,
        11: 0.0316,
        12: 0.0291,
        13: 0.0119,
        14: 0.0150,
    },
}

# Initialize weights
df["weight"] = 1.0


# Function to apply rim weighting
def rim_weighting(df, category, target_dist):
    # Calculate current distribution
    current_dist = df.groupby(category).weight.sum() / df.weight.sum()
    current_dist = current_dist.reindex(target_dist.index, fill_value=0)

    # Calculate adjustment factors
    adjustment_factors = target_dist / current_dist

    # Apply adjustment
    df["weight"] *= df[category].map(adjustment_factors)
    return df


# Apply rim weighting for each category
for category, target_dist in targets.items():
    target_series = pd.Series(target_dist)
    df = rim_weighting(df, category, target_series)

# Save the weighted DataFrame
df.to_excel("weighted_demog.xlsx", index=False)

# Filter out values 15 and 16
filtered_df = df[df["vote2022"].isin([15, 16]) == False]

# Calculate the proportion of each category in 'vote2022'
vote_proportions = (
    filtered_df.groupby("vote2022")["weight"].sum() / filtered_df["weight"].sum()
)

# Display the proportions
print(vote_proportions)
