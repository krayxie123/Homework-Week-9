import json
import requests

def check_topojson_properties():
    """
    Check what properties are available in the TopoJSON file
    """
    print("Checking TopoJSON properties...")
    
    try:
        # Load the TopoJSON file
        url = "https://raw.githubusercontent.com/krayxie123/Homework-Week-9/main/vicsuburbsgood.topojson"
        response = requests.get(url)
        response.raise_for_status()
        
        topojson_data = response.json()
        
        print(f"TopoJSON loaded successfully")
        print(f"Keys in TopoJSON: {list(topojson_data.keys())}")
        
        # Check the features
        if 'objects' in topojson_data:
            print(f"Objects in TopoJSON: {list(topojson_data['objects'].keys())}")
            
            # Check the Vicsubs.topojson feature
            if 'Vicsubs.topojson' in topojson_data['objects']:
                vicsubs = topojson_data['objects']['Vicsubs.topojson']
                print(f"Vicsubs feature type: {vicsubs.get('type', 'Unknown')}")
                
                if 'geometries' in vicsubs:
                    geometries = vicsubs['geometries']
                    print(f"Number of geometries: {len(geometries)}")
                    
                    # Check properties of first few geometries
                    print(f"\nSample properties from first 5 geometries:")
                    for i, geom in enumerate(geometries[:5]):
                        if 'properties' in geom:
                            props = geom['properties']
                            print(f"Geometry {i}: {props}")
                        else:
                            print(f"Geometry {i}: No properties")
        
        # Also check if there are other feature names
        print(f"\nAll possible feature names:")
        for obj_name, obj_data in topojson_data.get('objects', {}).items():
            print(f"- {obj_name}")
            
    except Exception as e:
        print(f"Error loading TopoJSON: {e}")

if __name__ == "__main__":
    check_topojson_properties()
