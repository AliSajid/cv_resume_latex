#!/usr/bin/env python3
"""
Cover Letter Template Generator for Modular CV System

This script generates cover letter templates using the same styling and
contact information as the corresponding CV documents.
"""

import argparse
import os
from pathlib import Path

# Template for moderncv cover letter
COVER_LETTER_TEMPLATE = """\
\\documentclass[10pt,letterpaper,sans]{{moderncv}}
\\moderncvstyle{{classic}}
\\moderncvcolor{{cerulean}}
\\usepackage[hmargin=0.75in,vmargin=0.75in]{{geometry}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}

% Personal information (matches {cv_file})
\\name{{Ali Sajid}}{{Imami}}
\\address{{2050 Country Trace Pl, Apt 3C}}{{Toledo, OH 43615}}{{USA}}
\\phone[mobile]{{+1~(567)~698~3744}}
\\email{{Ali.Sajid.Imami@gmail.com}}
\\email{{Ali.Imami@rockets.utoledo.edu}}
\\homepage{{www.aliimami.com}}
\\social[linkedin]{{asimami}}
\\social[github]{{AliSajid}}
\\social[orcid]{{0000-0003-3684-3539}}

% Cover letter recipient information
\\recipient{{{recipient}}}{{{organization}\\\\{location}}}
\\date{{\\today}}
\\opening{{{opening}}}
\\closing{{Sincerely,}}

\\begin{{document}}

\\makelettertitle

{content}

\\makeletterclosing

\\end{{document}}"""

def create_cover_letter(directory, recipient, organization, location, opening, content, cv_file="cv.tex"):
    """Create a cover letter template in the specified directory."""

    directory = Path(directory)
    if not directory.exists():
        print(f"Error: Directory {directory} does not exist")
        return False

    cover_letter_content = COVER_LETTER_TEMPLATE.format(
        cv_file=cv_file,
        recipient=recipient,
        organization=organization,
        location=location,
        opening=opening,
        content=content
    )

    cover_letter_path = directory / "cover_letter.tex"

    try:
        with open(cover_letter_path, 'w', encoding='utf-8') as f:
            f.write(cover_letter_content)
        print(f"✅ Cover letter created: {cover_letter_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating cover letter: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Generate cover letter templates")
    parser.add_argument("directory", help="Directory to create cover letter in")
    parser.add_argument("--recipient", default="Hiring Manager",
                       help="Recipient title (default: Hiring Manager)")
    parser.add_argument("--organization", required=True,
                       help="Organization name")
    parser.add_argument("--location", required=True,
                       help="Organization location")
    parser.add_argument("--opening", default="Dear Hiring Manager,",
                       help="Letter opening (default: Dear Hiring Manager,)")
    parser.add_argument("--content",
                       help="Path to file containing letter content")
    parser.add_argument("--cv-file", default="cv.tex",
                       help="Name of corresponding CV file (default: cv.tex)")

    args = parser.parse_args()

    # Default content if none provided
    default_content = """I am writing to express my strong interest in contributing to your organization's mission. As a biomedical scientist with expertise in computational biology, data science, and software development, I am excited about the opportunity to apply my skills to advance scientific research and innovation.

My background includes:

\\begin{itemize}
\\item \\textbf{Computational Biology \\& Bioinformatics}: Extensive experience in analyzing large-scale biological datasets
\\item \\textbf{Software Development}: Proficient in R, Python, and Rust with experience developing research tools
\\item \\textbf{Data Science \\& Machine Learning}: Applied statistical modeling to biomedical research questions
\\item \\textbf{Open Science}: Committed to reproducible research and collaborative science
\\end{itemize}

I am excited about the possibility of contributing to your team's important work and would welcome the opportunity to discuss how my skills and experience can benefit your organization.

Thank you for your consideration. I look forward to hearing from you."""

    content = default_content
    if args.content:
        try:
            with open(args.content, 'r', encoding='utf-8') as f:
                content = f.read().strip()
        except Exception as e:
            print(f"Warning: Could not read content file {args.content}: {e}")
            print("Using default content.")

    success = create_cover_letter(
        args.directory,
        args.recipient,
        args.organization,
        args.location,
        args.opening,
        content,
        args.cv_file
    )

    if success:
        print(f"\\n📝 To customize the cover letter, edit {args.directory}/cover_letter.tex")
        print(f"🔧 To build: cd {args.directory} && latexmk -pdf -silent cover_letter.tex")

if __name__ == "__main__":
    main()
