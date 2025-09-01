# Modular CV System Documentation

## Overview

This repository now uses a three-tier modular system for building CVs and resumes:

1. Individual Units (units/)     → Atomic CV components
2. Assembled Sections (sections/) → Tag-based combinations
3. Final Documents (*/*)         → Complete CVs/resumes

## Directory Structure

```bash
cv_resume_latex/
├── units/                          # 📦 Individual atomic units
│   ├── education/
│   │   ├── phd_biomedical_sciences.tex
│   │   ├── ms_biomedical_sciences.tex
│   │   └── ...
│   ├── experience/
│   │   ├── graduate_research_assistant.tex
│   │   ├── cto_joy_of_urdu.tex
│   │   └── ...
│   ├── projects/
│   │   ├── kinnet.tex
│   │   ├── drugfindr.tex
│   │   └── ...
│   └── skills/, teaching/, activism/
├── sections/                       # 🔧 Assembled sections (auto-generated)
│   ├── education_full.tex
│   ├── education_short.tex
│   ├── experience_full.tex
│   └── ...
├── utils/                          # 🛠️ Build tools
│   ├── unit_metadata.yaml         # Unit configuration
│   ├── build_section.py           # Section builder
│   ├── build_all_sections.sh      # Batch section builder
│   └── build.sh                   # Master build script
└── short_cv/, long_cv/, resume/, czi/  # 📄 Final documents
```

## Usage

### Quick Start with Mise (Recommended)

```bash
# Build everything (sections + bibs + PDFs)
mise run build-all

# Quick build (sections + PDFs, skip bibs)
mise run quick-build

# Build only sections
mise run build-sections

# Build only PDFs
mise run build-pdfs

# Show system status
mise run status

# Clean build artifacts
mise run clean
```

### Specialized Workflows

```bash
# Academic-focused CV
mise run academic-cv

# Tech-focused resume sections
mise run tech-resume

# Individual documents
mise run build-short-cv
mise run build-long-cv
mise run build-resume
mise run build-czi              # Includes cover letter

# Cover letters only
mise run build-czi-cover-letter
```

### Cover Letter Generation

The system supports automatic cover letter generation using `moderncv` styling that matches your CV documents:

```bash
# Create a new cover letter template
python3 utils/create_cover_letter.py <directory> --organization "Company Name" --location "City, State"

# Example: Create cover letter for a new organization
python3 utils/create_cover_letter.py biotech_company --organization "Genentech" --location "South San Francisco, CA"

# Build the cover letter
cd biotech_company && latexmk -pdf -silent cover_letter.tex
```

### Manual Build Scripts

mise run build-czi        # CZI-specific document

```

### Manual Build Scripts

```bash
# Build everything (sections + PDFs)
./utils/build.sh

# Build only sections
./utils/build.sh sections

# Build only PDFs
./utils/build.sh pdfs

# Clean build artifacts
./utils/build.sh clean
```

### Individual Section Building

```bash
# Build full education section
python3 utils/build_section.py education --tags full_cv --include-header --output sections/education_full.tex

# Build short experience section (max 3 items)
python3 utils/build_section.py experience --tags short_cv --max-items 3 --include-header --output sections/experience_short.tex

# Build academic-focused projects
python3 utils/build_section.py projects --tags academic --include-header --output sections/projects_academic.tex

# Build tech-focused experience
python3 utils/build_section.py experience --tags technology --include-header --output sections/experience_tech.tex
```

## Configuration

### Unit Metadata (`utils/unit_metadata.yaml`)

Each unit is configured with:

- **Tags**: Categories for filtering (e.g., `full_cv`, `short_cv`, `academic`, `technology`)
- **Priority**: Sort order (lower number = higher priority)
- **Date Range**: For reference (not used in building)

Example:

```yaml
education:
  phd_biomedical_sciences:
    tags: [full_cv, short_cv, academic, research]
    priority: 1
    date_range: "2021--Present"
```

### Available Tags

- **Document Types**: `full_cv`, `short_cv`
- **Categories**: `academic`, `technology`, `medical`, `research`
- **Status**: `current`, `leadership`
- **Specific**: `r_package`, `rust`, `api`, `bioinformatics`

## Adding New Content

### 1. Create Unit File

```bash
# Create new experience unit
nano units/experience/new_position.tex
```

### 2. Update Metadata

Add entry to `utils/unit_metadata.yaml`:

```yaml
experience:
  new_position:
    tags: [full_cv, short_cv, technology]
    priority: 2
    date_range: "2023--Present"
```

### 3. Rebuild Sections

```bash
./utils/build_all_sections.sh
```

## Available Sections

The system automatically generates these section variants:

### Education

- `education_full.tex` - All education entries
- `education_short.tex` - Top 3 entries for short CVs
- `education_academic.tex` - Academic-focused entries

### Experience

- `experience_full.tex` - All professional experience
- `experience_short.tex` - Top 3 for short CVs
- `experience_academic.tex` - Academic/research roles
- `experience_tech.tex` - Technology-focused roles
- `experience_current.tex` - Currently active positions

### Projects

- `projects_full.tex` - All projects
- `projects_short.tex` - Top 4 for short CVs
- `projects_academic.tex` - Academic/research projects
- `projects_tech.tex` - Technical projects (R packages, Rust, APIs)
- `projects_current.tex` - Currently active projects

### Skills & Teaching

- `skills_full.tex` / `skills_short.tex`
- `teaching_full.tex` / `teaching_short.tex`

## Document Templates

### Short CV (`short_cv/short_cv.tex`)

Uses `*_short.tex` sections for a concise 2-3 page document.

### Long CV (`long_cv/long_cv.tex`)

Uses `*_full.tex` sections for a comprehensive academic CV.

### Resume (`resume/resume.tex`)

Can use specialized sections like `*_tech.tex` for industry positions.

## Advanced Usage

### Custom Section Building

```bash
# Exclude maintenance projects
python3 utils/build_section.py projects --tags full_cv --exclude-tags maintenance

# Only current and high-priority items
python3 utils/build_section.py experience --tags current --max-items 2

# Academic items excluding medical background
python3 utils/build_section.py experience --tags academic --exclude-tags medical
```

### Multiple Tag Filtering

Tags work with OR logic within include/exclude:

```bash
# Include items tagged with ANY of: academic, research, current
--tags academic research current

# Exclude items tagged with ANY of: medical, outdated
--exclude-tags medical outdated
```

## Available Mise Tasks

The system integrates with [mise](https://mise.jdx.dev/) for streamlined task management:

### Core Tasks

- `build-all` - Build everything: sections, bibs, and PDFs
- `build-sections` - Build all modular CV sections
- `build-pdfs` - Build all PDF documents
- `quick-build` - Quick build: sections + PDFs (skip bibs)
- `status` - Show modular CV system status
- `clean` - Remove all LaTeX build artifacts

### Document-Specific Tasks

- `build-short-cv` - Generate the short condensed CV
- `build-long-cv` - Generate the long detailed CV
- `build-resume` - Generate the small two page standard resume
- `build-czi` - Generate the CZI-specific document
- `gen-bibs` - Generate subset .bib files from tagged keywords

### Specialized Workflows

- `academic-cv` - Build academic-focused CV sections and documents
- `tech-resume` - Build tech-focused resume sections
- `format-latex` - Format .tex files using latexindent

### Usage Examples

```bash
# List all available tasks
mise tasks ls

# Run a specific task
mise run build-short-cv

# Run multiple tasks in sequence
mise run build-sections build-pdfs

# Check system status
mise run status
```

## Benefits

✅ **Atomic Units**: Each position/project/degree is a separate file
✅ **Flexible Assembly**: Mix and match using tags and priorities
✅ **Easy Maintenance**: Update once, propagates everywhere
✅ **Scalable**: Add new content without touching existing files
✅ **Automated**: Build process handles section assembly
✅ **Backward Compatible**: Maintains existing publication system

## Migration from Old System

The old `shared/` directory files are preserved but no longer used in the main documents. To migrate custom content:

1. Break apart content into individual unit files
2. Add metadata entries for each unit
3. Update document templates to use new section files
4. Test build process and verify output

## Troubleshooting

### Build Failures

- Check `build.log` files in document directories
- Verify all unit files exist and have valid LaTeX syntax
- Ensure metadata YAML syntax is correct

### Missing Content

- Verify unit files exist in `units/` subdirectories
- Check tag filtering in metadata
- Use `--verbose` flag with `build_section.py` for debugging

### LaTeX Errors

- Individual unit files must be valid LaTeX snippets
- Don't include `\section{}` headers in unit files (added automatically)
- Maintain consistent `\cventry{}` formatting
