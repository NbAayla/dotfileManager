# Copyright (C) 2021 Aayla Semyonova
# 
# This file is part of dotfileManager.
# 
# dotfileManager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# dotfileManager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with dotfileManager.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import yaml
import os


# Set up argument parsing
# parser = argparse.ArgumentParser()
# parser.add_argument("--verbose", "-v", help="Increase output verbosity")
# subparsers = parser.add_subparsers(dest="subparser_name", required=True)
# # Arguments for "run" subcommand
# run_subparser = subparsers.add_subparser(dest="run")
# run_subparser.add_argument("config", default="~/.manager_config")
# # Arguments for "validate" subcommand
# validate_subparser = subparsers.add_subparsers(dest="validate")


def validate_config(path):
    """
    Validate the config file provided in argument "path"
    Arguments:
    - path: string, path to config file to validate
    Returns: bool, True if config file is valid
    """
    # Ensure config file in question exists
    if not os.path.exists(path):
        print(f"Error: \"{path}\" does not exist")
        exit(1)
    # Ensure config file in question is a file
    if not os.path.isfile(path):
        print(f"Error: \"{path}\" is not a file")
        exit(1)
    # Attempt to open the file as YAML
    with open(path, "r") as inputFile:
        yaml_content = yaml.load(inputFile, Loader=yaml.FullLoader)
    # TODO: Validate contents
    print(yaml_content)
    return True


def clone_file(src, dest):
    """
    Clone a file from src to dest
    Arguments:
    - src: Source file to copy
    - dest: Destination to copy file to
    Returns: None
    """
    # Ensure the source path exists
    if not os.path.exists(src):
        print(f"Source file does not exist {src} -> {dest}")
        exit(1)
    # Create the destination path if needed
    if not os.path.exists(os.path.dirname(os.path.realpath(dest))):
        os.makedirs(os.path.dirname(os.path.realpath(dest)))
    # Copy the file contents
    with open(src, "rb") as source_file:
        with open(dest, "wb") as dest_file:
            dest_file.write(
                source_file.read()
            )

clone_file("test.yaml", "output_test.yaml")