import pandas as pd
from fuzzywuzzy import fuzz, process

# Read the CSV files
municipalities = pd.read_csv('data/victoria_municipalities.csv')
study_scores = pd.read_csv('data/suburb_study_scores_joined.csv')

print("Municipalities columns:", municipalities.columns.tolist())
print("Study scores columns:", study_scores.columns.tolist())
print("\nFirst few municipalities:")
print(municipalities.head())
print("\nFirst few study scores:")
print(study_scores.head())

# Create a mapping function to match suburbs to municipalities
def find_best_municipality_match(suburb_name, municipality_list, threshold=60):
    """
    Find the best matching municipality for a suburb name using fuzzy matching
    """
    best_match = process.extractOne(suburb_name, municipality_list, scorer=fuzz.ratio)
    if best_match and best_match[1] >= threshold:
        return best_match[0]
    return None

# Get list of municipalities
municipality_list = municipalities['Municipality'].tolist()

# Create a new column for matched municipality
study_scores['matched_municipality'] = study_scores['suburb'].apply(
    lambda x: find_best_municipality_match(x, municipality_list)
)

# Show some examples of matches
print("\nSample matches:")
sample_matches = study_scores[study_scores['matched_municipality'].notna()].head(10)
print(sample_matches[['suburb', 'matched_municipality', 'avg_study_score']])

# Merge with municipalities data
merged_data = study_scores.merge(
    municipalities, 
    left_on='matched_municipality', 
    right_on='Municipality', 
    how='left'
)

# Show the final result
print(f"\nTotal records: {len(merged_data)}")
print(f"Records with municipality match: {merged_data['Municipality'].notna().sum()}")
print(f"Records without municipality match: {merged_data['Municipality'].isna().sum()}")

# Save the merged data
merged_data.to_csv('data/suburb_municipality_scores.csv', index=False)
print("\nMerged data saved to 'data/suburb_municipality_scores.csv'")

# Show final structure
print("\nFinal columns:")
print(merged_data.columns.tolist())
print("\nFirst few rows of merged data:")
print(merged_data.head())
