from tokenizer import tokenize
from pathlib import Path


def parse_md(path):
    corrected_path = Path(path)
    with open(corrected_path, "r") as f:
        file_content = f.readlines()
        print(file_content)

    root = tokenize(file_content)
    return root


def main():
    current_dir = Path(__file__).parent.resolve()
    root = parse_md(current_dir / "tests" / "test.md")

    for child in root.children:
        print(child)


if __name__ == "__main__":
    main()
