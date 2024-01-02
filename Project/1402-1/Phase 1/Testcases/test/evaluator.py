import re
import os
import logging
import subprocess

LINE_PATTERN = re.compile(r"(?P<linenum>\d+)\.\s*(?P<content>.+)")
ERROR_PATTERN = re.compile(
    r"\(\s*(?P<token>\S+)\s*,\s*(?P<message>[^)]+)\s*\)")
TOKEN_PATTERN = re.compile(
    r"\(\s*(?P<type>NUM|ID|KEYWORD|SYMBOL)\s*,\s*(?P<token>.+?)\)")


def calc_alignment_score(first, second, del_penalty=-1, edit_penalty=-1, match_score=0):
    dp = [[(0, -1) for j in range(len(second) + 1)]
          for i in range(len(first) + 1)]

    # These are used for tracking the comparison decisions
    FDEL = 0
    SDEL = 1
    MATCH = 2

    calc_del_penalty = del_penalty
    calc_edit_penalty = edit_penalty
    calc_match_score = match_score

    if isinstance(del_penalty, int):
        def calc_del_penalty(x): return del_penalty

    if isinstance(edit_penalty, int):
        def calc_edit_penalty(x, y): return edit_penalty

    if isinstance(match_score, int):
        def calc_match_score(x, y): return match_score

    for i in range(1, len(first) + 1):
        dp[i][0] = (calc_del_penalty(first[i - 1]) * i, FDEL)

    for j in range(1, len(second) + 1):
        dp[0][j] = (calc_del_penalty(second[j - 1]) * j, SDEL)

    dp[0][0] = (0, -1)

    for i in range(1, len(first) + 1):
        for j in range(1, len(second) + 1):
            dp[i][j] = max(
                [
                    (dp[i - 1][j][0] + calc_del_penalty(first[i - 1]), FDEL),
                    (dp[i][j - 1][0] + calc_del_penalty(second[j - 1]), SDEL),
                    (dp[i - 1][j - 1][0] +
                     (calc_match_score(first[i - 1], second[j - 1])
                      if first[i - 1] == second[j - 1]
                      else calc_edit_penalty(first[i - 1], second[j - 1])),
                     MATCH)
                ],
                key=lambda x: x[0])

    return dp[len(first)][len(second)][0]


def extract_line_parts(line: str):
    m = LINE_PATTERN.match(line)
    if m:
        return m.groupdict()
    else:
        return {"linenum": -1, "content": ""}


def convert_to_list(text: str, extractor):
    return [extractor(line) for line in text.splitlines() if line]


def calc_line_content_del_penalty(x):
    return -(1 + len(x[1]))


def calc_line_content_edit_penalty(x, y):
    penalty = 0
    if x[0] != y[0]:
        penalty -= 1

    return penalty + calc_alignment_score(
        x[1], y[1],
        del_penalty=lambda x: -len(x),
        edit_penalty=lambda x, y: sum(0 if a == b else -1 for a, b in zip(x, y)))


def calc_score(expected: str, actual: str, extractor, del_penalty, edit_penalty):
    expected = convert_to_list(expected, extractor)
    actual = convert_to_list(actual, extractor)
    return calc_alignment_score(
        expected, actual, del_penalty=del_penalty, edit_penalty=edit_penalty)


def calc_symbol_table_score(expected: str, actual: str):
    def extract_symbols(text: str):
        return extract_line_parts(text)["content"]

    expected = set(convert_to_list(expected, extract_symbols))
    actual = set(convert_to_list(actual, extract_symbols))
    return -len(expected ^ actual)


def calc_lexical_errors_score(expected: str, actual: str):
    def extract_parts(text: str):
        line_parts = extract_line_parts(text)
        errors = [(d["token"], d["message"]) for d in
                  [m.groupdict() for m in ERROR_PATTERN.finditer(line_parts["content"])]]

        return line_parts["linenum"], errors

    return calc_score(
        expected, actual,
        extract_parts,
        del_penalty=calc_line_content_del_penalty,
        edit_penalty=calc_line_content_edit_penalty)


def calc_tokens_score(expected: str, actual: str):
    def extract_parts(text: str):
        line_parts = extract_line_parts(text)
        tokens = [(d["type"], d["token"]) for d in
                  [m.groupdict() for m in TOKEN_PATTERN.finditer(line_parts["content"])]]

        return (line_parts["linenum"], tokens)

    return calc_score(
        expected, actual,
        extract_parts,
        del_penalty=calc_line_content_del_penalty,
        edit_penalty=calc_line_content_edit_penalty)


def calc_test_score(test_name):
    subprocess.call(['cp', 'test/testcases/' + test_name + '/input.txt', 'input.txt'])
    remove_files = ["lexical_errors.txt", "symbol_table.txt", "tokens.txt"]
    for file_name in remove_files:
        if os.path.exists(file_name):
            os.remove(file_name)

    subprocess.call(['python', 'compiler.py'])
    with open(file='test/testcases/' + test_name + '/lexical_errors.txt', mode="r") as f:
        expected_errors = f.read()
    with open(file='test/testcases/' + test_name + '/symbol_table.txt', mode="r") as f:
        expected_symbols = f.read()
    with open(file='test/testcases/' + test_name + '/tokens.txt', mode="r") as f:
        expected_tokens = f.read()
    with open(file='lexical_errors.txt', mode="r") as f:
        errors = f.read()
    with open(file='symbol_table.txt', mode="r") as f:
        symbols = f.read()
    with open(file='tokens.txt', mode="r") as f:
        tokens = f.read()
    score1 = calc_tokens_score(expected_tokens, tokens)
    score2 = calc_symbol_table_score(expected_symbols, symbols)
    score3 = calc_lexical_errors_score(expected_errors, errors)
    print(test_name, "-->", score1, score2, score3)
    return score1, score2, score3


