from .token import Token, TokenType
from .parent_token import ParentToken
from typing import List


class RootToken(ParentToken):
    def __init__(self, children) -> None:
        super().__init__(t_type=TokenType.ROOT, children=children)
        self.__depth = -1
        self.__count = -1

    def set_children(self, children: List[Token]) -> None:
        self.children = children
