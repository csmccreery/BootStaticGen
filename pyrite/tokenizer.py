from token import Token, TokenType
from block_token import BlockToken, BlockQuote, ParagraphToken, CodeBlock, HeaderToken
from inline_token import InlineToken, StrongToken, EmphasisToken
from leaf_token import LeafToken, ImageToken, LinkToken, TextToken
from root import RootToken
from typing import List
import re


def tokenize(lines) -> Token:
    return parse_blocks(lines)


def parse_blocks(lines) -> RootToken:
    block_rules = [
                ("block_quote", re.compile(r'^>\s?.*')),
                ("heading", re.compile(r'^#{1,6}\s+.+')),
                ("code_fence", re.compile(r'^```.*"')),
                ("list_item", re.compile(r'^[\*\-\+]\s+.*|^\d+\.\s.*')),
            ]

    blocks = []
    cursor = 0

    while cursor < len(lines):
        line: str = lines[cursor]

        for rule, pattern in block_rules:
            match = re.search(pattern, line)
            if match:
                print(f"Block match {rule} found")
                if rule == 'block_quote':
                    pass
                elif rule == 'heading':
                    depth = len(line.split()[0].strip())
                    content = line.split()[1].strip()
                    print(f"Depth: {depth}")
                    blocks.append(HeaderToken(
                        children=parse_inline(content),
                        depth=depth
                    ))
                    cursor += 1

                elif rule == 'code_fence':
                    pass

                elif rule == 'list_item':
                    pass
                else:
                    break
            else:
                # Catch all paragraph
                para_lines = []
                while cursor < len(lines) and not any(
                    re.search(p, lines[cursor]) for _, p in block_rules
                ):
                    para_lines.append(lines[cursor])
                    cursor += 1

                blocks.append(
                        ParagraphToken(children=parse_inline(
                            "\n".join(para_lines)
                            )))

    return RootToken(blocks)


def parse_inline(content) -> List[Token]:
    inline_rules = [
            ("strong", re.compile(r'\*\*(.+?)\*\*', re.DOTALL)),
            ("emphasis", re.compile(r'\*(.+?)\*', re.DOTALL)),
            ("inline_code", re.compile(r'`(.+?)`')),
            ("link", re.compile(r'\[(.+?)\]\((.+?)\)')),
            ("image", re.compile(r'!\[(.+?)\]\((.+?)\)')),
        ]

    if not content:
        return []

    for rule, pattern in inline_rules:
        match = re.search(pattern, content)
        if match:
            before = content[:match.start()]
            inner = match.group(1)
            after = content[match.end():]

            before_tokens = parse_inline(before)
            after_tokens = parse_inline(after)

            if rule == "strong":
                token = StrongToken(children=parse_inline(inner))
            elif rule == "emphasis":
                token = EmphasisToken(children=parse_inline(inner))

            return before_tokens + [token] + after_tokens

    return [TextToken(content)]
