import glob
import os

repeat_namespaces = ["experimental", "chrono", "filesystem"]


def get_libs_list(language: str):
    with open(f"src/cppref/{language}libs.txt", "r") as libs:
        for item in libs:
            if " " in item:
                # The [:-1] is to remove the '\n' written to the end of each line
                yield item[:-1].split(" ")


def get_language_list(language: str):
    with open(f"src/cppref/{language}lang.txt", "r") as lang:
        for item in lang:
            if " " in item:
                yield item[:-1].split(" ")


def find_results(language: str, query: str):
    libs = get_libs_list(language)
    lang = get_language_list(language)

    res = {"language": [], "libs": []}

    count = 0
    for path in lang:
        if count >= 5:
            break
        if query.lower() in path:
            count += 1
            res["language"].append(path)

    count = 0
    for path in libs:
        if count >= 5:
            break
        if query.lower() in path:
            count += 1
            res["libs"].append(path)

    return res


def cppref(query: str):
    """Search something on cppreference"""

    results = find_results("cpp", query)

    url = f'https://en.cppreference.com/mwiki/index.php?title=Special%3ASearch&search={query}'

    lang_results = []
    lib_results = []

    for i in results["language"]:
        lang_results.append(
            f"[`({i[0]}) {'/'.join(i[1:])}`](http://en.cppreference.com/w/cpp/{'/'.join(i)})")

    for i in results["libs"]:
        if i[0] in repeat_namespaces:
            lib_results.append(
                f"[`({i[0]}) std::{'::'.join(i)}`](http://en.cppreference.com/w/cpp/{'/'.join(i)})")
            continue
        lib_results.append(
            f"[`({i[0]}) std::{'::'.join(i[1:])}`](http://en.cppreference.com/w/cpp/{'/'.join(i)})")

    print("\nLanguage Results:\n")
    print("\n".join(lang_results))
    print("\nLibrary Results:\n")
    print("\n".join(lib_results))

    print("Didn't find what you were looking for?")
    print(f'See more [`{query}` results]({url})')


def cref(query: str):
    """Search something on cppreference"""

    results = find_results("c", query)

    url = f'https://en.cppreference.com/mwiki/index.php?title=Special%3ASearch&search={query}'

    lang_results = []
    lib_results = []

    for i in results["language"]:
        lang_results.append(
            f"[`({i[0]}) {'/'.join(i[1:])}`](http://en.cppreference.com/w/c/{'/'.join(i)})")

    for i in results["libs"]:
        lib_results.append(
            f"[`({'/'.join(i[:-1])}) {i[-1]}`](http://en.cppreference.com/w/c/{'/'.join(i)})")

    print("\nLanguage Results:\n")
    print("\n".join(lang_results))
    print("\nLibrary Results:\n")
    print("\n".join(lib_results))

    print("Didn't find what you were looking for?")
    print(f'See more [`{query}` results]({url})')


search = ""
search = input("Input: ")
cppref(search)
