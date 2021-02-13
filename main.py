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
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", "-v", help="Increase output verbosity")
subparsers = parser.add_subparsers(dest="subparser_name", required=True)
# Arguments for "run" subcommand
run_subparser = subparsers.add_parser("run")
run_subparser.add_argument("--config", "-c", default="~/.manager_config.yaml", help="Configuration file to execute")
# Arguments for "validate" subcommand
validate_subparser = subparsers.add_parser("validate")
validate_subparser.add_argument("--config", "-c", default="~/.manager_config.yaml", help="Configuration file to execute")
arguments = parser.parse_args()


def resolve_home_dir(path):
    """
    Resolve ~ to the HOME environment variable because Python is too stupid to do it for me
    Inputs:
    - path: Path to resolve
    Returns: String of new path or False if the operation failed
    """
    if os.environ["HOME"]:
        return path.replace("~", os.environ["HOME"])
    else:
        print("FATAL: Environment variable \"HOME\" is not defined.")
        return False


def validate_config(path):
    """
    Validate the config file provided in argument "path"
    Arguments:
    - path: string, path to config file to validate
    Returns: bool, True if config file is valid
    """
    path = resolve_home_dir(path)
    # Ensure config file in question exists
    if not os.path.exists(path):
        print(f"ERROR: \"{path}\" does not exist")
        return False
    # Ensure config file in question is a file
    if not os.path.isfile(path):
        print(f"ERROR: \"{path}\" is not a file")
        return False
    # Attempt to open the file as YAML
    with open(path, "r") as inputFile:
        yaml_content = yaml.load(inputFile, Loader=yaml.FullLoader)
    # Ensure required values are present
    required_values = ["destination", "copy"]
    for value in required_values:
        if not value in yaml_content:
            print(f"FATAL: Required value \"{value}\" not found in configuration {path}")
            return False
    # Ensure all copy operations have a destination
    for operation in yaml_content["copy"]:
        if not yaml_content["copy"][operation]:
            print(f"FATAL: All \"copy\" actions must have a source and destination")
            return False
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
        print(f"ERROR: Source file does not exist {src} -> {dest}")
        return False
    # Create the destination path if needed
    destination_path = resolve_home_dir(os.path.dirname(
            os.path.realpath(dest)
    ))
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    # Copy the file contents
    src = resolve_home_dir(src)
    dest = resolve_home_dir(os.path.join(destination_path, dest))
    with open(src, "rb") as source_file:
        with open(dest, "wb") as dest_file:
            dest_file.write(
                source_file.read()
            )
    print(f"Copied: {src} -> {dest}")


def execute_config(path):
    """
    Execute a given config file
    Arguments:
    - path: Path to configuration file to execute
    Returns: None
    """
    path = resolve_home_dir(path)
    if not validate_config(path):
        # Configuration file failed to validate
        exit(1)
    with open(path, "r") as inputFile:
        yaml_content = yaml.load(inputFile, Loader=yaml.FullLoader)
    # Create destination path if needed
    destination_path = yaml_content["destination"]
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    # Begin copying files
    for operation in yaml_content["copy"]:
        status = clone_file(
            resolve_home_dir(operation), 
            resolve_home_dir(
                os.path.join(
                    destination_path,
                    yaml_content["copy"][operation]
                )
            )
        )
        if status is False:
            # Copy operation failed
            exit(1)
    # All files copied successfully
    return True


# Execute provided subcommand
if arguments.subparser_name == "run":
    execute_config(arguments.config)
elif arguments.subparser_name == "validate":
    if validate_config(arguments.config):
        exit(0)
    else:
        exit(1)
else:
    print(f"{arguments.subparser_name} is not a valid command")
    exit(1)