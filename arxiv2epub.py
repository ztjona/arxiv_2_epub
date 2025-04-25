# -*- coding: utf-8 -*-

"""
arxiv2epub - Summary

Usage:
    arxiv2epub.py <arxiv_url> [--latex_file=<latex_file>] [--output=<output>] [--clear]
    arxiv2epub.py -h|--help
    arxiv2epub.py --version

Options:
    -h,--help               show help.
    --version               show version.
    --output=<output>       output file name [default: out/$1.epub].
    <arxiv_url>             arxiv url.
    --latex_file=<latex_file>  latex file name [default: main.tex].
    --clear                 clear temporary files [default: True].
"""

"""
Python 3
22 / 04 / 2025
@author: z_tjona

"I find that I don't understand things unless I try to program them."
-Donald E. Knuth
"""
import re

# ----------------------------- logging --------------------------
import logging
from sys import stdout
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s] %(message)s",
    stream=stdout,
    datefmt="%m-%d %H:%M:%S",
)
logging.info(datetime.now())


# ----------------------------- #### --------------------------
from docopt import docopt
import requests
import os
import subprocess


# ####################################################################
def download_latex_from_arxiv(arxiv_url, output_dir="downloads"):
    """
    Downloads the LaTeX source code for a given ArXiv URL.

    Args:
        arxiv_url (str): The URL of the ArXiv paper.
        output_dir (str): Directory to save the downloaded LaTeX files.

    Returns:
        str: Path to the downloaded LaTeX file.
    """
    if not arxiv_url.startswith("https://arxiv.org/abs/"):
        raise ValueError("Invalid ArXiv URL. Must start with 'https://arxiv.org/abs/'.")

    paper_id = arxiv_url.split("/")[-1]
    source_url = f"https://arxiv.org/e-print/{paper_id}"

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{paper_id}.tar.gz")

    logging.info(f"Starting download for ArXiv URL: {arxiv_url}")
    response = requests.get(source_url, stream=True)

    if response.status_code == 200:
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        logging.info(f"Download completed. File saved at: {output_path}")
        return output_path
    else:
        logging.error(
            f"Failed to download LaTeX source. HTTP Status: {response.status_code}"
        )
        raise Exception(f"Failed to download LaTeX source from {source_url}")




