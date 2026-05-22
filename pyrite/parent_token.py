from .token import TokenType, Token


class ParentToken(Token):
    def __init__(self, t_type: TokenType, children=None) -> None:
        super().__init__(t_type=t_type, children=children, value=None)
        self.children = children or []

    def __repr__(self) -> str:
        return f"ParentToken: Type: [{self.token_type.value}] \
                [Children: {[str(child) for child in self.children]}"
