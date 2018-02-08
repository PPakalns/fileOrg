#!/usr/bin/env python3

import configparser
import argparse
from pathlib import Path
from organizer import OrganizerInstance

def organize(args):

    config = configparser.ConfigParser()
    config.read(args.config)
    if "fileOrg" not in config.sections():
        raise "fileOrg section not in config file. Please see example_config.ini"

    dry_run = config.getboolean("fileOrg", 'dry_run')
    ext_list = config.get("fileOrg", 'extensions').split(' ')
    src_dir = Path(config.get("fileOrg", 'src_dir'))
    out_dir = Path(config.get("fileOrg", 'out_dir'))

    organizer = OrganizerInstance(src_dir, out_dir, ext_list)
    organizer.organize(dry_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', required=True, dest='config', type=str, help="Location of config file")
    args = parser.parse_args()
    organize(args)

