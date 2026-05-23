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


class EmphasisToken(InlineToken):
    def __init__(self, children) -> None:
        super().__init__(t_type=TokenType.EMPHASIS, children=children)

class ListItemToken(InlineToken):
    def __init__(self, children, depth=0) -> None:
        super().__init__(t_type=TokenType.LIST_ITEM, children=children)
        self.__depth = depth
