import pandas as pd

school_locations = pd.read_csv('data/dv402-SchoolLocations2025.csv')

#print(school_locations.head(10))

vce_results = pd.read_csv('data/VCE 2024 Results.csv')
print(f"VCE Results: {len(vce_results)} schools")
print(vce_results['Median VCE study score'].value_counts().head(10))