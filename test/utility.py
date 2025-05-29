import csv
import json
import os
import re
import html # For unescaping HTML entities
import urllib.parse # For unescaping URL-encoded characters

def clean_text_for_csv(text: str) -> str:
    if not isinstance(text, str):
        return text 
    cleaned_text = urllib.parse.unquote(text)
    cleaned_text = html.unescape(cleaned_text)
    cleaned_text = re.sub(r'\s*\n\s*', '\n', cleaned_text).strip()
    cleaned_text = cleaned_text.strip()
    return cleaned_text

def convert_json_file_to_csv(input_json_filepath: str, output_csv_filepath: str, encoding: str = 'utf-8'):
    try:
        with open(input_json_filepath, 'r', encoding=encoding) as json_file:
            data = json.load(json_file) 
        if not data:
            print(f"Warning: JSON data in '{input_json_filepath}' is empty. No CSV file will be created.")
            return
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            print("Error: JSON data in the file must be a list of objects or a single object.")
            return
        processed_data = []
        for row in data:
            cleaned_row = {}
            for key, value in row.items():
                if key == "job_description" and isinstance(value, str):
                    cleaned_row[key] = clean_text_for_csv(value)
                elif key == "skills" and isinstance(value, list):
                    cleaned_row[key] = ", ".join(value)
                elif isinstance(value, str):
                    cleaned_row[key] = clean_text_for_csv(value)
                else:
                    cleaned_row[key] = value
            processed_data.append(cleaned_row)
        fieldnames = processed_data[0].keys()
        with open(output_csv_filepath, 'w', newline='', encoding=encoding) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader() 
            writer.writerows(processed_data)  
        print(f"Successfully converted '{input_json_filepath}' to CSV: '{output_csv_filepath}'")
    except FileNotFoundError:
        print(f"Error: The input JSON file '{input_json_filepath}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data from '{input_json_filepath}': {e}")
    except IOError as e:
        print(f"Error writing CSV file '{output_csv_filepath}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    job_roles = [
        "Data Engineer",
        "Data Analyst",
        "Data Architect",
        "Data Scientist",
        "Machine Learning Engineer"
    ]
    for role in job_roles:
        input_json_file = f"{role.replace(' ','_').lower()}_output.json"
        output_csv_file = f"{role.replace(' ','_').lower()}_output.csv"
        print("\n--- Running Conversion ---")
        convert_json_file_to_csv(input_json_file, output_csv_file)
        if os.path.exists(output_csv_file):
            print(f"CSV file '{output_csv_file}' is created.")
        else:
            print(f"CSV file '{output_csv_file}' was not created.")