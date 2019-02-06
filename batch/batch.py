import csv
import os


class Dissertations:
    def __init__(self, filepath):
        self.path = filepath
        self.contents = self.read_etds(filepath)

    @staticmethod
    def read_etds(path):
        for filename in os.walk(path):
            our_new_files = filename[2]
        return our_new_files


class MetadataReader:
    def __init__(self, filename, etds):
        self.file = filename
        self.etds = etds
        self.rows = self.read_contents()

    def read_contents(self):
        with open(self.file, 'r') as our_csv_file:
            reader = csv.reader(our_csv_file, delimiter="|")
            urls_for_spreadsheet = []
            for row in reader:
                try:
                    starting_text = f"{row[6]}{row[4]}"
                    for dissertation in self.etds:
                        if dissertation.startswith(starting_text):
                            del row[1]
                            row.insert(1, f"http://dlshare.lib.utk.edu/historical/{dissertation}")
                    urls_for_spreadsheet.append(row)
                except IndexError:
                    print("error")
            return urls_for_spreadsheet


if __name__ == "__main__":
    dissertations = Dissertations("/home/mark/PycharmProjects/historical_etds/data/2003disserations").contents
    MetadataReader("/home/mark/PycharmProjects/historical_etds/mark_test_2003_dissertations.csv", dissertations).rows
