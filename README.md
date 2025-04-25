# LaTeX to EPUB Conversion Tool

## Overview

This project is a command-line interface (CLI) tool designed to convert academic papers from ArXiv into EPUB format. The tool simplifies the process of downloading LaTeX source files, extracting their content, and converting them into a format suitable for e-readers and mobile devices.

## Features

- Download LaTeX source files directly from ArXiv.
- Extract and process LaTeX files.
- Automatically retrieve the title from the LaTeX file (if possible).
- If the main LaTeX file is not `main.tex`, it is prompted to be selected by the user..
- Convert LaTeX to EPUB format for easy reading.
- Option to clean up temporary files after conversion.

## Requirements

- Python 3.x
- System Python installation (no virtual environments required).
- Required tools:
  - `latexml` and `latexmlpost` for LaTeX to XML/HTML conversion.
  - `ebook-convert` (from Calibre) for HTML to EPUB conversion.
  - `tar` for extracting `.tar.gz` files.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/latex_2_epub.git
   cd latex_2_epub
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the required tools (`latexml`, `ebook-convert`, etc.) are installed and available in your system's PATH.

## Usage

Run the tool using the following command:

```bash
python arxiv2epub.py <arxiv_url> [--latex_file=<latex_file>] [--output=<output>] [--clear]
```

### Options

- `<arxiv_url>`: The URL of the ArXiv paper (e.g., `https://arxiv.org/abs/1234.56789`).
- `--latex_file=<latex_file>`: Specify the main LaTeX file name (default: `main.tex`). If the main file is not `main.tex`, it will be scanned from the folder and user can select the found tex files.
- `--output=<output>`: Specify the output EPUB file name (default: `out/$1.epub`, where `$1` is replaced by the paper's title retrieved from the LaTeX file).
- `--clear`: Remove temporary files (non-EPUB files) from the `out` directory after conversion.

### Example

```bash
python arxiv2epub.py https://arxiv.org/abs/1234.56789 --output=my_paper.epub --clear
```

## Project Structure

```
latex_2_epub/
├── arxiv2epub.py       # Main script for the CLI tool
├── README.md           # Project documentation
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
└── out/                # Output directory for EPUB files
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [LaTeXML](https://dlmf.nist.gov/LaTeXML) for LaTeX to XML/HTML conversion.
- [Calibre](https://calibre-ebook.com/) for EPUB conversion.
- Inspired by the need to make academic papers more accessible on e-readers.