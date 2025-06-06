import pandas as pd
import os
import glob
from charset_normalizer import from_path

folder_path = './'
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
dataframes = []

def detect_encoding(file_path):
    result = from_path(file_path).best()
    if result:
        return result.encoding
    return None

for file in csv_files:
    encoding = detect_encoding(file)
    if encoding:
        try:
            df = pd.read_csv(file, encoding=encoding, dtype=str, on_bad_lines='skip')
            print(f"✅ Successfully read {file} with encoding: {encoding}")
            dataframes.append(df)
        except Exception as e:
            print(f"❌ Failed to read {file} with detected encoding {encoding}: {e}")
    else:
        print(f"⚠️ Could not detect encoding for {file}")

if dataframes:
    merged_df = pd.concat(dataframes, ignore_index=True, sort=False)
    merged_df.to_csv('merged_output.csv', index=False, encoding='utf-8-sig')
    print(f"✅ Merged {len(dataframes)} files into 'merged_output.csv'")
else:
    print("❌ No files were successfully read and merged.")
