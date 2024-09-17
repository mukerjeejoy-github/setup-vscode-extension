# setup-vscode-extension

# Project Setup and Extension Creation Script

This repository contains a Python script designed to automate the setup of development environments for various programming languages and to create a new Visual Studio Code (VSCode) extension project. Below is a detailed explanation of the script and its components.

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Functions](#functions)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## Overview

The script performs the following tasks:
1. Checks if certain development tools and languages are installed.
2. Installs missing tools and languages.
3. Creates a new VSCode extension project using Yeoman.
4. Generates basic server code for the specified language.

## Requirements

- Python 3.x
- `curl`, `tar`, `unzip`, `wget`, `brew`, and `npm` (for package management and installation)
- Administrative access for installations

## Functions

### `run_command(command, cwd=None, stream_output=False)`

Runs a shell command and optionally streams its output.

- **Parameters**:
  - `command`: The shell command to execute.
  - `cwd`: Optional directory to run the command in.
  - `stream_output`: Boolean to determine if output should be streamed.

- **Returns**: Exit code of the command.

### `install_package(package_name, install_command)`

Installs a package if it is not already installed.

- **Parameters**:
  - `package_name`: Name of the package to check.
  - `install_command`: Command to install the package.

### `check_and_install_dotnet()`

Checks if .NET is installed and installs it if not.

### `install_node()`

Installs Node.js if it is not already installed.

### `install_yeoman_and_generator()`

Installs Yeoman and the VSCode Extension Generator globally.

### `install_maven()`

Checks if Maven is installed and installs it if not.

### `install_ruby()`

Checks if Ruby is installed and installs it if not.

### `install_php()`

Checks if PHP is installed and installs it if not.

### `install_go()`

Checks if Go is installed and installs it if not.

### `generate_extension_name_and_identifier(extension_name)`

Generates a formatted extension name and identifier.

- **Parameters**:
  - `extension_name`: The name of the extension.

- **Returns**: Tuple of extension name and identifier.

### `create_extension_project(extension_name)`

Creates a new VSCode extension project using Yeoman.

- **Parameters**:
  - `extension_name`: The name of the extension project.

### `setup_environment_for_language(language)`

Sets up the development environment based on the specified language.

- **Parameters**:
  - `language`: The programming language for the environment setup.

### `create_server_code(language)`

Generates basic server code for the specified language.

- **Parameters**:
  - `language`: The programming language for the server code.

### Language-specific server creation functions

- `create_ruby_server_code()`
- `create_php_server_code()`
- `create_go_server_code()`
- `create_python_server_code()`
- `create_js_server_code(language)`
- `create_csharp_server_code()`
- `create_java_server_code()`

## Usage

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Run the script:
   ```bash
   python setup_vscode_extension.py
   ```
3. Follow the prompts to enter the extension name and select the language for the server

## Troubleshooting
- **Problem**: Installation of tools or packages fails.
  - **Solution**: Ensure you have administrative rights and required tools like curl, wget, and brew installed.
- **Problem**: Unsupported operating system error.
  - **Solution**: Verify that your operating system (Windows, Linux, Darwin) is supported by the script or modify the script to handle your OS

## License
This project is licensed under the GPL 3.0 License. See the LICENSE file for details.
