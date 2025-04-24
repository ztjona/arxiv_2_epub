# -*- coding: utf-8 -*-

"""
arxiv2epub - Summary

Usage:
    arxiv2epub.py <arxiv_url> [--output=<output>] [--verbose] [--debug]
    arxiv2epub.py -h|--help
    arxiv2epub.py --version

Options:
    -h,--help               show help.
"""

"""
Python 3
22 / 04 / 2025
@author: z_tjona

"I find that I don't understand things unless I try to program them."
-Donald E. Knuth
"""


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

    logging.info(f"Downloading LaTeX source from {source_url}...")
    response = requests.get(source_url, stream=True)

    if response.status_code == 200:
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        logging.info(f"Downloaded LaTeX source to {output_path}")
        return output_path
    else:
        logging.error(
            f"Failed to download LaTeX source. HTTP Status: {response.status_code}"
        )
        raise Exception(f"Failed to download LaTeX source from {source_url}")


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
    logging.info(f"Unzipping {file_path} to {paper_dir}...")

    try:
        subprocess.run(
            ["tar", "-xzf", file_path, "-C", paper_dir],
            check=True,
        )
        logging.info(f"Unzipped files to {paper_dir}")
        return paper_dir
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to unzip file: {e}")
        raise Exception(f"Error unzipping file: {file_path}")


def compile_latex_to_epub(latex_dir, output_file="output.epub"):
    """
    Compiles LaTeX files into an EPUB format using pandoc.

    Args:
        latex_dir (str): Directory containing the LaTeX files.
        output_file (str): Path to the output EPUB file.

    Returns:
        str: Path to the generated EPUB file.
    """
    logging.info(f"Compiling LaTeX files in {latex_dir} to EPUB: {output_file}...")

    try:
        # Find the main .tex file (assumes a single .tex file in the directory)
        tex_files = [f for f in os.listdir(latex_dir) if f.endswith(".tex")]
        if not tex_files:
            raise Exception("No .tex file found in the directory.")
        main_tex_file = os.path.join(latex_dir, tex_files[0])

        # Run pandoc to convert the .tex file to .epub
        subprocess.run(
            [
                "pandoc",
                main_tex_file,
                "-o",
                output_file,
                "--mathjax",  # Use MathJax for rendering math
                "--resource-path",
                latex_dir,  # Set resource path to the LaTeX directory
                "--fail-if-warnings",  # Fail if there are warnings
            ],
            check=True,
            shell=True,
        )
        logging.info(f"EPUB file generated at: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to compile LaTeX to EPUB: {e}")
        raise Exception(f"Error compiling LaTeX to EPUB: {latex_dir}")


def main(args):
    arxiv_url = args["<arxiv_url>"]
    output_file = (
        args["--output"] if args["--output"] else "output.epub"
    )  # Ensure default value
    # try:
    
    latex_file = download_latex_from_arxiv(arxiv_url)
    extracted_dir = unzip_latex_file(latex_file)
        # epub_file = compile_latex_to_epub(extracted_dir, output_file)
        # logging.info(f"EPUB file successfully created: {epub_file}")
    # except Exception as e:
    #     logging.error(f"Error: {e}")


if __name__ == "__main__":
    args = docopt(
        doc=__doc__,
        version="1",
    )
    main(args)