# print(calc_tokens_score(
#     """
# 1.	(KEYWORD, void) (ID, min) (SYMBOL, () (KEYWORD, void) (SYMBOL, )) (SYMBOL, {)
# 2.	(KEYWORD, for) (KEYWORD, int) (ID, j0) (SYMBOL, ;) (NUM, 2) (SYMBOL, :) (NUM, 90) (SYMBOL, )) (SYMBOL, {)
# 3.	(ID, output) (SYMBOL, () (ID, v) (SYMBOL, )) (SYMBOL, ;)
# 4.	(SYMBOL, })
# 6.	(ID, i)
# 7.	(KEYWORD, switch) (SYMBOL, () (ID, arr) (SYMBOL, [) (ID, g) (SYMBOL, ]) (SYMBOL, )) (SYMBOL, {)
# 8.	(KEYWORD, case) (NUM, 2) (SYMBOL, :)
# 9.	(ID, b) (SYMBOL, ==) (SYMBOL, ==) (SYMBOL, =) (ID, b) (SYMBOL, +) (NUM, 1) (SYMBOL, ;)
# 10.	(KEYWORD, case) (SYMBOL, <) (NUM, 3) (SYMBOL, :)
# 11.	(ID, b) (SYMBOL, =) (ID, b) (SYMBOL, +) (NUM, 2) (SYMBOL, ;)
# 12.	(KEYWORD, return) (SYMBOL, ;)
# 13.	(KEYWORD, case) (NUM, 4) (SYMBOL, :) (SYMBOL, ,) (SYMBOL, -) (SYMBOL, -) (SYMBOL, ]) (SYMBOL, [) (SYMBOL, ;) (SYMBOL, ;) (SYMBOL, ;)
# 14.	(SYMBOL, {) (SYMBOL, *) (SYMBOL, *) (SYMBOL, *) (SYMBOL, <) (SYMBOL, <)
# 15.	(ID, x) (SYMBOL, =) (NUM, 5) (SYMBOL, ;) (SYMBOL, :) (SYMBOL, :)
# 16.	(ID, b) (SYMBOL, =) (ID, u) (SYMBOL, *) (NUM, 123) (SYMBOL, ;)
# 17.	(KEYWORD, break) (SYMBOL, ;) (SYMBOL, })
# 18.	(KEYWORD, default) (SYMBOL, :)
# 19.	(ID, b) (SYMBOL, =) (ID, b) (SYMBOL, -) (NUM, 1) (SYMBOL, ;)
# 20.	(SYMBOL, })
# 21.	(KEYWORD, return) (SYMBOL, ;)
# 22.	(SYMBOL, })
# 24.	(ID, bar) (SYMBOL, =) (SYMBOL, *) (ID, then)
# """,
#     """
# 1.	(KEYWORD, void) (ID, min) (SYMBOL, () (KEYWORD, void) (SYMBOL, )) (SYMBOL, {)
# 2.	(KEYWORD, for) (KEYWORD, int) (ID, j0) (SYMBOL, ;) (NUM, 2) (SYMBOL, :) (NUM, 90) (SYMBOL, )) (SYMBOL, {)
# 3.	(ID, output) (SYMBOL, () (ID, v) (SYMBOL, )) (SYMBOL, ;)
# 4.	(SYMBOL, })
# 6.	(ID, i)
# 7.	(KEYWORD, switch) (SYMBOL, () (ID, arr) (SYMBOL, [) (ID, g) (SYMBOL, ]) (SYMBOL, )) (SYMBOL, {)
# 8.	(KEYWORD, case) (NUM, 2) (SYMBOL, :)
# 9.	(ID, b) (SYMBOL, ==) (SYMBOL, ==) (SYMBOL, =) (ID, b) (SYMBOL, +) (NUM, 1) (SYMBOL, ;)
# 10.	(KEYWORD, case) (SYMBOL, <) (NUM, 3) (SYMBOL, :)
# 11.	(ID, b) (SYMBOL, =) (ID, b) (SYMBOL, +) (NUM, 2) (SYMBOL, ;)
# 12.	(KEYWORD, return) (SYMBOL, ;)
# 13.	(KEYWORD, case) (NUM, 4) (SYMBOL, :) (SYMBOL, ,) (SYMBOL, -) (SYMBOL, -) (SYMBOL, ]) (SYMBOL, [) (SYMBOL, ;) (SYMBOL, ;) (SYMBOL, ;)
# 14.	(SYMBOL, {) (SYMBOL, *) (SYMBOL, *) (SYMBOL, *) (SYMBOL, <) (SYMBOL, <)
# 15.	(ID, x) (SYMBOL, =) (NUM, 5) (SYMBOL, ;) (SYMBOL, :) (SYMBOL, :)
# 16.	(ID, b) (SYMBOL, =) (ID, u) (SYMBOL, *) (NUM, 123) (SYMBOL, ;)
# 17.	(KEYWORD, break) (SYMBOL, ;) (SYMBOL, })
# 18.	(KEYWORD, default) (SYMBOL, :)
# 19.	(ID, b) (SYMBOL, =) (ID, b) (SYMBOL, -) (NUM, 1) (SYMBOL, ;)
# 20.	(SYMBOL, })
# 21.	(KEYWORD, return) (SYMBOL, ;)
# corrupted line 22.	(SYMBOL, })
# 25.	(ID, bar) (SYMBOL, =) (SYMBOL, *) (ID, then) (ID, Extra)
# """
# ))
