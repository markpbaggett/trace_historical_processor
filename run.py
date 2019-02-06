import argparse
from emoji import emojize
from batch.batch import ETDs, MetadataReader


def main():
    help_string = emojize(
        f":snake::snake::snake: Find URLs for ETDs with Python. :snake::snake::snake:"
    )
    parser = argparse.ArgumentParser(description=help_string)
    parser.add_argument(
        "-e",
        "--etds",
        dest="etds_path",
        help="Specify path to your ETDs.",
        required=True,
    )
    parser.add_argument(
        "-c", "--csv", dest="csv_path", help="Specify path to your CSV.", required=True
    )
    parser.add_argument(
        "-t",
        "--type",
        dest="etds_path_type",
        default="WEB",
        help="Specify WEB or FILE for etds path. Defaults to WEB",
    )
    args = parser.parse_args()

    if args.etds_path_type != "WEB":
        etd_path = False
    else:
        etd_path = True
    etds = ETDs(args.etds_path, etd_path).contents
    processor = MetadataReader(args.csv_path, etds)
    print(f"\n{processor.write_urls_to_file()}\n")
    print(f"Could not match on these values:\n{processor.bad_metadata}")
    return


if __name__ == "__main__":
    main()
