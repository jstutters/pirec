import os
import csv

class CSVFile(object):
    def __init__(self, path, values):
        self.path = path
        self.values = values

    def write(self, results):
        field_names = self.values.keys()
        write_header = not os.path.exists(self.path)
        with open(self.path, 'a') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=field_names)
            if write_header:
                writer.writeheader()
            row = {}
            for field in self.values:
                row[field]= self.values[field](results)
            writer.writerow(row)
