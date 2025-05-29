import csv
import json
import os
import re
import html 
import urllib.parse 

def clean_text_for_csv(text: str) -> str:
    if not isinstance(text, str):
        return text 
    cleaned_text = urllib.parse.unquote(text)
    cleaned_text = html.unescape(cleaned_text)
    cleaned_text = re.sub(r'\s*\n\s*', '\n', cleaned_text).strip()
    cleaned_text = cleaned_text.strip()
    return cleaned_text

def save_dicts_to_csv(data: list[dict], filename: str, encoding: str = 'utf-8'):
    if not data:
        print("No data to write.")
        return
    processed_data = []
    for row in data:
        cleaned_row = {}
        for key, value in row.items():
            if isinstance(value, str):
                cleaned_row[key] = clean_text_for_csv(value)
            elif isinstance(value, list):
                cleaned_row[key] = ", ".join(map(str, value)) 
            else:
                cleaned_row[key] = value
        processed_data.append(cleaned_row)
    fieldnames = processed_data[0].keys()

    try:
        with open(filename, 'w', newline='', encoding=encoding) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()  
            writer.writerows(processed_data) 
        print(f"Data successfully saved to {filename}")
    except IOError as e:
        print(f"Error writing CSV file '{filename}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def save_dicts_to_json(data, filename):
    """
    Saves a list of dictionaries to a JSON file.

    Args:
        data (list): The list of dictionaries to save.
        filename (str): The name of the output JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4) 

    print(f"Data successfully saved to {filename}")
