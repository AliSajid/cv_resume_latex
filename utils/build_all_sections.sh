#!/bin/bash
# Build all sections for the modular CV system

set -e # Exit on any error

echo "Building modular CV sections..."

# Create sections directory if it doesn't exist
mkdir -p sections

echo "Building full CV sections..."

# Full CV sections (include everything marked for full CV)
python3 utils/build_section.py education --tags full_cv --include-header --output sections/education_full.tex
python3 utils/build_section.py experience --tags full_cv --include-header --output sections/experience_full.tex
python3 utils/build_section.py projects --tags full_cv --include-header --output sections/projects_full.tex
python3 utils/build_section.py teaching --tags full_cv --include-header --output sections/teaching_full.tex
python3 utils/build_section.py skills --tags full_cv --include-header --output sections/skills_full.tex
python3 utils/build_section.py activism --tags full_cv --include-header --output sections/activism_full.tex

echo "Building short CV sections..."

# Short CV sections (limited items, only high priority)
python3 utils/build_section.py education --tags short_cv --max-items 3 --include-header --output sections/education_short.tex
python3 utils/build_section.py experience --tags short_cv --max-items 3 --include-header --output sections/experience_short.tex
python3 utils/build_section.py projects --tags short_cv --max-items 4 --include-header --output sections/projects_short.tex
python3 utils/build_section.py teaching --tags short_cv --max-items 2 --include-header --output sections/teaching_short.tex
python3 utils/build_section.py skills --tags short_cv --include-header --output sections/skills_short.tex
python3 utils/build_section.py activism --tags short_cv --include-header --output sections/activism_short.tex

echo "Building utra CV sections..."

# UTRA CV sections (limited items, only high priority)
python3 utils/build_section.py education --tags utra --max-items 3 --include-header --output sections/education_utra.tex
python3 utils/build_section.py experience --tags utra --max-items 3 --include-header --output sections/experience_utra.tex
python3 utils/build_section.py projects --tags utra --max-items 4 --include-header --output sections/projects_utra.tex
python3 utils/build_section.py teaching --tags utra --max-items 2 --include-header --output sections/teaching_utra.tex
python3 utils/build_section.py skills --tags utra --include-header --output sections/skills_utra.tex
python3 utils/build_section.py activism --tags utra --include-header --output sections/activism_utra.tex

echo "Building czi CV sections..."

# CZI CV sections (limited items, only high priority)
python3 utils/build_section.py education --tags czi --max-items 3 --include-header --output sections/education_czi.tex
python3 utils/build_section.py experience --tags czi --max-items 3 --include-header --output sections/experience_czi.tex
python3 utils/build_section.py projects --tags czi --max-items 4 --include-header --output sections/projects_czi.tex
python3 utils/build_section.py teaching --tags czi --max-items 2 --include-header --output sections/teaching_czi.tex
python3 utils/build_section.py skills --tags czi --include-header --output sections/skills_czi.tex
python3 utils/build_section.py activism --tags czi --include-header --output sections/activism_czi.tex

echo "Building specialized sections..."

# Academic-focused sections
python3 utils/build_section.py education --tags academic --include-header --output sections/education_academic.tex
python3 utils/build_section.py experience --tags academic research --include-header --output sections/experience_academic.tex
python3 utils/build_section.py projects --tags academic --include-header --output sections/projects_academic.tex

# Industry/tech-focused sections
python3 utils/build_section.py experience --tags technology --include-header --output sections/experience_tech.tex
python3 utils/build_section.py projects --tags r_package rust api --include-header --output sections/projects_tech.tex

# Current/active items only
python3 utils/build_section.py experience --tags current --include-header --output sections/experience_current.tex
python3 utils/build_section.py projects --tags current --include-header --output sections/projects_current.tex

echo "All sections built successfully!"
echo "Generated files in sections/ directory:"
ls -la sections/
