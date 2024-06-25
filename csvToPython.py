import csv
import pprint

def csv_to_dict(file_path):
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        result = {}
        for row in csv_reader:
            for key, value in row.items():
                if key not in result:
                    result[key] = []
                result[key].append(value)
    return result

# Example usage
file_path = 'dk.csv'
data_dict = csv_to_dict(file_path)
for player in data_dict:
    pprint.pprint(player)
