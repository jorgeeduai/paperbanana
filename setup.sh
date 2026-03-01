#!/bin/bash
# PaperBanana — Dataset Setup Script
# Downloads PaperBananaBench from HuggingFace (~254MB)
# Run once before using PaperBanana for the first time.
#
# Usage: bash setup.sh [--force]
#   --force  Re-download even if dataset already exists

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data/PaperBananaBench"
ZIP_URL="https://huggingface.co/datasets/PaperBanana/PaperBananaBench/resolve/main/PaperBananaBench.zip"
ZIP_FILE="$SCRIPT_DIR/data/PaperBananaBench.zip"
FORCE=false

# Parse args
for arg in "$@"; do
  case $arg in
    --force) FORCE=true ;;
    --help|-h)
      echo "PaperBanana Dataset Setup"
      echo "Usage: bash setup.sh [--force]"
      echo "  --force  Re-download even if dataset exists"
      exit 0
      ;;
  esac
done

echo "🍌 PaperBanana — Dataset Setup"
echo "================================"

# Check if already exists
if [ -d "$DATA_DIR/diagram" ] && [ -d "$DATA_DIR/plot" ] && [ "$FORCE" != "true" ]; then
  DIAGRAM_COUNT=$(ls "$DATA_DIR/diagram/"*.jpg 2>/dev/null | wc -l)
  PLOT_COUNT=$(ls "$DATA_DIR/plot/"*.jpg 2>/dev/null | wc -l)
  echo "✅ Dataset already exists!"
  echo "   📊 Diagrams: $DIAGRAM_COUNT images"
  echo "   📈 Plots: $PLOT_COUNT images"
  echo "   Use --force to re-download."
  exit 0
fi

# Create data directory
mkdir -p "$SCRIPT_DIR/data"

echo "📥 Downloading PaperBananaBench (~254MB)..."
echo "   Source: HuggingFace (PaperBanana/PaperBananaBench)"

# Download with progress (try curl first, then wget)
if command -v curl &>/dev/null; then
  curl -L --progress-bar -o "$ZIP_FILE" "$ZIP_URL"
elif command -v wget &>/dev/null; then
  wget --show-progress -O "$ZIP_FILE" "$ZIP_URL"
else
  echo "❌ Error: Neither curl nor wget found. Install one and retry."
  exit 1
fi

# Verify download
if [ ! -f "$ZIP_FILE" ]; then
  echo "❌ Error: Download failed. File not found."
  exit 1
fi

ZIP_SIZE=$(stat -f%z "$ZIP_FILE" 2>/dev/null || stat -c%s "$ZIP_FILE" 2>/dev/null)
if [ "$ZIP_SIZE" -lt 100000000 ]; then
  echo "❌ Error: Downloaded file too small ($ZIP_SIZE bytes). Expected ~254MB."
  echo "   The download may have failed. Try again or check your connection."
  rm -f "$ZIP_FILE"
  exit 1
fi

echo "📦 Extracting dataset..."
cd "$SCRIPT_DIR/data"
unzip -o -q "$ZIP_FILE"

# Verify extraction
if [ -d "$DATA_DIR/diagram" ] && [ -d "$DATA_DIR/plot" ]; then
  DIAGRAM_COUNT=$(ls "$DATA_DIR/diagram/"*.jpg 2>/dev/null | wc -l)
  PLOT_COUNT=$(ls "$DATA_DIR/plot/"*.jpg 2>/dev/null | wc -l)
  echo ""
  echo "✅ Dataset ready!"
  echo "   📊 Diagrams: $DIAGRAM_COUNT images"
  echo "   📈 Plots: $PLOT_COUNT images"
  echo "   📁 Location: $DATA_DIR"
  
  # Clean up zip
  rm -f "$ZIP_FILE"
  echo "   🗑️ Zip file removed to save space."
else
  echo "❌ Error: Extraction failed. Expected diagram/ and plot/ directories."
  exit 1
fi

echo ""
echo "🍌 Setup complete! You can now run PaperBanana."
echo "   Example: python run_es.py --caption 'Tu descripción de figura'"
