import xml.etree.ElementTree as ET
import argparse
import os
import sys

def clean_strava_peloton_tcx(input_file, output_file=None):
    """
    Cleans up a Peloton to Strava TCX export file for better compatibility with Garmin Connect.
    - Removes leading/trailing whitespace from the file content.
    - Parses and re-serializes the XML to ensure well-formed structure.
    - Removes the <Creator> tag entirely.
    - Removes non-standard <Cadence> element directly under <Lap>.
    - Removes non-standard <Resistance> elements from trackpoint extensions.
    - Removes non-standard <TotalPower>, <AverageResistance>, and <MaximumResistance> from lap extensions.
    - Renames lap extension <TPX> to <LX> and renames child elements to standard names (e.g., AverageCadence to AvgCadence).
    - Rounds float values to integers for heart rate, cadence, calories, and watts where appropriate.
    
    Args:
        input_file (str): Path to the input Strava TCX file.
        output_file (str, optional): Path to the output cleaned file. If None, overwrites input.
    
    Returns:
        str: Path to the cleaned file.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found.")
    
    # Define namespaces URIs
    ns_tcx = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'
    ns_ext = 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'
    
    # Register namespaces for serialization: default for TCX, 'ae' for extensions to avoid any 'ns' prefix issues
    ET.register_namespace('', ns_tcx)
    ET.register_namespace('ae', ns_ext)
    
    # Namespaces dict for finding elements
    ns = {
        '': ns_tcx,
        'ae': ns_ext
    }
    
    # Read the file content and strip whitespace
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Parse the XML
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        if content.startswith('<?xml'):
            decl_end = content.find('?>') + 2
            content = content[decl_end:].strip()
        try:
            root = ET.fromstring(content)
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse XML: {e}")
    
    # Remove <Creator> from Activity
    activity = root.find(".//Activity", namespaces=ns)
    if activity is not None:
        creator = activity.find("Creator", namespaces=ns)
        if creator is not None:
            activity.remove(creator)
    
    # Process each Lap
    for lap in root.findall(".//Lap", namespaces=ns):
        # Remove <Cadence> directly under Lap
        cadence = lap.find("Cadence", namespaces=ns)
        if cadence is not None:
            lap.remove(cadence)
        
        # Round <Calories> to integer
        calories = lap.find("Calories", namespaces=ns)
        if calories is not None:
            try:
                calories.text = str(int(round(float(calories.text))))
            except ValueError:
                pass
        
        # Round AverageHeartRateBpm Value
        avg_hr = lap.find("AverageHeartRateBpm/Value", namespaces=ns)
        if avg_hr is not None:
            try:
                avg_hr.text = str(int(round(float(avg_hr.text))))
            except ValueError:
                pass
        
        # Round MaximumHeartRateBpm Value
        max_hr = lap.find("MaximumHeartRateBpm/Value", namespaces=ns)
        if max_hr is not None:
            try:
                max_hr.text = str(int(round(float(max_hr.text))))
            except ValueError:
                pass
        
        # Process Lap Extensions
        extensions = lap.find("Extensions", namespaces=ns)
        if extensions is not None:
            tpx = extensions.find("ae:TPX", namespaces=ns)
            if tpx is not None:
                # Change tag to LX
                tpx.tag = f"{{{ns_ext}}}LX"
                
                # Rename child elements and round values
                rename_map = {
                    'AverageCadence': 'AvgCadence',
                    'MaximumCadence': 'MaxCadence',
                    'AverageWatts': 'AvgWatts',
                    'MaximumWatts': 'MaxWatts'
                }
                to_remove = []
                for child in tpx:
                    child_tag = child.tag.split('}')[-1]
                    if child_tag in ['TotalPower', 'AverageResistance', 'MaximumResistance']:
                        to_remove.append(child)
                    elif child_tag in rename_map:
                        child.tag = f"{{{ns_ext}}}{rename_map[child_tag]}"
                    # Round child text to int if possible
                    if child.text:
                        try:
                            child.text = str(int(round(float(child.text))))
                        except ValueError:
                            pass
                for item in to_remove:
                    tpx.remove(item)
    
    # Process all Trackpoints
    for tp in root.findall(".//Trackpoint", namespaces=ns):
        # Round HeartRateBpm Value to integer
        hr_value = tp.find("HeartRateBpm/Value", namespaces=ns)
        if hr_value is not None:
            try:
                hr_value.text = str(int(round(float(hr_value.text))))
            except ValueError:
                pass
        
        # Round Cadence to integer
        cadence = tp.find("Cadence", namespaces=ns)
        if cadence is not None:
            try:
                cadence.text = str(int(round(float(cadence.text))))
            except ValueError:
                pass
        
        # Remove <Resistance> and round <Watts> in TPX
        extensions = tp.find("Extensions", namespaces=ns)
        if extensions is not None:
            tpx = extensions.find("ae:TPX", namespaces=ns)
            if tpx is not None:
                resistance = tpx.find("ae:Resistance", namespaces=ns)
                if resistance is not None:
                    tpx.remove(resistance)
                watts = tpx.find("ae:Watts", namespaces=ns)
                if watts is not None:
                    try:
                        watts.text = str(int(round(float(watts.text))))
                    except ValueError:
                        pass
    
    # Re-serialize the XML cleanly
    tree = ET.ElementTree(root)
    if output_file is None:
        output_file = input_file  # Overwrite original
    
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    
    print(f"Cleaned file saved to: {output_file}")
    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean Peloton to Strava TCX file for Garmin Connect compatibility.")
    parser.add_argument("input_file", help="Path to the input Strava TCX file")
    parser.add_argument("-o", "--output_file", help="Path to the output cleaned file (optional)")
    
    args = parser.parse_args()
    try:
        clean_strava_peloton_tcx(args.input_file, args.output_file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
pip install streamlit        
streamlit run FixTCXUI.py
