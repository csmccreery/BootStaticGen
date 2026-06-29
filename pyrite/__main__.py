from tokenizer import tokenize
from tokens.root import RootToken
from pathlib import Path
from http_server import run_server
import argparse


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-R',
        '--root',
        help="Specify the root directory of the http server",
        action="store_true"
    )
 
    parser.add_argument(
        '-g',
        '--good-boi',
        help="Look you made the damn thing using a mark and sweep. You've gone above and beyond the call of duty.",
        action="store_true"
    )
    
    parser.add_argument(
        '-i',
        '--input',
        help="Path like object pointing at either a directory or single file path", default="/"
    )
     
    parser.add_argument(
        '-O',
        '--one-shot',
        help="Instead of parsing an entire directory, point the parser at one file, get one file out", action="store_true"
    )
  
    parser.add_argument(
        '-D',
        '--dashboard',
        help="If true, will create an index.html at the root of the target dir with links to all created files", 
        default=False,
        action="store_true"
    )
 
    parser.add_argument(
        '-o',
        '--output',
        help="Path like object representing a file or directory to store the output", default="."
    )
    
    parser.add_argument(
        '-r',
        '--recursive',
        help="Pyrite will recursively search through directories and output in the same order",
        action="store_true"
    )

    parser.add_argument(
        '-s',
        "--serve",
        help="Serve the contents of the path pointed to by --output",
        action="store_true"
    )
    
    parser.add_argument(
        '-w',
        '--watch',
        help="Watch the path specified by --output for changes and update the files live",
        action="store_true"
    )

    parser.add_argument(
        '-p',
        '--port',
        help="specify the port to serve on: Default 8088",
        type=int,
        default=8088
    )

    return parser

from pathlib import Path
from tokenizer import tokenize

def recursive_parse_md_to_html(dir_path) -> tuple[dict, list]:
    path_names = []
    
    def create_ast(current_dir) -> dict:
        current_level_dict = {}  # Create a fresh dict for this specific directory level
        paths = Path(current_dir)
        
        for path in paths.iterdir():
            path_names.append(path)
            if path.is_dir():
                # Recursively get the dictionary for THIS subdirectory
                current_level_dict[path.as_posix()] = create_ast(path)
            else:
                with open(path, 'r', encoding='utf-8') as content:
                    lines = content.readlines()
                    current_level_dict[path.as_posix()] = tokenize(lines).to_html()

        return current_level_dict

    html_tree = create_ast(dir_path)
    return html_tree, path_names


def parse_single_md_to_html(input: Path):
    with open(input, "r") as fp:
        roots = tokenize(fp.readlines()).to_html()
        return roots


def initialize_static_dir(output_dir, input_dir, roots, make_dashboard=False) -> None:
    # Flatten the nested dictionary safely
    def recursive_flatten_dir(root_dict) -> list:
        accumulated_paths = []
        for _path, node in root_dict.items():
            path = Path(_path)
            
            if isinstance(node, dict):
                # Node is a sub-directory dictionary, drill down
                accumulated_paths.extend(recursive_flatten_dir(node))
            else:
                # Node is the HTML string content
                accumulated_paths.append((path, node))
                
        return accumulated_paths

    body = ""
    for original_path, content in recursive_flatten_dir(roots):
        relative_part = original_path.relative_to(input_dir)
        print(f"Relative_part: {relative_part}")
        target_path = output_dir / relative_part.with_suffix(".html") 
        print(f"Target Path: {target_path}")

        relative_url = target_path.relative_to(output_dir)
        print(f"Relative Final: {relative_url}")
        
        body += f"<li><a href={relative_url.as_posix()}>{target_path.name}</a></li>"
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(target_path.as_posix(), "w", encoding='utf-8') as f:
            f.write(content)

    dash_board = f"<html>{body}</html>"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    if make_dashboard:
        with open(output_dir / "index.html", "w", encoding='utf-8') as index:
            index.write(dash_board)
            

def main():
    parser = argument_parser()
    args = parser.parse_args()

    if args.good_boi:
        print("Well done.")
        return

    if args.one_shot:
        input = Path(args.input)
        output = Path(args.output)
        roots = parse_single_md_to_html(input)
        with open(output, "w") as idx:
            idx.write(roots)

        if args.serve:
            run_server(("127.0.0.1", args.port), directory=output.parent.resolve())

    else:
        input_dir = Path(args.input).resolve()
        output_dir = Path(args.output).resolve()
    
        roots, _ = recursive_parse_md_to_html(input_dir)
        initialize_static_dir(output_dir, input_dir, roots, False)

    if args.serve:
        run_server(("127.0.0.1", args.port), directory=output_dir) 


if __name__ == "__main__":
    main()
