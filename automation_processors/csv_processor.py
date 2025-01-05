import csv

def read_csv(file_path):
    """Read the input CSV file."""
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]