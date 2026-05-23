from enum import Enum


class TokenType(Enum):
    ROOT = "root"
    BLOCK_QUOTE = "block_quote"
    HEADING = "heading"
    LIST = "list"
    LIST_ITEM = "list_item"
    PARAGRAPH = "paragraph"
    CODE_BLOCK = "code_block"
    STRONG = "strong"
    EMPHASIS = "emphasis"
    INLINE_CODE = "inline_code"
    LINK = "link"
    IMAGE = "image"
    TEXT = "text"


class Token:
    def __init__(self, t_type: TokenType, children=None, value=None) -> None:
        self.token_type = t_type or TokenType.ROOT
        self.children = children
        self.value = value

    def __repr__(self) -> str:
        raise NotImplementedError
