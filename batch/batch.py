import csv
import os
import requests
from bs4 import BeautifulSoup


class ETDs:
    """An object to grab and store ETDs.

    Attributes:
        path (str): A web uri or file path that points at your URIs.

    """

    def __init__(self, path, web_request=True):
        """Initializes ETDS class.

        Args:
            path (str): A web uri or file path that points at your URIs.
            web_request (bool): Defaults to True. Defines whether you do a web request or file path request.

        """
        self.path = path
        if web_request is not True:
            self.contents = self.read_etds_from_disk(path)
        else:
            self.contents = self.read_etds_from_web(path)

    @staticmethod
    def read_etds_from_disk(filepath):
        our_new_files = []
        for filename in os.walk(filepath):
            our_new_files = filename[2]
        return our_new_files

    @staticmethod
    def read_etds_from_web(web_path):
        parsed_data = BeautifulSoup(requests.get(web_path).text, "html.parser")
        return [anchor.get("href") for anchor in parsed_data.find_all("a")]


class MetadataReader:
    """A Class to Read a Metadata CSV from Digital Commons.

    Attributes:
        file (str): The filename of the imported csv.
        etds (list): A list of ETDs to check for filenames against.
        bad_metadata (list): A list of metadata objects where no matching documents were found.
        urls (list): A list of URLs where a row matched a file in the given set of ETDs.

    """

    def __init__(self, filename, etds, web_path):
        """Initializes MetadataReader class.

        Args:
            filename (str): A CSV to read metadata from.
            etds (list): A list of ETDs to check against.

        """
        self.file = filename
        self.etds = etds
        self.web_path = self.__clean_web_path(web_path)
        self.bad_metadata = []
        self.urls = self.read_contents()

    @staticmethod
    def __clean_web_path(path):
        if path.endswith('/'):
            return path[:-1]
        else:
            return path

    def read_contents(self):
        """A method to read the last and first name from a spreadsheet.

        Returns:
            list: A list of strings.  If match found, a URL to the file.  If not, an empty string.

        Examples:
            >>> a_list_of_dissertations = ["BaggettMark_2050.pdf", "OmegaKenny_2029.pdf"]
            >>> MetadataReader("my_csv_file.csv", a_list_of_dissertations).read_contents()
            ['http://dlshare.lib.utk.edu/historical/2050etds/BaggettMark_2050.pdf', '']

        """
        with open(self.file, "r") as our_csv_file:
            reader = csv.reader(our_csv_file, delimiter="|")
            urls_for_spreadsheet = []
            for row in reader:
                try:
                    starting_text = f"{row[6].rstrip()}{row[4].rstrip()}"
                    my_url = ""
                    for dissertation in self.etds:
                        if dissertation.startswith(starting_text):
                            my_url = f"{self.web_path}/{dissertation}"
                    if my_url == "":
                        self.bad_metadata.append(f"{row[6]}{row[4]}")
                    urls_for_spreadsheet.append(my_url)
                except IndexError:
                    urls_for_spreadsheet.append("")
            return urls_for_spreadsheet

    def write_urls_to_file(self):
        """Writes urls to a text file.

        Returns:
            str: A message containing the number of urls that were written to current_urls.txt

        Examples:
            >>> a_list_of_dissertations = ["BaggettMark_2050.pdf", "OmegaKenny_2029.pdf"]
            >>> MetadataReader("my_csv_file.csv", a_list_of_dissertations).write_urls_to_file()
            'Wrote 2 records to current_urls.txt'
        """
        with open("current_urls.txt", "w") as output_text:
            for url in self.urls:
                output_text.write(f"{url}\n")
        return f"Wrote {len(self.urls)} records to current_urls.txt"
