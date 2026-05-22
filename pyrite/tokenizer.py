import re
from typing import List
from .token import Token
from .inline_token import StrongToken, EmphasisToken
from .root import RootToken
from .block_token import (
            BlockQuote,
            ParagraphToken,
            HeaderToken
        )
from .leaf_token import (
            InlineCodeToken,
            ImageToken,
            LinkToken,
            CodeBlock,
            TextToken
        )


def tokenize(lines) -> Token:
    return parse_blocks(lines)


def parse_header(lines, cursor) -> tuple[Token, int]:
    depth = len(lines[cursor].split()[0].strip())
    content = lines[cursor].split()[1].strip()
    return HeaderToken(
        children=parse_inline(content),
        depth=depth
    ), cursor + 1


def parse_block_quote(lines, cursor) -> tuple[Token, int]:
    return BlockQuote(children=[]), cursor


def parse_paragraph(block_rules, lines, cursor) -> tuple[Token, int]:
    para_lines = []
    while cursor < len(lines) and not any(
        re.search(p, lines[cursor]) for _, p in block_rules
    ):
        para_lines.append(lines[cursor])
        cursor += 1

    if para_lines:
        return ParagraphToken(children=parse_inline(
            "\n".join(para_lines)
        )), cursor

    return None, cursor


def parse_code_fence(pattern, lines, cursor) -> tuple[Token, int]:
    code_lines = []
    cursor += 1
    while (
        cursor < len(lines) and
        not pattern.search(lines[cursor])
    ):
        code_lines.append(lines[cursor])
        cursor += 1

    if cursor < len(lines):
        cursor += 1

    return CodeBlock(
        value="\n".join(code_lines),
        language="text"
    ), cursor


# TODO
def parse_list_block(lines, cursor) -> tuple[Token, int]:
    return None, cursor


def parse_blocks(lines) -> RootToken:
    block_rules = [
                ("block_quote", re.compile(r'^>\s?.*')),
                ("heading", re.compile(r'^#{1,6}\s+.+')),
                ("code_fence", re.compile(r'^```')),
                ("list_item", re.compile(r'^[\*\-\+]\s+.*|^\d+\.\s.*')),
            ]

    blocks = []
    cursor = 0

    while cursor < len(lines):
        matched = False
        for rule, pattern in block_rules:
            block_match = pattern.search(lines[cursor])
            if block_match:
                matched = True
                block = None
                new_cursor = cursor
                match rule:
                    case "block_quote":
                        block, new_cursor = parse_block_quote(lines, cursor)
                    case "heading":
                        block, new_cursor = parse_header(lines, cursor)
                    case "code_fence":
                        block, new_cursor = parse_code_fence(pattern, lines, cursor)
                    case "list_item":
                        block, new_cursor = parse_list_block(lines, cursor)

                blocks.append(block)
                if new_cursor < len(lines):
                    cursor = new_cursor
                else:
                    return RootToken(blocks)
        if not matched:
            block, new_cursor = parse_paragraph(block_rules, lines, cursor)
            if block:
                blocks.append(block)

            if new_cursor < len(lines):
                cursor = new_cursor
            else:
                return RootToken(blocks)

    return RootToken(blocks)


def parse_inline(content) -> List[Token]:
    inline_rules = [
            ("strong", re.compile(r'\*\*(.+?)\*\*', re.DOTALL)),
            ("emphasis", re.compile(r'\*(.+?)\*', re.DOTALL)),
            ("inline_code", re.compile(r'`(.+?)`')),
            ("image", re.compile(r'!\[(.+?)\]\((.+?)\)')),
            ("link", re.compile(r'\[(.+?)\]\((.+?)\)')),
        ]

    if not content:
        return []

    earliest_match = None
    earliest_pos = float("inf")
    matched_rule = None

    for rule, pattern in inline_rules:
        inline_match = pattern.search(content)
        if inline_match and inline_match.start() < earliest_pos:
            earliest_pos = inline_match.start()
            earliest_match = inline_match
            matched_rule = rule

    if earliest_match is None:
        return [TextToken(content)]

    before = content[:earliest_match.start()]
    after = content[earliest_match.end():]

    before_tokens = parse_inline(before)
    after_tokens = parse_inline(after)

    token = None

    match matched_rule:
        case "strong":
            inner = earliest_match.group(1)
            token = StrongToken(children=parse_inline(inner))
        case "emphasis":
            inner = earliest_match.group(1)
            token = EmphasisToken(children=parse_inline(inner))
        case "inline_code":
            inner = earliest_match.group(1)
            token = InlineCodeToken(value=inner)
        case "link":
            display_text = earliest_match.group(1)
            url = earliest_match.group(2)
            token = LinkToken(
                        value=earliest_match.group(0),
                        url=url,
                        display_text=display_text
                )
        case "image":
            alt_text = earliest_match.group(1)
            url = earliest_match.group(2)
            token = ImageToken(
                        value=earliest_match.group(0),
                        url=url,
                        alt_text=alt_text
                )
        case _:
            token = TextToken(earliest_match.groups())

    return before_tokens + [token] + after_tokens
