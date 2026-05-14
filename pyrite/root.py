from token import Token, TokenType
from typing import List


class RootToken(Token):
    def __init__(self, children) -> None:
        super().__init__(t_type=TokenType.ROOT, children=children, value=None)
        self.__depth = -1
        self.__count = -1

    def set_children(self, children: List[Token]) -> None:
        self.children = children

    def __repr__(self) -> str:
        return f"ParentToken: Type: [{self.token_type.value}] \
                [Children: {[str(child) for child in self.children]}]"
