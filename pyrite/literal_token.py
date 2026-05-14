from token import Token, TokenType


class LiteralToken(Token):
    def __init__(self, t_type: TokenType, value: str) -> None:
        super().__init__(t_type=t_type, children=None, value=value)

    def __repr__(self) -> str:
        return self.value
