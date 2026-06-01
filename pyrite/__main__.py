from tokenizer import tokenize
from tokens.root import RootToken
from pathlib import Path
import argparse


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.addArgument('-i', '--input', help="Path like object pointing at either a directory or single file path", default="./*")
    parser.addArgument('-o', '--output', help="Path like object representing a file or directory to store the output", default=".")
    parser.addArgument('-r', '--recursive', help="If true Pyrite will recursively search through directories and output in the same order", action="store_true")
    parser.addArgument('-s', "--serve", help="Serve the contents of the path pointed to by --output", action="store_true")
    parser.addArgument('-w', '--watch', help="Watch the contents of the path specified by --output for changes and update the files live", action="store_true")
    parser.addArgument('-p', '--port', help="specify the port to serve on: Default 8088", type=int, default=8088)

    return parser


def parse_md(path) -> RootToken:
    corrected_path = Path(path)
    with open(corrected_path, "r") as f:
        file_content = f.readlines()
        print(file_content)

    root = tokenize(file_content)
    return root


def main():
    current_dir = Path(__file__).parent.resolve()
    root = parse_md(current_dir / "tests" / "test.md")

    webpage = root.to_html()
    print(webpage)


if __name__ == "__main__":
    main()
