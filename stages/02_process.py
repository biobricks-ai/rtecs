import os
import time
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm
from xml.etree import ElementTree
import gzip
import tempfile

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
        

# TODO TRANSFORM the xml file into a set of dataframes
