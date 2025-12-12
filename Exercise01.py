import sys
import shutil
from pathlib import Path

# ANSI escape codes for colored output
COLOR_BLUE = "\\033[94m"
COLOR_RESET = "\\033[0m"



def arguments_parsing(*argv):
    """
    Парсінг аргументів - шлях до вихідної директорій та директорії призначення dafault - dist
    Перевірка чи існує шлях
    """
   
    if len(argv) == 0 or len(argv) > 2:
        raise ValueError(f"You need to provide at least one source directory name to copy from and one optional to copy too") 
    
    src = argv[0]
    dest = argv[1] if len(argv) == 2 else "destination"

    # Validate source exists
    if not os.path.isdir(src):
        raise ValueError(f"Source folder does not exists: {src}")
    
    return src, dest

def ensure_directory(path: Path) -> None:
    """Create directory if it does not exist."""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        print(f"PermissionError: Cannot create directory {path}: {e}", file=sys.stderr)
        raise
    except OSError as e:
        print(f"OSError: Cannot create directory {path}: {e}", file=sys.stderr)
        raise

def copy_folder_tree(src: str | Path, dest: str | Path) -> None:
    """
    RECURSIVE DIRECTORY READER + COPIER
    - Iterates items in 'src' directory.
    - If item is a directory, recurses.
    - If item is a file (or existing file symlink), copies it into 'dest' grouped by extension.
    """
    src_path = Path(src)
    dest_root = Path(dest)

    try:
        for item in src_path.iterdir():
            if item.is_dir():
                # Рекурсивно обходимо піддиректорії
                copy_folder_tree(item, dest_root)         # Рекурсія
            elif item.is_file():
                ext = item.suffix[1:] if item.suffix else "no_extension"
                target_dir = dest_root / ext
                ensure_directory(target_dir)
                try:
                    shutil.copy2(item, target_dir / item.name)
                except Exception as e:
                    print(f"Error copying {item} to {target_dir}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error reading directory {src_path}: {e}", file=sys.stderr)
    

def display_tree(path: Path, indent: str = "", prefix: str = "") -> None:
    if path.is_dir():
        # Use blue color for directories
        print(indent + prefix + COLOR_BLUE + str(path.name) + COLOR_RESET)
        indent += "    " if prefix else ""

        # Get a sorted list of children, with directories last
        children = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))

        for index, child in enumerate(children):
            # Check if the current child is the last one in the directory
            is_last = index == len(children) - 1
            display_tree(child, indent, "└── " if is_last else "├── ")
    else:
        print(indent + prefix + str(path.name))



if __name__ == "__main__":
    import sys
    try:
        src, dest = arguments_parsing(*sys.argv[1:]) # читаєжмо перші аргументи - директорії src & dest
        copy_folder_tree(src, dest)
        display_tree(Path(dest))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
