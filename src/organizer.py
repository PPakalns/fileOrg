from pathlib import Path

class OrganizerException(Exception):
    pass

class OrganizerInstance:

    def __init__(self, src_dir: Path, out_dir, ext_list):

        if not (src_dir.exists() and src_dir.is_dir()):
            raise OrganizerException("Provided source directory doesn't exist or isn't a directory!")

    def organize(self, dry_run = False):
        print("Files organized!")
