# John Wesley Thompson
# Created: 8/9/2025
# Last Edited: 6/18/20265
# flashcard.py

from typing import Final

IDEOGRAPHIC_SPACE: Final[str] = "\u3000"

class FlashCard:
    def __init__(self, word) -> None:
        self.writing: str = word[0]
        self.kana: str = word[1]
        self.definition = ""
        self.sentences = ""
        self.word_audio_filepath = ""
        self.sentence_audio_filepath = ""

    def __repr__(self) -> str:
        if self.writing:
            word = f"{self.writing}{IDEOGRAPHIC_SPACE}{self.kana}"
        else:
            word = f"{self.kana}"

        return (
            "--------------------\n"
            f"{word}\n"
            f"{self.definition}\n"
            f"{self.sentences}\n"
            f"{self.word_audio_filepath}\n"
            f"{self.sentence_audio_filepath}\n"
            "--------------------\n")

    @property
    def TSVString(self) -> str:
        word = f"{self.writing}{IDEOGRAPHIC_SPACE}{self.kana}" if self.writing else self.kana

        tsv_string = (f"{word}\t{self.definition}\t"
            f"{self.sentences}\t[sound:{self.word_audio_filepath}]\t"
            f"[sound:{self.sentence_audio_filepath}]")

        return tsv_string.replace('\n', "<br>")

    def isMissingFields(self) -> bool:
        # card can have no kanji if it has kana
        if (self.writing == "" and self.kana == "" or 
            self.kana == "" or
            self.definition == "" or
            self.sentences == "" or
            self.word_audio_filepath == "" or
            self.sentence_audio_filepath == ""):
            return True

        return False

    # def addPitch(self):
    #     pass


if __name__ == "__main__":

    both = FlashCard(("図書館", "としょかん"))
    nokanji = FlashCard(("", "こんにちは"))


    print(f"both: \n{both}")
    print(f"nokanji: \n{nokanji}")
    print("csv:")
    print(both.csv_string())
    print(nokanji.csv_string())

    print(f"'both' missing fields: {both.missingFields()}")
    print(f"'nokanji' missing fields: {nokanji.missingFields()}")

    both.definition = "library"
    both.sentences = "これはテストだ"
    both.audio_filepath = "ttsSounds/notreal/filepath"

    nokanji.definition = "hello"
    nokanji.sentences = "これもテスト"
    nokanji.audio_filepath = "ttsSounds/fake/filepath"

    print("with other members")
    print(f"both: \n{both}")
    print(f"nokanji: \n{nokanji}")
    print("csv:")
    print(both.csv_string())
    print(nokanji.csv_string())

    print(f"'both' missing fields: {both.missingFields()}")
    print(f"'nokanji' missing fields: {nokanji.missingFields()}")