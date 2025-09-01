#!/bin/bash
# Master build script for the modular CV system

set -e # Exit on any error

echo "🔧 Starting modular CV build process..."

# Function to run steps with proper error handling
run_step() {
    local step_name="$1"
    local command="$2"
    echo "📋 $step_name..."
    if eval "$command"; then
        echo "✅ $step_name completed successfully"
    else
        echo "❌ $step_name failed"
        exit 1
    fi
}

# Function to build LaTeX document
build_latex() {
    local dir="$1"
    local filename="$2"
    echo "📄 Building LaTeX document: $dir/$filename..."

    cd "$dir"

    # Run pdflatex multiple times to resolve references
    pdflatex -interaction=nonstopmode "$filename.tex" >build.log 2>&1 || {
        echo "❌ LaTeX compilation failed. Check $dir/build.log for details"
        return 1
    }

    # Run bibtex for all bibliography types if .aux files exist
    for aux_file in *.aux; do
        if [ -f "$aux_file" ] && grep -q "\\bibdata" "$aux_file" 2>/dev/null; then
            echo "   📚 Running bibtex for $aux_file..."
            bibtex "$aux_file" >>build.log 2>&1 || true
        fi
    done

    # Run pdflatex again to incorporate bibliography
    pdflatex -interaction=nonstopmode "$filename.tex" >>build.log 2>&1 || {
        echo "❌ Second LaTeX pass failed. Check $dir/build.log for details"
        return 1
    }

    # Final pass to ensure all references are correct
    pdflatex -interaction=nonstopmode "$filename.tex" >>build.log 2>&1 || {
        echo "❌ Final LaTeX pass failed. Check $dir/build.log for details"
        return 1
    }

    cd ..
    echo "✅ LaTeX document $dir/$filename.pdf built successfully"
}

# Check if we should only run specific steps
STEP="${1:-all}"

case "$STEP" in
"sections")
    run_step "Building modular sections" "./utils/build_all_sections.sh"
    ;;
"bibs")
    if [ -f "main.py" ]; then
        run_step "Generating bibliography files" "python3 main.py"
    else
        echo "⚠️  No main.py found, skipping bibliography generation"
    fi
    ;;
"pdfs")
    echo "📄 Building PDF documents..."

    # Build short CV
    if [ -d "short_cv" ]; then
        build_latex "short_cv" "short_cv"
    fi

    # Build long CV
    if [ -d "long_cv" ]; then
        build_latex "long_cv" "long_cv"
    fi

    # Build resume
    if [ -d "resume" ]; then
        build_latex "resume" "resume"
    fi

    # Build utra
    if [ -d "utra" ]; then
        build_latex "utra" "utra"
    fi

    # Build czi
    if [ -d "czi" ]; then
        build_latex "czi" "czi"
        build_latex "czi" "cover_letter"
    fi
    ;;
"all")
    run_step "Building modular sections" "./utils/build_all_sections.sh"

    if [ -f "main.py" ]; then
        run_step "Generating bibliography files" "python3 main.py"
    else
        echo "⚠️  No main.py found, skipping bibliography generation"
    fi

    echo "📄 Building PDF documents..."

    # Build short CV
    if [ -d "short_cv" ]; then
        build_latex "short_cv" "short_cv"
    fi

    # Build long CV
    if [ -d "long_cv" ]; then
        build_latex "long_cv" "long_cv"
    fi

    # Build resume
    if [ -d "resume" ]; then
        build_latex "resume" "resume"
    fi

    # Build utra
    if [ -d "utra" ]; then
        build_latex "utra" "utra"
    fi

    # Build czi
    if [ -d "czi" ]; then
        build_latex "czi" "czi"
    fi
    ;;
"clean")
    echo "🧹 Cleaning build artifacts..."
    find . -name "*.aux" -o -name "*.bbl" -o -name "*.blg" -o -name "*.log" \
        -o -name "*.out" -o -name "*.fls" -o -name "*.fdb_latexmk" \
        -o -name "*.synctex.gz" -o -name "build.log" | xargs rm -f
    echo "✅ Cleanup completed"
    exit 0
    ;;
"help")
    echo "Usage: $0 [step]"
    echo ""
    echo "Steps:"
    echo "  all      - Build everything (default)"
    echo "  sections - Build only modular sections"
    echo "  bibs     - Generate only bibliography files"
    echo "  pdfs     - Build only PDF documents"
    echo "  clean    - Clean build artifacts"
    echo "  help     - Show this help"
    exit 0
    ;;
*)
    echo "❌ Unknown step: $STEP"
    echo "Run '$0 help' for available options"
    exit 1
    ;;
esac

echo ""
echo "🎉 Build process completed successfully!"
echo ""
echo "📊 Generated files:"
echo "   Sections: $(ls -1 sections/*.tex 2>/dev/null | wc -l | tr -d ' ') files"
echo "   PDFs: $(find . -name "*.pdf" -not -path "./.*" | wc -l | tr -d ' ') files"
echo ""

# Show generated PDFs with sizes
if find . -name "*.pdf" -not -path "./.*" -print0 | xargs -0 ls -lh >/dev/null 2>&1; then
    echo "📄 PDF documents:"
    find . -name "*.pdf" -not -path "./.*" -exec ls -lh {} \; | awk '{print "   " $9 " (" $5 ")"}'
fi
