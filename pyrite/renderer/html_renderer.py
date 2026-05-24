from pyrite.tokens.token import Token
from pyrite.tokens.root import RootToken


def HTMLRenderer(root: Token) -> str:
    if not root.children:
        return token_to_html(root)

    



