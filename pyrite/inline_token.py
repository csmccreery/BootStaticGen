from token import TokenType
from parent_token import ParentToken


class InlineToken(ParentToken):
    def __init__(self, t_type, children) -> None:
        super().__init__(t_type=t_type, children=children)


class StrongToken(InlineToken):
    def __init__(self, children) -> None:
        super().__init__(t_type=TokenType.STRONG, children=children)


class EmphasisToken(InlineToken):
    def __init__(self, children) -> None:
        super().__init__(t_type=TokenType.EMPHASIS, children=children)
