from consts import *
from podcast_utils import *

from os import listdir
import spacy
from spacy.language import Language
from spacy.tokens import Doc
from typing import Generator


def get_book_schema() -> dict:
    """
    Load the book JSON schema into an object
    """
    with open(BOOK_SCHEMA_PATH, 'r') as read_file:
        schema = json.load(read_file)
    return schema


def get_transcript_path(transcript_name: str) -> str:
    """
    Get full path to transcript
    """
    path = TRANSCRIPTS_DIR_PATH + "/" + transcript_name
    return path


def get_transcript_name(num: int) -> str:
    """
    Get transcript file name by number/ID
    """
    name = TRANSCRIPT_NAME_PREFIX + \
        str(num) + TRANSCRIPT_NAME_SUFFIX
    return name


def get_transcript_num(fname: str) -> int:
    """
    Get transcript number from name
    """
    num = ''.join([c for c in fname if c.isdigit()])
    return int(num)


def get_transcript_files_gen() -> Generator:
    """
    Return generator for all transcripts full paths
    """
    path = TRANSCRIPTS_DIR_PATH + '/'
    files = listdir(path)
    file_paths_gen = (path + f for f in files)
    return file_paths_gen


def init_spacy() -> Language:
    """
    Initaliaze spacy
    """
    nlp = spacy.load("en_core_web_sm")
    return nlp


def tokenize_transcript(nlp: Language, transcript: str) -> Doc:
    """
    Tokenize podcast transcript; returns spacy document
    """
    doc = nlp(transcript)
    return doc


def get_book_recommendations(fname: str):
    """
    Get book recommendations from podcast transcript
    """
    book = get_book_schema()

    book['id'] = get_transcript_num(fname)
    book['recomendations'] = []

    return book


def main():
    files = get_transcript_files_gen()

    book_map = dict()
    for f in files:
        book = get_book_recommendations(f)
        id = book['id']
        book_map[id] = book

    book_map = dict(sorted(book_map.items(), reverse=True))

    with open(BOOKS_OUTPUT_PATH, 'w') as f:
        json.dump(book_map, f)


if __name__ == "__main__":
    main()