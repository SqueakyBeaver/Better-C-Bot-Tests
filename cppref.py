import glob
import os


def get_directory_files(query, directory):
    for file in glob.iglob(f"{directory}/*"):
        if not query.lower() in file.lower():
            continue
        yield f"http://en.cppreference.com/w/{file[2:]}"
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
        check_name = result.replace("http://en.cppreference.com/w/cpp", "src")
        check_name = result.replace("http://en.cppreference.com/w/c", "src")

        check_name = check_name.replace("\\", "/")
        print(check_name)

        if check_name.startswith("src/cppref/cpp/container"):
            check_name = check_name[:5] + check_name[15:]

        if check_name.startswith("src/cppref/cpp/algorithm"):
            check_name = check_name[:5] + check_name[15:]

        if check_name.startswith("src/cppref/cpp/memory"):
            check_name = check_name[:5] + check_name[12:]

        check_name = check_name.replace("src/cppref/cpp/", "")
        check_name = check_name.replace("src/cppref/c/", "")
        print(check_name)
        f_name = check_name.replace("\\", "::").replace(".html", "")

        if check_name.startswith(("language", "concept")) and not check_name.startswith("concepts"):
            special_pages.append(
                f'[`{f_name.replace("/", "::")}`]({result})')
            continue

        description.append(
            f'[`std::{f_name.replace("/", "::")}`]({result})')

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

    url = f'http://en.cppreference.com/w/cpp/index.php?title=Special:Search?search={query}'

    special_pages = []
    description = []
    q = query.replace('std::', '')

    if os.path.isdir(f"src/cppref/cpp/{q}"):
        description.append(
            f"[`std::{q}`](http://en.cppreference.com/w/cpp/{q})")

    for _, result in enumerate(results):
        check_name = result.replace("http://en.cppreference.com/w/cpp", "src")
        check_name = result.replace("http://en.cppreference.com/w/c", "src")

        check_name = check_name.replace("\\", "/")
        print(check_name)

        if check_name.startswith("src/cppref/cpp/container"):
            check_name = check_name[:5] + check_name[15:]

        if check_name.startswith("src/cppref/cpp/algorithm"):
            check_name = check_name[:5] + check_name[15:]

        if check_name.startswith("src/cppref/cpp/memory"):
            check_name = check_name[:5] + check_name[12:]

        check_name = check_name.replace("src/cppref/cpp/", "")
        check_name = check_name.replace("src/cppref/c/", "")
        print(check_name)
        f_name = check_name.replace("\\", "::").replace(".html", "")

        if check_name.startswith(("language", "concept")) and not check_name.startswith("concepts"):
            special_pages.append(
                f'[`{f_name.replace("/", "::")}`]({result})')
            continue

        description.append(
            f'[`std::{f_name.replace("/", "::")}`]({result})')

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
