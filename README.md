[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg?style=flat-square)](https://opensource.org/licenses/)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/NbAayla/dotfileManager?style=flat-square)
# dotfileManager
A program I mage to manage my dotfiles after being dissatisfied with how much other managers were doing and being annoyed that they left artifacts in the dotfile repository.
# Usage
This program has two subcommands:
1. validate: Validate the given config (passed with `-c` or ``--config``) without copying any files
1. run: Validate and execute the config file and copy files
## Arguments:
Note that this program does have a verbosity flag, but it is currently not implemented
```
main.py [-h] [--verbose VERBOSE] {run,validate} ...

positional arguments:
  {run,validate}

optional arguments:
  -h, --help            show this help message and exit
  --verbose VERBOSE, -v VERBOSE
                        Increase output verbosity
```
## Configuration Files
The files copied to the dotfiles repository location are configured in a YAML file (`~/.manager_config.yaml` by default). A valid configuration file must have a `destination` value and at least one `copy` action. Below is my configuration file for example:
```yaml
destination: ~/.dotfiles

copy:
  ~/.vimrc: vimrc
  ~/.zshrc: zshrc
  ~/.bash_profile: bash_profile
  ~/.bashrc: bashrc
  ~/.config/i3/config: config/i3/config
  ~/.config/i3status/config:  config/i3status/config
```
