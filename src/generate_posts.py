from consts import *

import json
from pytablewriter import MarkdownTableWriter


def load_podcasts() -> dict:
    """
    Load the podcast list JSON into an object
    """
    podcasts_path = PODCASTS_OUTPUT_PATH
    with open(podcasts_path, 'r') as read_file:
        podcasts = json.load(read_file)
    return podcasts


def load_books() -> dict:
    """
    Load the books list JSON into an object
    """
    books_path = BOOKS_OUTPUT_PATH
    with open(books_path, 'r') as read_file:
        books = json.load(read_file)
    return books


def get_post_filename(id):
    name = POSTS_OUTPUT_PATH + '/' + POST_NAME_PREFIX + id + POST_NAME_SUFFIX
    return name


def create_post_file(id):
    name = get_post_filename(id)
    f = open(name, 'w')
    return f


def write_yaml_block(file, podcast):
    block = '---\n'

    file.write(block)
    # Body of block
    title = 'title: ' + '"' + podcast['title'] + '"\n'
    file.write(title)

    # TODO: Remove line breaks better in description (breaks the YAML)
    description = 'description: |\n' + "  " + podcast['description'] + '"\n'
    file.write(description)

    # TODO
    # thumbnail_path = 'thumb: ' + '\'' + thumbnail_path + '\''
    thumbnail_path = 'thumb: ' + '"' + "" + '"\n'
    file.write(thumbnail_path)

    # TODO: Wasn't working with 11ty template
    # date = 'date: ' + '"' + podcast['date'] + '"\n'
    # file.write(date)

    # TODO
    # tags = 'tags: '
    # file.write(tags)
    # for tag in tag_list:
    #     prefix = "   - "
    #     tag = prefix + '\'' + tag + '\''
    #     file.write(tag)

    file.write(block)


def write_podcast_info(file, podcast):
    heading = '\n# ' + podcast['title'] + '\n\n'
    file.write(heading)

    date = '  - Date: ' + podcast['date'] + '\n'
    file.write(date)
    date = '  - Link: ' + podcast['url'] + '\n'
    file.write(date)
    date = '  - Description: ' + podcast['description'] + '\n'
    file.write(date)


def write_book_recommendations(file, recommendations):
    heading = '\n## Book Recommendations\n\n'
    file.write(heading)
    file.write(str(recommendations))
    # TODO
    # writer = MarkdownTableWriter(
    #     table_name="example_table",
    #     headers=["int", "float", "str", "bool", "mix", "time"],
    #     value_matrix=[
    #         [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
    #     ],
    # )
    # writer.write_table()
    # writer.close()


def main():
    podcasts = load_podcasts()
    books_list = load_books()

    for id, books in books_list.items():
        # Skip if no corresponding podcast
        if id not in podcasts:
            continue

        recommendations = books['recommendations']
        podcast = podcasts[id]

        # Create file
        file = create_post_file(id)

        write_yaml_block(file, podcast)

        write_podcast_info(file, podcast)

        write_book_recommendations(file, recommendations)

        file.close()


if __name__ == "__main__":
    main()