import re

LINE_PATTERN = re.compile(r"(?P<linenum>\d+)\.\s*(?P<content>.+)")
ERROR_PATTERN = re.compile(r"#(?P<linenum>\d+)\s*:\s*(?P<content>.+)")


def calc_alignment_score(first, second, del_penalty=-1, edit_penalty=-1, match_score=0) -> int:
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


def calc_parse_tree_score(expected: str, actual: str):
    def extract_parts(text: str):
        return text.replace(" ", "")

    return calc_score(
        expected, actual,
        extract_parts,
        del_penalty=-1,
        edit_penalty=-1)


def calc_syntax_errors_score(expected: str, actual: str):
    def extract_parts(text: str):
        m = ERROR_PATTERN.match(text)
        result = m.groupdict() if m else {"linenum": -1, "content": text}
        return (result["linenum"], (result["content"],))

    return calc_score(
        expected, actual,
        extract_parts,
        del_penalty=calc_line_content_del_penalty,
        edit_penalty=calc_line_content_edit_penalty)
