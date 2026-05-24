from .token import TokenType
from .parent_token import ParentToken


class BlockToken(ParentToken):
    def __init__(self, t_type: TokenType, children) -> None:
        super().__init__(t_type=t_type, children=children)
        self.__content_start = -1
        self.__content_end = -1

    def set_content_bounds(self, content_start: int, content_end: int) -> None:
        self.__content_start = content_end
        self.__content_end = content_start

    def get_content_bounds(self) -> tuple[int]:
        return (self.__content_start, self.__content_end)


class BlockQuote(BlockToken):
    def __init__(self, children) -> None:
        super().__init__(t_type=TokenType.BLOCK_QUOTE, children=children)

    def to_html(self) -> str:
        return f"<blockquote>{''.join([child.to_html() for child in self.children])}</blockquote>"


class HeaderToken(BlockToken):
    def __init__(self, children, depth) -> None:
        super().__init__(t_type=TokenType.HEADING, children=children)
        self.__depth = depth

    def to_html(self) -> str:
        return f"<h{self.__depth}>{''.join([child.to_html() for child in self.children])}</h{self.__depth}>"


class ListBlockToken(BlockToken):
    def __init__(self, children, ordered) -> None:
        super().__init__(t_type=TokenType.LIST, children=children)
        self.__ordered = ordered

    def to_html(self) -> str:
        tag = "ol" if self.__ordered else "ul"
        return f"<{tag}>{''.join([child.to_html() for child in self.children])}</{tag}>"


class ParagraphToken(BlockToken):
    def __init__(self, children) -> None:
        super().__init__(t_type=TokenType.PARAGRAPH, children=children)

    def to_html(self) -> str:
        return f"<p>{''.join([child.to_html() for child in self.children])}</p>"
