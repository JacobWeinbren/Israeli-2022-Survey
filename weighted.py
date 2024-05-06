import pandas as pd
import ujson


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


# Load the DataFrame
df = pd.read_excel("weighted_demog.xlsx")

# Replace numeric identifiers with labels
df["sex"] = df["sex"].replace({1: "male", 2: "female"})

# Mapping dictionaries for education, income, religious community, and religious identification
education_map = {
    1: "No high school diploma",
    2: "No high school diploma",
    3: "No high school diploma",
    4: "No high school diploma",
    5: "High school diploma with matriculation",
    6: "Post-high school, nonacademic diploma",
    7: "Post-high school, nonacademic diploma",
    8: "Academic degree - BA",
    9: "Academic degree - BA",
    10: "Academic degree - MA or higher",
    11: "Academic degree - MA or higher",
}

income_map = {
    0: "No income at all",
    9: "No income at all",
    1: "Much below average",
    2: "Below average",
    3: "Average",
    4: "Above average",
    5: "Much above average",
}

rel_map = {
    1: "Jewish",
    2: "Christian",
    3: "Muslim",
    4: "Druze",
    5: "Other",
    6: "No religion",
}

relid_map = {1: "Secular", 2: "Traditional", 3: "Religious", 4: "Ultra-Orthodox"}

# Apply mappings
df["education_group"] = df["edu"].map(education_map)
df["income_group"] = df["ses"].map(income_map)
df["rel_group"] = df["rel"].map(rel_map)
df["relid_group"] = df["relid"].map(relid_map)

# Calculate age and group it
df["age"] = 2023 - df["byear"]  # Assuming the current year is 2023
df["age_group"] = df["age"].apply(lambda x: categorize_age(x))

# Load regions using ujson for efficiency
with open("regions.json", "r") as file:
    regions = ujson.load(file)

df["cbor_region"] = df["cbor"].map(regions)

# Filter out unwanted data
df = df[df["ses"] != 6]  # Exclude 'Prefer not to answer'
df = df[df["vote2022"].isin(range(1, 15))]  # Exclude parties 15 and 16

# Select required columns
result_df = df[
    [
        "sex",
        "vote2022",
        "weight",
        "education_group",
        "income_group",
        "rel_group",
        "relid_group",
        "age_group",
        "cbor_region",
    ]
]


# Group by categories and calculate weighted sums and proportions
def calculate_proportions(groupby_cols):
    grouped = (
        result_df.groupby(groupby_cols + ["vote2022"])
        .weight.sum()
        .unstack(fill_value=0)
    )
    proportions = grouped.div(grouped.sum(axis=1), axis=0) * 100
    return proportions


# Calculate and save results
for category in [
    "sex",
    "education_group",
    "income_group",
    "rel_group",
    "relid_group",
    "age_group",
    "cbor_region",
]:
    proportions = calculate_proportions([category])
    proportions.to_csv(f"party_proportions_by_{category}.csv")
    print(f"Proportions by {category.capitalize()}:")
    print(proportions)
    print("\n")
