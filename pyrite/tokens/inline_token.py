from .token import TokenType
from .parent_token import ParentToken


class InlineToken(ParentToken):
    def __init__(self, t_type, children) -> None:
        super().__init__(t_type=t_type, children=children)

    def __repr__(self) -> str:
        return f"{self.token_type.value}: Children={[str(child) for child in self.children]}"


class StrongToken(InlineToken):
    def __init__(self, children) -> None:
        super().__init__(t_type=TokenType.STRONG, children=children)

    def to_html(self) -> str:
        return (
            f"<strong>{''.join([child.to_html() for child in self.children])}</strong>"
        )


class EmphasisToken(InlineToken):
    def __init__(self, children) -> None:
        super().__init__(t_type=TokenType.EMPHASIS, children=children)

    def to_html(self) -> str:
        return f"<em>{''.join([child.to_html() for child in self.children])}</em>"


class ListItemToken(InlineToken):
    def __init__(self, children) -> None:
        super().__init__(t_type=TokenType.LIST_ITEM, children=children)

    def to_html(self) -> str:
        return f"<li>{''.join([child.to_html() for child in self.children])}</li>"
