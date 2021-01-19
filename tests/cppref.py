import glob
import os


def get_directory_files(query, directory):
    for file in glob.iglob(f"{directory}/*", recursive=True):
        if not query.lower() in file.lower():
            continue
        yield f'http://en.cppreference.com/w/{file.replace("/src/cppref", "")}'
        if not os.path.isdir(file):
            continue
        yield from get_directory_files(query, file)


def get_corresponding_files(query: str, language: str):
    if query.startswith("std::"):
        query = query.replace("std::", "")

    query = query.replace("::", "/")
    output = []
    to_queue = list(get_directory_files(query, f"src/cppref/{language}/**"))
    for index, each in enumerate(to_queue):
        if each.endswith(".html"):
            continue
        output.append(
            to_queue.pop(index))

    output.extend(to_queue)
    return output


search = ""
search = input("Input: ")


def cppref(query: str):
    """Search something on cppreference"""
    results = get_corresponding_files(query, "cpp")

    url = f'http://en.cppreference.com/w/cpp/index.php?title=Special:Search?search={query}'

    special_pages = []
    description = []
    q = query.replace('std::', '')

    if os.path.isdir(f"src/cppref/cpp/{q}"):
        description.append(
            f"[`std::{q}`](http://en.cppreference.com/w/cpp/{q})")

    for _, result in enumerate(results):
        check_name = result.replace(
            "http://en.cppreference.com/w/", "")
        check_name = check_name.replace("\\", "/")
        # print(check_name)

        check_name = check_name.replace("src/cppref/cpp/", "")
        # print(check_name)
        f_name = check_name.replace("/", "::")
        f_name = f_name.replace(".html", "")

        if check_name.startswith(("language", "concept")) and not check_name.startswith("concepts"):
            special_pages.append(
                f'[`{f_name}`]({result})')
            continue

        description.append(
            f'[`std::{f_name}`]({result})')

    if len(special_pages) > 0:
        print('Language Results')
        print('\n'.join(
            special_pages))
        if len(description):
            print('Library Results')
            print('\n'.join(
                description[:10]))
    else:
        if not len(description):
            return print('No results found.')

        desc_str = '\n'.join(description[:15])
        print('Search Results')
        print(desc_str)

    print('See More')
    print(f'[`{query}` results]({url})')


def cref(query: str):
    """Search something on cppreference"""
    results = get_corresponding_files(query, "c")

    url = f'http://en.cppreference.com/w/c/index.php?title=Special:Search?search={query}'

    special_pages = []
    description = []

    # No need to replace std:: with "" since this is a c reference search
    if os.path.isdir(f"src/cppref/c/{query}"):
        description.append(
            f"[`{query}`](http://en.cppreference.com/w/c/{query})")

    for _, result in enumerate(results):
        check_name = result.replace("http://en.cppreference.com/w/", "")

        check_name = check_name.replace(
            "\\", "/")
        # print(check_name)

        f_name = check_name.replace(".html", "")
        f_name = f_name.replace("src/cppref/c/", "")

        if check_name.startswith(("language", "concept")) and not check_name.startswith("concepts"):
            special_pages.append(
                f'[`{f_name}`]({result})')
            continue

        description.append(
            f'[`{f_name}`]({result})')

    if len(special_pages) > 0:
        print('Language Results')
        print('\n'.join(
            special_pages))
        if len(description):
            print('Library Results')
            print('\n'.join(
                description[:10]))
    else:
        if not len(description):
            return print('No results found.')

        desc_str = '\n'.join(description[:15])
        print('Search Results')
        print(desc_str)

    print('See More')
    print(f'[`{query}` results]({url})')


cref(search)