# ####################################################################
def get_title(latex_file: str) -> str:
    logging.info(f"Extracting title from LaTeX file: {latex_file}")
    rg = r"title\{(.+)[\\\}\{]"
    with open(latex_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    match = re.search(rg, content)
    logging.debug(match)
    if match:
        logging.info(f"Title found: {match.group(1).strip()}")
        return match.group(1).strip()
    else:
        logging.warning("No title found in the LaTeX file.")
        return latex_file


# ####################################################################
def unzip_latex_file(file_path, output_dir="unzipped"):
    """
    Unzips a .tar.gz file into a folder named after the paper ID.

    Args:
        file_path (str): Path to the .tar.gz file.
        output_dir (str): Base directory to extract the contents.

    Returns:
        str: Path to the directory containing the extracted files.
    """
    paper_id = os.path.basename(file_path).replace(".tar.gz", "")
    paper_dir = os.path.join(output_dir, paper_id)
    os.makedirs(paper_dir, exist_ok=True)
    logging.info(f"Preparing to unzip file: {file_path}")

    try:
        subprocess.run(
            ["tar", "-xzf", file_path, "-C", paper_dir],
            check=True,
        )
        logging.info(f"Extraction completed. Files are in: {paper_dir}")
        return paper_dir
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to unzip file: {e}")
        raise Exception(f"Error unzipping file: {file_path}")


# def compile_latex_to_epub(latex_dir, output_file="output.epub"):
#     """
#     Compiles LaTeX files into an EPUB format using pandoc.

#     Args:
#         latex_dir (str): Directory containing the LaTeX files.
#         output_file (str): Path to the output EPUB file.

#     Returns:
#         str: Path to the generated EPUB file.
#     """
#     logging.info(f"Compiling LaTeX files in {latex_dir} to EPUB: {output_file}...")

#     try:
#         # Find the main .tex file (assumes a single .tex file in the directory)
#         tex_files = [f for f in os.listdir(latex_dir) if f.endswith(".tex")]
#         if not tex_files:
#             raise Exception("No .tex file found in the directory.")
#         main_tex_file = os.path.join(latex_dir, tex_files[0])

#         # Run pandoc to convert the .tex file to .epub
#         subprocess.run(
#             [
#                 "pandoc",
#                 main_tex_file,
#                 "-o",
#                 output_file,
#                 "--mathjax",  # Use MathJax for rendering math
#                 "--resource-path",
#                 latex_dir,  # Set resource path to the LaTeX directory
#                 "--fail-if-warnings",  # Fail if there are warnings
#             ],
#             check=True,
#             shell=True,
#         )
#         logging.info(f"EPUB file generated at: {output_file}")
#         return output_file
#     except subprocess.CalledProcessError as e:
#         logging.error(f"Failed to compile LaTeX to EPUB: {e}")
#         raise Exception(f"Error compiling LaTeX to EPUB: {latex_dir}")


def run_latexml(latex_file: str, output_file: str = "out/main.xml") -> None:
    """
    Runs the latexml command to convert a LaTeX file to XML format.

    Args:
        latex_file (str): Path to the LaTeX file.
        output_file (str): Path to the output XML file. Defaults to 'main.xml'.

    Raises:
        RuntimeError: If the latexml command fails.
    """
    logging.info(f"Running latexml on file: {latex_file}, output: {output_file}")
    try:
        command = ["latexml", f"--dest={output_file}", latex_file,"--verbose"]
        result = subprocess.run(command, check=True)
        logging.info(f"latexml command executed successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running latexml: {e.stderr}")
        raise RuntimeError("Failed to run latexml command") from e
    

def run_latexmlpost(xml_file: str = "out/main.xml", output_file: str = "out/main.html") -> None:
    """
    Runs the latexmlpost command to convert an XML file to HTML format.

    Args:
        xml_file (str): Path to the XML file.
        output_file (str): Path to the output HTML file. Defaults to 'main.html'.

    Raises:
        RuntimeError: If the latexmlpost command fails.
    """
    logging.info(f"Running latexmlpost on file: {xml_file}, output: {output_file}")
    try:
        command = ["latexmlpost", f"--dest={output_file}", xml_file]
        result = subprocess.run(command, check=True)
        logging.info(f"latexmlpost command executed successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running latexmlpost: {e.stderr}")
        raise RuntimeError("Failed to run latexmlpost command") from e
    
def convert_html_to_epub(epub_file: str, html_file: str = "out/main.html") -> None:
    """
    Converts an HTML file to EPUB format using the ebook-convert command.

    Args:
        epub_file (str): Path to the output EPUB file.
        html_file (str): Path to the HTML file. Defaults to 'main.html'.
    Raises:
        RuntimeError: If the ebook-convert command fails.
    """
    logging.info(f"Converting HTML to EPUB. HTML file: {html_file}, EPUB file: {epub_file}")
    try:
        command = [
            "ebook-convert",
            html_file,
            epub_file,
            "--language",
            "en",
            "--no-default-epub-cover",
        ]
        result = subprocess.run(command, check=True)
        logging.info(f"ebook-convert command executed successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running ebook-convert: {e.stderr}")
        raise RuntimeError("Failed to convert HTML to EPUB") from e
    

def list_tex_files(folder: str) -> list:
    """
    Lists all .tex files in the specified folder.
    E.g. unzipped/2503.05613/acl_latex.tex
    Args:
        folder (str): Path to the folder.

    Returns:
        list: A list of .tex file paths.
    """
    if not os.path.isdir(folder):
        raise ValueError(f"The folder '{folder}' does not exist or is not a directory.")

    tex_files = [f for f in os.listdir(folder) if f.endswith(".tex")]
    logging.info(f"Found {len(tex_files)} .tex files in folder '{folder}'.")
    logging.info(f"List of .tex files: {tex_files}")
    return tex_files


def ensure_latex_element_exists(tex_files: list, element: str) -> str:
    """
    Ensures that the specified LaTeX element exists in one of the .tex files.
    If not found, prompts the user to select a file from the list.

    Args:
        tex_files (list): List of .tex file paths.
        element (str): The LaTeX element to search for (e.g., "\\begin{document}").

    Returns:
        str: Path to the selected .tex file.
    """
    logging.info(f"Ensuring LaTeX element '{element}' exists in the provided .tex files.")
    if element in tex_files:
        logging.info(f"Found LaTeX element '{element}' in file '{tex_files[element]}'.")
        return element
    else:
        print("LaTeX element not found in any file.")
        print("Available .tex files:")
        for i, file in enumerate(tex_files):
            print(f"{i}: {file}")
        selected_index = int(input("Select a file by index: "))
        if selected_index < 0 or selected_index >= len(tex_files):
            raise ValueError("Invalid index selected.")
        logging.info(f"Selected LaTeX file: {tex_files[selected_index]}")
        return tex_files[selected_index]

def delete_non_epub_files(output_dir: str = "out") -> None:
    """
    Deletes all files in the specified directory that are not EPUB files.

    Args:
        output_dir (str): The directory to clean. Defaults to 'out'.
    """
    if not os.path.isdir(output_dir):
        logging.warning(f"Output directory '{output_dir}' does not exist. Skipping cleanup.")
        return

    logging.info(f"Cleaning up non-EPUB files in directory: {output_dir}")
    for file_name in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file_name)
        if not file_name.endswith(".epub") and os.path.isfile(file_path):
            try:
                os.remove(file_path)
                logging.info(f"Deleted file: {file_path}")
            except Exception as e:
                logging.error(f"Failed to delete file '{file_path}': {e}")

def main(args):
    logging.info("Starting main process with arguments:")
    logging.info(args)
    arxiv_url = args["<arxiv_url>"]
    latex_file = args["--latex_file"]
    output_file = args["--output"]
    clear_temp_files = args["--clear"]

    latex_file = download_latex_from_arxiv(arxiv_url)
    extracted_dir = unzip_latex_file(latex_file)
    logging.info(f"Extracted directory: {extracted_dir}")

    latex_found = list_tex_files(extracted_dir)
    latex_file_name = ensure_latex_element_exists(latex_found, latex_file)

    latex_full_file = os.path.join(extracted_dir, latex_file_name)
    title = get_title(latex_full_file)

    if "$1" in output_file:
        output_file = output_file.replace("$1", title)
    
    run_latexml(latex_full_file)
    run_latexmlpost()
    convert_html_to_epub(output_file)

    if clear_temp_files:
        delete_non_epub_files("out")

    logging.info(f"Final EPUB file created: {output_file}")


if __name__ == "__main__":
    logging.info("Program started.")
    args = docopt(
        doc=__doc__,
        version="1",
    )
    logging.info(args)
    main(args)
    logging.info("Program finished.")
