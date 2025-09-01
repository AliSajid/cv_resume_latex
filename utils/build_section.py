#!/usr/bin/env python3
"""
Section Builder for Modular CV System
=====================================

This script builds CV sections by assembling individual units based on tags,
priorities, and item limits. It reads metadata from unit_metadata.yaml and
combines the appropriate unit files into section files.

Usage:
    python build_section.py education --tags full_cv --output sections/education_full.tex
    python build_section.py experience --tags short_cv --max-items 3 --output sections/experience_short.tex
"""

import argparse
from pathlib import Path
import sys
import os
import re

def load_metadata():
    """Load the unit metadata from YAML file using simple parsing."""
    metadata_path = Path('utils/unit_metadata.yaml')
    if not metadata_path.exists():
        print(f"Error: Metadata file {metadata_path} not found!")
        sys.exit(1)

    # Simple YAML parser for our specific format
    metadata = {}
    current_section = None
    current_unit = None

    with open(metadata_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            original_line = line
            line = line.rstrip()  # Remove trailing whitespace but preserve leading

            if not line.strip() or line.strip().startswith('#'):
                continue

            # Top-level sections (education:, experience:, etc.)
            if line.endswith(':') and not line.startswith(' '):
                current_section = line[:-1]
                metadata[current_section] = {}
                continue

            # Unit entries (  phd_biomedical_sciences:)
            if line.startswith('  ') and line.endswith(':') and not line.startswith('    '):
                current_unit = line.strip()[:-1]
                if current_section:
                    metadata[current_section][current_unit] = {}
                continue

            # Properties (    tags: [full_cv, short_cv])
            if line.startswith('    ') and ':' in line:
                key, value = line.strip().split(':', 1)
                value = value.strip()

                if current_section and current_unit:
                    # Parse lists [tag1, tag2, tag3]
                    if value.startswith('[') and value.endswith(']'):
                        # Remove brackets and split on commas
                        tags_str = value[1:-1]
                        tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
                        metadata[current_section][current_unit][key] = tags
                    # Parse numbers
                    elif value.isdigit():
                        metadata[current_section][current_unit][key] = int(value)
                    # Parse strings (remove quotes)
                    else:
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        metadata[current_section][current_unit][key] = value

    return metadata

def build_section(section_name, tags=None, max_items=None, exclude_tags=None):
    """
    Build a section by assembling units based on criteria.

    Args:
        section_name: Name of the section (education, experience, etc.)
        tags: List of tags to filter by (include units with any of these tags)
        max_items: Maximum number of items to include
        exclude_tags: List of tags to exclude (exclude units with any of these tags)

    Returns:
        String containing the assembled section content
    """
    metadata = load_metadata()
    section_data = metadata.get(section_name, {})

    if not section_data:
        print(f"Warning: No metadata found for section '{section_name}'")
        return ""

    # Filter units by tags
    filtered_units = []
    for unit_name, unit_meta in section_data.items():
        unit_tags = unit_meta.get('tags', [])

        # Skip if exclude_tags specified and unit has any of them
        if exclude_tags and any(tag in unit_tags for tag in exclude_tags):
            continue

        # Include if no tags filter specified, or unit has any of the required tags
        if tags is None or any(tag in unit_tags for tag in tags):
            filtered_units.append((unit_name, unit_meta))

    # Sort by priority (lower number = higher priority)
    filtered_units.sort(key=lambda x: x[1].get('priority', 999))

    # Limit number of items
    if max_items:
        filtered_units = filtered_units[:max_items]

    # Build section content
    section_content = []
    for unit_name, unit_meta in filtered_units:
        unit_file = Path(f"units/{section_name}/{unit_name}.tex")
        if unit_file.exists():
            with open(unit_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:  # Only add non-empty content
                    section_content.append(content)
        else:
            print(f"Warning: Unit file {unit_file} not found!")

    if not section_content:
        print(f"Warning: No content generated for section '{section_name}'")
        return ""

    return '\n\n'.join(section_content)

def get_section_header(section_name):
    """Get the appropriate LaTeX section header for a given section."""
    headers = {
        'education': r'\section{Education, Scholarships \& Distinctions}',
        'experience': r'\section{Professional Experience}',
        'projects': r'\section{Open–Source Tools \& Projects}',
        'teaching': r'\section{Teaching Experience}',
        'skills': r'\section{Technical Skills}',
        'publications': r'\section{Publications}',
        'activism': r'\section{Community Service \& Activism}',
    }
    return headers.get(section_name, f'\\section{{{section_name.title()}}}')

def main():
    parser = argparse.ArgumentParser(
        description='Build CV sections from modular units',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build full education section
  python build_section.py education --tags full_cv --output sections/education_full.tex

  # Build short experience section with max 3 items
  python build_section.py experience --tags short_cv --max-items 3 --output sections/experience_short.tex

  # Build projects section excluding certain tags
  python build_section.py projects --tags full_cv --exclude-tags maintenance --output sections/projects_full.tex

  # Print content to stdout (no output file)
  python build_section.py skills --tags technical
        """
    )

    parser.add_argument('section', help='Section name (education, experience, projects, etc.)')
    parser.add_argument('--tags', nargs='+', help='Include units with any of these tags')
    parser.add_argument('--exclude-tags', nargs='+', help='Exclude units with any of these tags')
    parser.add_argument('--max-items', type=int, help='Maximum number of items to include')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--include-header', action='store_true',
                       help='Include LaTeX section header in output')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if args.verbose:
        print(f"Building section: {args.section}")
        if args.tags:
            print(f"Including tags: {args.tags}")
        if args.exclude_tags:
            print(f"Excluding tags: {args.exclude_tags}")
        if args.max_items:
            print(f"Max items: {args.max_items}")

    # Build the section content
    content = build_section(args.section, args.tags, args.max_items, args.exclude_tags)

    if not content:
        print(f"No content generated for section '{args.section}'")
        sys.exit(1)

    # Add section header if requested
    if args.include_header:
        header = get_section_header(args.section)
        content = f"{header}\n\n{content}"

    # Output to file or stdout
    if args.output:
        output_path = Path(args.output)
        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        if args.verbose:
            print(f"Section written to: {output_path}")
    else:
        print(content)

if __name__ == "__main__":
    main()
