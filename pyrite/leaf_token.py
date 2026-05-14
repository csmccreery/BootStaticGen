from token import TokenType
from literal_token import LiteralToken


class LeafToken(LiteralToken):
    def __init__(self, t_type, value: str) -> str:
        super().__init__(t_type=t_type, value=value)


class TextToken(LeafToken):
    def __init__(self, value) -> None:
        super().__init__(t_type=TokenType.TEXT, value=value)

    def __repr__(self) -> str:
        return f"TextToken: [{self.value}]"


class ImageToken(LeafToken):
    def __init__(self, value: str, alt_text: str, url: str) -> None:
        super().__init__(t_type=TokenType.IMAGE, value=value)
        self.__alt_text = alt_text
        self.__url = url


class LinkToken(LiteralToken):
    def __init__(self, value: str, url: str, display_text: str) -> None:
        super().__init__(t_type=TokenType.LINK, value=value)
        self.__url = url
        self.__display_text = display_text
