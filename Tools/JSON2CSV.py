import pandas as pd
import json

# Prompt user for input JSON file path
input_file = input("Enter the path to the JSON file: ")
output_file = 'output.csv'  # Desired output CSV file path

try:
    # Read the JSON file
    with open(input_file, 'r') as file:
        # Load all JSON objects
        data = []
        for line in file:
            data.append(json.loads(line.strip()))
    
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    df.to_csv(output_file, index=False)

    print(f"Converted {input_file} to {output_file} successfully.")

except Exception as e:
    print(f"An error occurred: {e}")