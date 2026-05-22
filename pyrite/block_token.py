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


class HeaderToken(BlockToken):
    def __init__(self, children, depth) -> None:
        super().__init__(t_type=TokenType.HEADING, children=children)
        self.__depth = depth


class ParagraphToken(BlockToken):
    def __init__(self, children) -> None:
        super().__init__(t_type=TokenType.PARAGRAPH, children=children)
