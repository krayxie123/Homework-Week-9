import pandas as pd
import requests
import json

def check_suburb_matching():
    """
    Check how well the suburb names match between CSV and TopoJSON
    """
    print("Checking suburb name matching...")
    
    # Load the study scores data
    study_scores = pd.read_csv('data/suburb_study_scores_joined.csv')
    print(f"Study scores data: {len(study_scores)} suburbs")
    print("Sample study score suburbs:")
    print(study_scores['suburb'].head(10).tolist())
    
    # Load TopoJSON to get the vic_loca_2 names
    try:
        url = "https://raw.githubusercontent.com/krayxie123/Homework-Week-9/main/vicsuburbsgood.topojson"
        response = requests.get(url)
        topojson_data = response.json()
        
        # Extract all vic_loca_2 names
        topojson_suburbs = []
        for geom in topojson_data['objects']['Vicsubs.topojson']['geometries']:
            if 'properties' in geom and 'vic_loca_2' in geom['properties']:
                suburb_name = geom['properties']['vic_loca_2']
                if suburb_name and suburb_name not in topojson_suburbs:
                    topojson_suburbs.append(suburb_name)
        
        print(f"\nTopoJSON suburbs: {len(topojson_suburbs)} unique suburbs")
        print("Sample TopoJSON suburbs:")
        print(topojson_suburbs[:10])
        
        # Check for exact matches
        study_suburbs = set(study_scores['suburb'].str.upper())
        topojson_suburbs_set = set([s.upper() for s in topojson_suburbs])
        
        exact_matches = study_suburbs.intersection(topojson_suburbs_set)
        print(f"\nExact matches: {len(exact_matches)}")
        print("Sample exact matches:")
        print(list(exact_matches)[:10])
        
        # Check for partial matches
        partial_matches = []
        for study_suburb in study_suburbs:
            for topojson_suburb in topojson_suburbs_set:
                if study_suburb in topojson_suburb or topojson_suburb in study_suburb:
                    if study_suburb != topojson_suburb:  # Not exact match
                        partial_matches.append((study_suburb, topojson_suburb))
        
        print(f"\nPartial matches: {len(partial_matches)}")
        print("Sample partial matches:")
        for match in partial_matches[:10]:
            print(f"  {match[0]} -> {match[1]}")
        
        # Show unmatched study suburbs
        unmatched = study_suburbs - topojson_suburbs_set
        print(f"\nUnmatched study suburbs: {len(unmatched)}")
        print("Sample unmatched:")
        print(list(unmatched)[:10])
        
        return len(exact_matches), len(partial_matches), len(unmatched)
        
    except Exception as e:
        print(f"Error loading TopoJSON: {e}")
        return 0, 0, 0

if __name__ == "__main__":
    exact, partial, unmatched = check_suburb_matching()
    print(f"\nSummary:")
    print(f"Exact matches: {exact}")
    print(f"Partial matches: {partial}")
    print(f"Unmatched: {unmatched}")
