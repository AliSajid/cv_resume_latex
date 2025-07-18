#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pybtex"
# ]
# ///

import os
import sys
import argparse
from collections import defaultdict
from pybtex.database import parse_file, BibliographyData, Entry


def load_keyword_mappings(mapping_file="keyword-map.txt"):
    """Load keyword mappings from file."""
    mappings = {}
    if os.path.exists(mapping_file):
        with open(mapping_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if " -> " in line:
                        old, new = line.split(" -> ", 1)
                        mappings[old.strip()] = new.strip()
    return mappings


def process_keywords(entry, keyword_mappings, valid_prefixes=None):
    """Apply keyword remapping and filter to only prefixed keywords."""
    if "keywords" not in entry.fields:
        return entry

    if valid_prefixes is None:
        valid_prefixes = ["pub:", "topic:", "meta:"]

    keywords = [kw.strip() for kw in entry.fields["keywords"].split(",")]
    remapped = []

    for kw in keywords:
        # First remap the keyword
        mapped_kw = keyword_mappings.get(kw, kw)

        # Only keep if it has a valid prefix
        if any(mapped_kw.startswith(prefix) for prefix in valid_prefixes):
            remapped.append(mapped_kw)

    # Create new entry with filtered keywords
    new_entry = Entry(entry.type)
    # Convert OrderedCaseInsensitiveDict to regular dict before copying
    new_entry.fields = dict(entry.fields)

    if remapped:
        new_entry.fields["keywords"] = ", ".join(remapped)
    else:
        # Remove keywords field if no valid keywords remain
        new_entry.fields.pop("keywords", None)

    new_entry.persons = entry.persons

    return new_entry


def extract_tagged_entries(bib_data, tag_prefix):
    """Extract entries based on keyword tags."""
    subsets = defaultdict(dict)
    all_entries = {}

    for key, entry in bib_data.entries.items():
        keywords = entry.fields.get("keywords", "")
        tags = [
            kw.strip()
            for kw in keywords.split(",")
            if kw.strip().startswith(tag_prefix)
        ]

        for tag in tags:
            subset_name = tag[len(tag_prefix) :].strip()
            if subset_name:
                subsets[subset_name][key] = entry

        all_entries[key] = entry

    return subsets, all_entries


def main():
    parser = argparse.ArgumentParser(
        description="Process keywords and split bibliography file"
    )
    parser.add_argument("input_bib", help="Input .bib file")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument(
        "--prefix", default="pub:", help="Keyword prefix (default: pub:)"
    )
    parser.add_argument(
        "--keyword-map", default="keyword-map.txt", help="Keyword mapping file"
    )
    parser.add_argument(
        "--valid-prefixes",
        nargs="+",
        default=["pub:", "topic:", "meta:"],
        help="Valid keyword prefixes to keep (default: pub: topic: meta:)",
    )

    args = parser.parse_args()

    if not os.path.exists(args.input_bib):
        print(f"Error: {args.input_bib} not found")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    # Load keyword mappings
    keyword_mappings = load_keyword_mappings(args.keyword_map)

    # Parse input file
    bib_data = parse_file(args.input_bib)

    # Process keywords
    processed_entries = {}
    for key, entry in bib_data.entries.items():
        processed_entries[key] = process_keywords(
            entry, keyword_mappings, args.valid_prefixes
        )

    # Create processed bibliography
    processed_bib = BibliographyData(entries=processed_entries)

    # Extract tagged entries
    subsets, all_entries = extract_tagged_entries(processed_bib, args.prefix)

    # Write subset files
    for name, entries in subsets.items():
        out_path = os.path.join(args.output_dir, f"{name}.bib")
        BibliographyData(entries=entries).to_file(out_path)
        print(f"→ {name}.bib ({len(entries)} entries)")

    # Write all.bib if it doesn't exist
    all_path = os.path.join(args.output_dir, "all.bib")
    if not os.path.exists(all_path):
        BibliographyData(entries=all_entries).to_file(all_path)
        print(f"→ all.bib ({len(all_entries)} entries)")


if __name__ == "__main__":
    main()
