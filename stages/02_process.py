import os
import pandas as pd
from xml.etree import ElementTree
import gzip

# Function to parse XML and extract data
def parse_xml_to_df(xml_path):
    tree = ElementTree.parse(xml_path)
    root = tree.getroot()
    
    data = []
    
    for record in root.findall('Record'):
        record_dict = {}
        
        # Extract RTECSNumber
        rtecs_number = record.find('.//RTECSNumber')
        record_dict['RTECSNumber'] = rtecs_number.text if rtecs_number is not None else None
        
        # Extract CASRegistryNumber
        cas_number = record.find('.//CASRegistryNumber')
        record_dict['CASRegistryNumber'] = cas_number.text if cas_number is not None else None
        
        # Store the entire Record as a string
        record_dict['xmlRecord'] = ElementTree.tostring(record, encoding='unicode')
        
        data.append(record_dict)
    
    return pd.DataFrame(data)

# Get path relative to cwd
xml_files = [f for f in os.listdir('download') if f.endswith('.xml.gz')]
xml_files = [os.path.join('download', f) for f in xml_files]

# Assume only one xmlgz
xmlgz = xml_files[0]  # This is download/rtecs_...xml.gz

# Unzip to temporary directory
os.makedirs('temp', exist_ok=True)
xml_path = os.path.join('temp', 'temp.xml')
with gzip.open(xmlgz, 'rb') as f_in:
    with open(xml_path, 'wb') as f_out:
        f_out.write(f_in.read())

# Parse XML and convert to DataFrame
df = parse_xml_to_df(xml_path)
# make a folder called brick if not exist

# Save DataFrame to Parquet 
output_file = 'rtecs_records.parquet'
# Have output_file saved 
df.to_parquet(output_file)
print(f"Data compiled and saved to {output_file}")

# Display the first few rows of the DataFrame
print(df.head())
