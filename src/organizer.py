from pathlib import Path, PosixPath
from typing import List
from enum import Enum
import os
import errno
import shutil

class OrganizerException(Exception):
    pass

class Answer(Enum):
    YES = 0
    NO = 1
    SKIP = 2
    LIST = 3

def AcceptDialog(message="Please indicate approval [y/n/s/l/?]: ") -> Answer:
    print(message, end='')
    yes = ['yes', 'y']
    no = ['no', 'n']
    skip = ['s']
    list_files = ['l']
    q = ["?"]

    answ = ""
    while True:
        choice = input().lower()
        if choice in yes:
            return Answer.YES
        if choice in no:
            return Answer.NO
        if choice in list_files:
            return Answer.LIST
        if choice in skip:
            return Answer.SKIP
        if choice in q:
            print("\n\ty - yes"
                  "\n\tn - no"
                  "\n\ts - skip"
                  "\n\tl - list files")

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

            while True:
                accepted = AcceptDialog()
                if accepted == Answer.LIST:
                    print("The following files were found:")
                    for file in files_to_copy:
                        print(f"\t{file}")
                if accepted == Answer.YES:
                    copy_target_dir = self.out_dir / path_prefix
                    self.mkdir_p(copy_target_dir, dry_run=dry_run)
                    for file in files_to_copy:
                        self.copy(file.absolute(), self.out_dir / path_prefix, dry_run=dry_run)
                    print("Files copied successfully")
                    break
                elif accepted == Answer.NO:
                    # Unset path prefix if this is determined to not be the root directory of specified files
                    if initialized_path_prefix:
                        path_prefix = None
                    break
                elif accepted == Answer.SKIP:
                    # Skip file copying and recursive directory parsing
                    return

        for ch_dir in dirs_to_parse:
            new_path_prefix = (path_prefix / ch_dir.name) if path_prefix else None
            self.parse_dir(ch_dir, dry_run, new_path_prefix)

    def mkdir_p(self, path: Path, dry_run: bool):
        # TODO: Add statistics
        if dry_run:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST or os.path.isdir(path):
                pass
            else:
                raise exc

    def copy(self, src_file: Path, target: Path, dry_run: bool):
        # TODO: Add statistics
        if dry_run:
            return
        shutil.copy(src_file, target)

