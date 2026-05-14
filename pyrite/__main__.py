from tokenizer import *
from pathlib import Path


def main() -> None:
    file_location = Path(__file__).resolve()

    with open(file_location.parent.parent / "tests" / "test.md", 'r') as fin:
        lines = fin.readlines()
        root = tokenize(lines)
        for child in root.children:
            print(child)

    print(file_location)


if __name__ == "__main__":
    main()
