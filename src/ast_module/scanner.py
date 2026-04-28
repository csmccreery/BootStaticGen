from .parent_token import ParentToken, ParentTokenType
from .literal_token import LiteralToken
import re


class Scanner:
    def __init__(self, text):
        self.text = text or ""
        self.trigger_chars = ["*", "-", "_", "#", "`" ">", "&", "[", "]", "(", ")", "!"]
        self.block_rules = [
            # Match any number of #'s followed by a space and then any amount of text ending in a newline
            ("header", re.compile(r"^(?P<header>#+)\s(?P<text>.*?)(\n|$)")),

            # Match exactly 3 `'s followed by a newline, then any amount of text (including new lines) ending in exactly 3 `'s and a newline
            ("code_block", re.compile(r"^`{3}(?P<code_type>[a-zA-Z])?\n(?P<text>.*?)`{3}\n", re.DOTALL)),  

            # Literally anything + two newlines
            ("paragraph", re.compile(r'^(?P<text>.*?)(\n\n|$)')),

            ("ordered_list", re.compile(r'^(?P<list_item>[0-9])\.\s(?P<text>.*?)\n[0-9]\.')),
            ("unordered_list", re.compile(r'^(?P<list_item>(\*|-|\+))\.\s(?P<text>.*?)\n\1\.'))
        ]
        self.inline_rules = [
            ("bold", re.compile(r"^\*\*(?P<text>.*?)\*\*", re.DOTALL)),
            ("italic", re.compile(r"^(\*|_)(?P<text>.*?)\1", re.DOTALL)), 
            ("link", re.compile(r"^\[(?P<text>.*?)\]\((?P<url>.*?)\)")),
            ("wiki_link", re.compile(r"^\[\[(?P<url>.*?)(?P<text>\|.*?)?\]\]")),
            ("image", re.compile(r"^!\[(?P<text>.*?)\]\((?P<url>.*?)\)")),
        ]

    #####################################################################################
    #                            UTILITIES SECTION                                      #
    #####################################################################################

    def tokenize(self):
        if not self.text:
            return None

        # All the stuff happens here
        block_children = self.block_parse()
        for block in block_children:
            content_start, content_end = block.start, block.end
            block.children = self.inline_parse(content_start, content_end)
        return block_children

    #####################################################################################
    #                                BLOCK SECTION                                      #
    #####################################################################################

    def block_parse(self):
        tokens = []
        cursor = 0
        while cursor < len(self.text):
            saved_pos = cursor

            # If the following triggers both the cursor and the saved position *should* be the same
            if self.text[cursor] in self.trigger_chars:
                new_token, next_pos = self.block_dispatcher(saved_pos)
            else:
                block_match = re.match(self.block_rules[-1][1], self.text[saved_pos:])
                new_token, next_pos = self.paragraph_handler(saved_pos, block_match)

            if new_token:
                print(new_token)
                cursor = next_pos
                tokens.append(new_token)
            else:
                cursor += 1
                continue

            # Skip empty lines
            while cursor < len(self.text) and self.text[cursor] == '\n':
                cursor += 1  # Still O(n) because both while loops have the same bound and move the same pointer

        return tokens

    def block_dispatcher(self, saved_pos):
        for rule, pattern in self.block_rules:
            block_match = re.match(pattern, self.text[saved_pos:])
            if block_match:
                match rule:
                    case ParentTokenType.HEADER.value:
                        return self.header_handler(saved_pos, block_match)
                    case ParentTokenType.CODE_BLOCK.value:
                        return self.code_block_handler(saved_pos, block_match)
                    case _:
                        return self.paragraph_handler(saved_pos, block_match)
        return None, saved_pos

    def header_handler(self, saved_pos, block_match):
        if block_match:

            header = block_match.group('header')
            content_start = saved_pos + block_match.start('header')
            content_end = saved_pos + block_match.end('text')
            next_pos = content_end + 1
            print("Called: Header Handler")
            print(f"Cursor: {saved_pos} Start: {block_match.start('text')}")
            print(f"Cursor: {saved_pos} Start: {block_match.end('text')}")

            return ParentToken(
                token_type=ParentTokenType.HEADER,
                children=[],
                start=content_start,
                end=content_end,
                data={'level', len(header)}
            ), next_pos 
        return None, saved_pos

    def code_block_handler(self, saved_pos, block_match):
        if block_match:
            print("block code")

            code_type = block_match.group('code_type')
            content_start = saved_pos + block_match.start('code_type')
            content_end = saved_pos + block_match.end('text')
            next_pos = content_end + 1
            print("Called: Code Block Handler")
            print(f"Cursor: {saved_pos} Start: {block_match.start('text')}")
            print(f"Cursor: {saved_pos} Start: {block_match.end('text')}")

            return ParentToken(
                token_type=ParentTokenType.CODE_BLOCK,
                children=[],
                start=content_start,
                end=content_end,
                data={'code_type', code_type}
            ), next_pos 
        return None, saved_pos

    def paragraph_handler(self, saved_pos, block_match):
        if block_match:
            print("caught in paragraph")

            content_start = saved_pos + block_match.start("text")
            content_end = saved_pos + block_match.end("text")
            next_pos = saved_pos + block_match.end()
            print("Called: Paragraph Handler")
            print(f"Cursor: {saved_pos} Start: {block_match.start('text')}")
            print(f"Cursor: {saved_pos} Start: {block_match.end('text')}")

            return ParentToken(
                token_type=ParentTokenType.PARAGRAPH,
                children=[],
                start=content_start,
                end=content_end,
                data={}
            ), next_pos
        return None, saved_pos

    #####################################################################################
    #                               INLINE SECTION                                      #
    #####################################################################################

    def inline_parse(self, start, end):
        cursor = start
        tokens = []

        last_processed_pos = start

        while cursor < end:
            if self.text[cursor] in self.trigger_chars:
                # If this is actually a token and not someone just randomly
                # throwing asterisks in their markdown then we do the following
                new_token, next_pos = self.inline_dispatch(cursor, end)
                if new_token:
                    if cursor > last_processed_pos:
                        tokens.append(LiteralToken(last_processed_pos, cursor))

                    tokens.append(new_token)

                    cursor = next_pos
                    last_processed_pos = cursor
                    continue

            cursor += 1
        if last_processed_pos < end:
            tokens.append(LiteralToken(last_processed_pos, end))

        return tokens

    def inline_dispatch(self, cursor, limit):
        for rule, pattern in self.inline_rules:
            inline_match = re.match(pattern, self.text[cursor:limit])
            if inline_match:
                match rule:
                    case ParentTokenType.BOLD.value:
                        return self.handle_inline_bold(cursor, inline_match)
                    case ParentTokenType.ITALIC.value:
                        return self.handle_inline_italic(cursor, inline_match)
                    case ParentTokenType.CODE.value:
                        return self.handle_inline_code(cursor, inline_match)
        return None, cursor

    def handle_inline_bold(self, cursor, inline_match):
        if inline_match:
            content_start = cursor + inline_match.start("text")
            content_end = cursor + inline_match.end("text")
            print(f"Cursor: {cursor} Start: {inline_match.start('text')}")
            print(f"Cursor: {cursor} Start: {inline_match.end('text')}")
            end_pos = cursor + inline_match.end()

            return ParentToken(
                token_type=ParentTokenType.BOLD,
                children=self.inline_parse(content_start, content_end),
                start=content_start,
                end=content_end,
                data={}
            ), end_pos
        return None, cursor

    def handle_inline_italic(self, cursor, inline_match):
        if inline_match:
            content_start = cursor + inline_match.start("text")
            content_end = cursor + inline_match.end("text")
            end_pos = cursor + inline_match.end()
            print(f"Cursor: {cursor} Start: {inline_match.start('text')}")
            print(f"Cursor: {cursor} Start: {inline_match.end('text')}")

            return ParentToken(
                token_type=ParentTokenType.ITALIC,
                children=self.inline_parse(content_start, content_end),
                start=content_start,
                end=content_end,
                data={}
            ), end_pos
        return None, cursor    

    def handle_inline_code(self, cursor, inline_match):
        if inline_match:
            print("inline code")
            content_start = cursor + inline_match.start("text")
            content_end = cursor + inline_match.end("text")
            end_pos = cursor + inline_match.end()

            return ParentToken(
                token_type=ParentTokenType.CODE,
                children=[],
                start=content_start,
                end=content_end,
                data={}
            ), end_pos
        return None, cursor    

    def handle_inline_links(self, cursor, inline_match):
        if inline_match:
            print("inline links")
            content_start = cursor + inline_match.start("text")
            content_end = cursor + inline_match.end("text")
            end_pos = cursor + inline_match.end("url") + 1

            return ParentToken(
                token_type=ParentTokenType.CODE,
                children=[],
                start=content_start,
                end=content_end,
                data={'url': inline_match.group("url")}
            ), end_pos
        return None, cursor    

    def handle_inline_wiki_links(self, cursor, inline_match):
        if inline_match:
            print("inline wiki-links")
            content_start = cursor + inline_match.start("text")
            content_end = cursor + inline_match.end("text")
            end_pos = cursor + inline_match.end("url") + 1

            return ParentToken(
                token_type=ParentTokenType.CODE,
                children=[],
                start=content_start,
                end=content_end,
                data={'url': inline_match.group("url")}
            ), end_pos
        return None, cursor    

    def handle_inline_images(self, cursor, inline_match):
        if inline_match:
            print("inline image")
            content_start = cursor + inline_match.start("text")
            content_end = cursor + inline_match.end("text")
            end_pos = cursor + inline_match.end("url") + 1

            return ParentToken(
                token_type=ParentTokenType.CODE,
                children=[],
                start=content_start,
                end=content_end,
                data={
                    'url': inline_match.group("url"),
                    'alt': inline_match.group("text")
                    }
            ), end_pos
        return None, cursor    

