from .token import TokenType
from .literal_token import LiteralToken


class LeafToken(LiteralToken):
    def __init__(self, t_type, value: str) -> str:
        super().__init__(t_type=t_type, value=value)

    def __repr__(self) -> str:
        return f"{self.token_type.value}: Value={self.value}"


class TextToken(LeafToken):
    def __init__(self, value) -> None:
        super().__init__(t_type=TokenType.TEXT, value=value)

    def to_html(self) -> str:
        return self.value.strip()


class InlineCodeToken(LeafToken):
    def __init__(self, value: str) -> None:
        super().__init__(t_type=TokenType.INLINE_CODE, value=value)

    def to_html(self) -> str:
        return f"<code>{self.value.strip()}</code>"


class ImageToken(LeafToken):
    def __init__(self, value: str, alt_text: str, url: str) -> None:
        super().__init__(t_type=TokenType.IMAGE, value=value)
        self.__alt_text = alt_text
        self.__url = url

    def __repr__(self) -> str:
        return f"{self.token_type.value}: Value={self.value} alt_text={self.__alt_text} url={self.__url}"

    def to_html(self) -> str:
        return f"<img src={self.__url.strip()} alt={self.__alt_text.strip()}>"


class LinkToken(LeafToken):
    def __init__(self, value: str, url: str, display_text: str) -> None:
        super().__init__(t_type=TokenType.LINK, value=value)
        self.__url = url
        self.__display_text = display_text

    def __repr__(self) -> str:
        return f"{self.token_type.value}: Value={self.value} display_text={self.__display_text} url={self.__url}"

    def to_html(self) -> str:
        return f"<a href={self.__url.strip()}>{self.__display_text.strip()}</a>"


class CodeBlock(LeafToken):
    def __init__(self, value: str, language=None) -> None:
        super().__init__(t_type=TokenType.CODE_BLOCK, value=value)
        self.__language = language or "plain_text"

    def __repr__(self) -> str:
        return f"{self.token_type.value}: Value={self.value}"

    def to_html(self) -> str:
        return f"<code>{self.value.strip()}</code>"
