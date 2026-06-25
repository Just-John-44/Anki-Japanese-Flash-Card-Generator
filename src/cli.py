# createcards.py
# Last Edited: 6/25/2026
# Author: John Wesley Thompson

from flash_card import FlashCard, Word
from sentence_generator import OpenAISentenceGenerator
from services.setup_service import SetupService
from services.flash_card_service import FlashCardService

import sqlite3
from pathlib import Path
import argparse
import sys


def main():
    args = parse_cli_args()

    if args.command == "setup":
        SetupService().run()
        return

    if not Path("data/jmdict.db").is_file():
        print("Database not found. Run 'createcards setup' to set up the database.")
        sys.exit(1)

    try:
        vocab = read_vocab_file(args.input_file)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        sys.exit(1)

    # FlashCardService setup
    db_conn = sqlite3.connect("data/jmdict.db")
    db_conn.row_factory = sqlite3.Row
    generator = OpenAISentenceGenerator(model="gpt-4o-mini")
    fc_service = FlashCardService(db_conn, generator)

    flash_cards = fc_service.create_flash_cards(vocab)

    db_conn.close()

    # create tsv file
    with open(args.output_file, "w") as deck_file:
        for card in flash_cards:
            print(card.tsv_string, file=deck_file)

    print("\ntsv file created. Don't forget to add any missing values for\n"
          "definitions that were listed as issues. Possible reasons for\n"
          "issues:\n"
          "\n"
          "- Provided a spelling for a word but no reading\n"
          "    example: 猫 (not followed by a space and ねこ)\n"
          "- Provided a word that is not in the database or is misspelled\n"
    )


def text_file(path_str: str) -> Path:
    path = Path(path_str)

    if path.suffix != ".txt" and path.suffix != ".text":
        raise argparse.ArgumentTypeError("Input file must be a text file.")

    return path


# def apkg_file(path_str: str) -> Path:
#     path = Path(path_str)

#     if path.suffix != ".apkg":
#         raise argparse.ArgumentTypeError("Output file must be an apkg file.")

#     return path

def tsv_file(path_str: str) -> Path:
    path = Path(path_str)

    if path.suffix != ".tsv":
        raise argparse.ArgumentTypeError("Output file must me a tsv file.")

    return path


def parse_cli_args() -> argparse.Namespace:
    cli_parser = argparse.ArgumentParser()
    cli_subparsers = cli_parser.add_subparsers(dest="command", required=True)

    cli_setup_parser = cli_subparsers.add_parser("setup")

    cli_generate_parser = cli_subparsers.add_parser("generate")
    cli_generate_parser.add_argument("input_file", type=text_file)
    cli_generate_parser.add_argument("output_file", type=tsv_file)

    return cli_parser.parse_args()



def read_vocab_file(filename: Path) -> list[Word]:
        try:
            with filename.open("r", encoding='utf-8') as vocab_file:
                lines = vocab_file.readlines()

        except FileNotFoundError:
            raise FileNotFoundError(f"file '{filename}' not found.")

        for i, line in enumerate(lines):
            line = line.strip().split()

            if len(line) > 2:
                raise ValueError(f"line {line} is invalid input. Only 2 fields should be provided")

            elif len(line) == 1:
                line.insert(0, "")

            lines[i] = Word(line[0], line[1])

        return lines


if __name__ == "__main__":
    main()
