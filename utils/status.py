#!/usr/bin/env python3
"""
Modular CV System Status
=======================

Shows the current status of the modular CV system including:
- Available units and their tags
- Generated sections
- Built documents
- System health
"""

import os
from pathlib import Path
import re

def load_simple_metadata():
    """Load unit metadata using simple parsing."""
    metadata_path = Path('utils/unit_metadata.yaml')
    if not metadata_path.exists():
        return {}

    metadata = {}
    current_section = None
    current_unit = None

    with open(metadata_path, 'r') as f:
        for line in f:
            line = line.rstrip()

            if not line.strip() or line.strip().startswith('#'):
                continue

            # Top-level sections
            if line.endswith(':') and not line.startswith(' '):
                current_section = line[:-1]
                metadata[current_section] = {}
                continue

            # Unit entries
            if line.startswith('  ') and line.endswith(':') and not line.startswith('    '):
                current_unit = line.strip()[:-1]
                if current_section:
                    metadata[current_section][current_unit] = {}
                continue

            # Properties
            if line.startswith('    ') and ':' in line:
                key, value = line.strip().split(':', 1)
                value = value.strip()

                if current_section and current_unit:
                    if value.startswith('[') and value.endswith(']'):
                        tags_str = value[1:-1]
                        tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
                        metadata[current_section][current_unit][key] = tags
                    elif value.isdigit():
                        metadata[current_section][current_unit][key] = int(value)
                    else:
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        metadata[current_section][current_unit][key] = value

    return metadata

def count_files_in_dir(directory):
    """Count files in a directory."""
    if not os.path.exists(directory):
        return 0
    return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

def get_file_size(filepath):
    """Get human-readable file size."""
    if not os.path.exists(filepath):
        return "Not found"

    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}TB"

def main():
    print("🔧 Modular CV System Status")
    print("=" * 50)

    # Load metadata
    metadata = load_simple_metadata()

    # System overview
    print("\n📊 System Overview:")
    total_units = sum(len(units) for units in metadata.values())
    print(f"   Sections: {len(metadata)} types")
    print(f"   Units: {total_units} total")
    print(f"   Generated sections: {count_files_in_dir('sections')}")

    # Units by section
    print("\n📦 Units by Section:")
    for section, units in metadata.items():
        print(f"   {section}: {len(units)} units")

        # Show tags for this section
        all_tags = set()
        for unit_data in units.values():
            all_tags.update(unit_data.get('tags', []))

        if all_tags:
            print(f"      Tags: {', '.join(sorted(all_tags))}")

    # Generated sections
    print("\n🔧 Generated Sections:")
    sections_dir = Path('sections')
    if sections_dir.exists():
        section_files = list(sections_dir.glob('*.tex'))
        if section_files:
            for section_file in sorted(section_files):
                size = get_file_size(section_file)
                print(f"   {section_file.name} ({size})")
        else:
            print("   No sections generated yet")
    else:
        print("   Sections directory not found")

    # Built documents
    print("\n📄 Built Documents:")
    pdf_found = False

    for doc_dir in ['short_cv', 'long_cv', 'resume']:
        pdf_path = Path(doc_dir) / f"{doc_dir}.pdf"
        if pdf_path.exists():
            size = get_file_size(pdf_path)
            mtime = os.path.getmtime(pdf_path)
            import time
            time_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(mtime))
            print(f"   {pdf_path} ({size}, {time_str})")
            pdf_found = True

    if not pdf_found:
        print("   No PDFs found")

    # System health
    print("\n🏥 System Health:")

    # Check required files
    required_files = [
        'utils/unit_metadata.yaml',
        'utils/build_section.py',
        'utils/build_all_sections.sh',
        'utils/build.sh'
    ]

    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"   ❌ Missing files: {', '.join(missing_files)}")
    else:
        print("   ✅ All required files present")

    # Check units directory structure
    for section in metadata.keys():
        unit_dir = Path('units') / section
        if not unit_dir.exists():
            print(f"   ⚠️  Missing units directory: {unit_dir}")
        else:
            # Check if all units have corresponding files
            missing_units = []
            for unit_name in metadata[section].keys():
                unit_file = unit_dir / f"{unit_name}.tex"
                if not unit_file.exists():
                    missing_units.append(unit_name)

            if missing_units:
                print(f"   ⚠️  Missing unit files in {section}: {', '.join(missing_units)}")

    # Build suggestions
    print("\n💡 Suggestions:")

    if not sections_dir.exists() or not list(sections_dir.glob('*.tex')):
        print("   🔧 Run './utils/build_all_sections.sh' to generate sections")

    if not pdf_found:
        print("   📄 Run './utils/build.sh pdfs' to build PDF documents")

    # Quick stats
    print("\n📈 Quick Stats:")
    tag_count = {}
    for section_data in metadata.values():
        for unit_data in section_data.values():
            for tag in unit_data.get('tags', []):
                tag_count[tag] = tag_count.get(tag, 0) + 1

    if tag_count:
        print("   Most common tags:")
        for tag, count in sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"      {tag}: {count} units")

if __name__ == "__main__":
    main()
