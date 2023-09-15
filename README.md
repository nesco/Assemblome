# Assemblome

Assemblome is a Python-based tool designed to simplify the parsing and manipulation of genetic data for non-biologists. It provides a user-friendly interface for working with genetic information in a structured manner using `.asb` files.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Assemblome aims to bridge the gap between genetic data and individuals with diverse technical backgrounds. It allows users to define genetic elements, their attributes, and relationships in simple `.asb` files, enabling easy manipulation and analysis of genetic information without requiring in-depth biological expertise.

## Features

- **Tag System:** Define macros to factor long protein, base64 complement strings or other sequences.
- **Import System:** Identical to tags, however instead of replacing a tag by a string, it replaces it by the content of a file. 
- **Functional Expressions:** Enables to express the full genomic information while specifying directly the output protein.
- **Parsing:** Read and interpret `.asb` files to populate the tag and relationship structures.

## Installation

To use Assemblome, follow these steps:

1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/assemblome.git
   ```

2. Navigate to the project directory:
   ```sh
   cd assemblome
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

To start using Assemblome, follow these basic steps:

1. Create or edit `.asb` files to define genetic elements and relationships.
2. ...


## Contributing

Contributions to Assemblome are welcome! Whether you're suggesting new features, reporting issues, or submitting pull requests, your input is valuable.


## License

Assemblome is released under the [MIT License](LICENSE).
