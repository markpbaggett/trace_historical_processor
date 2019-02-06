import csv
import os


class Dissertations:
    def __init__(self, filepath):
        self.path = filepath
        self.contents = self.read_etds(filepath)

    @staticmethod
    def read_etds(path):
        our_new_files = []
        for filename in os.walk(path):
            our_new_files = filename[2]
        return our_new_files


class MetadataReader:
    def __init__(self, filename, etds):
        self.file = filename
        self.etds = etds
        self.bad_metadata = []
        self.urls = self.read_contents()

    def read_contents(self):
        with open(self.file, "r") as our_csv_file:
            reader = csv.reader(our_csv_file, delimiter="|")
            urls_for_spreadsheet = []
            for row in reader:
                try:
                    starting_text = f"{row[6].rstrip()}{row[4].rstrip()}"
                    my_url = ""
                    for dissertation in self.etds:
                        if dissertation.startswith(starting_text):
                            my_url = (
                                f"http://dlshare.lib.utk.edu/historical/{dissertation}"
                            )
                    if my_url == "":
                        self.bad_metadata.append(f"{row[6]}{row[4]}")
                    urls_for_spreadsheet.append(my_url)
                except IndexError:
                    urls_for_spreadsheet.append("")
            return urls_for_spreadsheet

    def write_urls_to_file(self):
        with open("current_urls.txt", "w") as output_text:
            for url in self.urls:
                output_text.write(f"{url}\n")


if __name__ == "__main__":
    dissertations = Dissertations(
        "/home/mark/PycharmProjects/historical_etds/data/2003disserations"
    ).contents
    MetadataReader(
        "/home/mark/PycharmProjects/historical_etds/mark_test_2003_dissertations.csv",
        dissertations,
    ).write_urls_to_file()
