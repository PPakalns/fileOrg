from pathlib import Path, PosixPath
from typing import List

class OrganizerException(Exception):
    pass

def AcceptDialog(message="Please indicate approval [y/n/?]: "):
    print(message, end='')
    yes = ['yes', 'y']
    no = ['no', 'n']
    q = ['?']

    answ = ""
    while True:
        choice = input().lower()
        if choice in yes:
            return True
        if choice in no:
            return False
        if choice in q:
            return None


class OrganizerInstance:

    def __init__(self, src_dir:Path, out_dir:Path, ext_list:List[str]):

        if not (src_dir.exists() and src_dir.is_dir()):
            raise OrganizerException("Provided source directory doesn't exist or isn't a directory!")

        self.src_dir = src_dir
        self.out_dir = out_dir
        self.ext_list = [x.lower() for x in ext_list]


    def organize(self, dry_run:bool=False):
        print(f"Starting organizing process. dry_run={dry_run}")
        print(f"Searching for following extensions: {self.ext_list}")
        self.parse_dir(self.src_dir, dry_run=dry_run)
        print("\nFiles organized!")


    def parse_dir(self, act_dir: Path, dry_run:bool, path_prefix:Path=None):
        dirs_to_parse = []
        files_to_copy = []

        for ch in act_dir.iterdir():
            try:
                # Parse child directories later
                if ch.is_dir():
                    dirs_to_parse.append(ch)
                    continue

                # Skip non regular files
                if not ch.is_file():
                    continue

                if ch.suffix.lower() in self.ext_list:
                    files_to_copy.append(ch)

            except PermissionError as e:
                print("Insufficient permissions")
                print(e)

        if files_to_copy:
            # Prepare path prefix with folder
            initialized_path_prefix = False
            if path_prefix is None:
                initialized_path_prefix = True
                path_prefix = Path(act_dir.resolve().absolute().name or "root")

            print()
            print(f"In source directory \t{act_dir.relative_to(self.src_dir)}"
                  f"\n\tfound {len(files_to_copy)} specified files!")
            print(f"Files will be copied to directory: \t {path_prefix}")

            accepted = None
            while accepted is None:
                accepted = AcceptDialog()
                if accepted is None:
                    print("The following files were found:")
                    for file in files_to_copy:
                        print(f"\t{file}")

            if accepted:
                copy_target_dir = self.out_dir / path_prefix
                self.recursive_mkdir(copy_target_dir, dry_run=dry_run)
                for file in files_to_copy:
                    self.copy(file.absolute(), self.out_dir / path_prefix, dry_run=dry_run)
                print("Files copied successfully")
            else:
                # Unset path prefix if this is determined to not be the root directory of specified files
                if initialized_path_prefix:
                    path_prefix = None

        for ch_dir in dirs_to_parse:
            new_path_prefix = (path_prefix / ch_dir.name) if path_prefix else None
            self.parse_dir(ch_dir, dry_run, new_path_prefix)

    def recursive_mkdir(self, path: Path, dry_run: bool):
        # Add statistics
        if dry_run:
            return
        raise "Not implemented"

    def copy(self, src_file: Path, trg_file: Path, dry_run: bool):
        # Add statistics
        if dry_run:
            return
        raise "Not implemented"

