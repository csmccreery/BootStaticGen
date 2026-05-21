import re
from typing import List
from .token import Token, TokenType
from .inline_token import InlineToken, StrongToken, EmphasisToken
from .root import RootToken
from .block_token import (
            BlockToken,
            BlockQuote,
            ParagraphToken,
            CodeBlock,
            HeaderToken
        )
from .leaf_token import (
            LeafToken,
            InlineCodeToken,
            ImageToken,
            LinkToken,
            TextToken
        )


def tokenize(lines) -> Token:
    return parse_blocks(lines)


def parse_blocks(lines) -> RootToken:
    block_rules = [
                ("block_quote", re.compile(r'^>\s?.*')),
                ("heading", re.compile(r'^#{1,6}\s+.+')),
                ("code_fence", re.compile(r'^```(\s.+?<language>).*"')),
                ("list_item", re.compile(r'^[\*\-\+]\s+.*|^\d+\.\s.*')),
            ]

    blocks = []
    cursor = 0

    while cursor < len(lines):
        line: str = lines[cursor]

        for rule, pattern in block_rules:
            block_match = re.search(pattern, line)
            match block_match:
                case "block_quote":
                    pass
                case "heading":
                    depth = len(line.split()[0].strip())
                    content = line.split()[1].strip()
                    blocks.append(HeaderToken(
                        children=parse_inline(content),
                        depth=depth
                    ))
                    cursor += 1
                case "code_fence":
                    language = block_match.group(1)
                    code_lines = []
                    while (
                        cursor < len(lines) and
                        not re.search(pattern, lines[cursor])
                    ):
                        code_lines.append(lines[cursor])
                        cursor += 1

                    content = "\n".join(code_lines)
                    blocks.append(
                        CodeBlock(
                            children=TextToken(value=content),
                            language=language | "text"
                        ))
                case "list_item":
                    pass
                case _:
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

            match rule:
                case "strong":
                    token = StrongToken(children=parse_inline(inner))
                case "emphasis":
                    token = EmphasisToken(children=parse_inline(inner))
                case "inline_code":
                    print("processing inline_code token")
                    token = InlineCodeToken(value=inner)
                case "link":
                    print("processing link token")
                    token = LinkToken(
                                value=inner,
                                url=match.group(2),
                                display_text=match.group(1)
                        )
                case "image":
                    print("processing image token")
                    token = ImageToken(
                                value=inner,
                                url=match.group(1),
                                alt_text=match.group(2)
                        )
                case _:
                    pass

            return before_tokens + [token] + after_tokens

    return [TextToken(content)]
