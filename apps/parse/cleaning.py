"""Function for data cleaning."""

from collections import Counter
from typing import List


def normalized_category_names(names: List[str]) -> List[str]:
    return [name.lower().replace("_", " ") for name in names]


def without_common_prefix(words):
    """Returns the list of strings with the common prefix."""
    cnt = Counter()
    for word in words:
        if not word:
            return words
        cnt[word[0]] += 1
    first_letter = list(cnt)[0]

    filter_list = [word for word in words if word[0] == first_letter]
    filter_list.sort(key=lambda s: len(s))  # To avoid iob

    prefix = ""
    length = len(filter_list[0])
    for i in range(length):
        test = filter_list[0][i]
        if all([word[i] == test for word in filter_list]):
            prefix += test
        else:
            break
    return [word[len(prefix) :] if word.startswith(prefix) else word for word in words]
