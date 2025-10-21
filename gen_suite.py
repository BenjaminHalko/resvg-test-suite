#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
import sys
from typing import List

try:
    import cairosvg
except ImportError:
    print("cairosvg is not installed. Please install it with 'pip install cairosvg'", file=sys.stderr)
    sys.exit(1)


def process_file(input_file: Path) -> bool:
    """
    Renders an SVG file to a PNG using cairosvg.
    
    Args:
        input_file: Path to input file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Define the final output file path
        output_file = input_file.with_suffix('.png')
        if output_file.exists():
            output_file.unlink()

        # Render the SVG to a PNG, fitting it into a 200x200 box
        cairosvg.svg2png(
            url=str(input_file),
            write_to=str(output_file),
            output_width=200,
            output_height=200
        )

        print(f"✓ Processed: {input_file}")
        return True
        
    except Exception as e:
        print(f"Exception processing {input_file}: {e}", file=sys.stderr)
        return False


def find_files(input_dir: Path) -> List[Path]:
    files = input_dir.rglob('*svg')
    return sorted(files)

def main():
    parser = argparse.ArgumentParser(
        description='Process files through Inkscape while maintaining directory structure'
    )
    parser.add_argument(
        'input',
        type=Path,
        help='Input directory containing files to process'
    )
    args = parser.parse_args()
    
    # Validate input directory
    if not args.input.exists():
        print(f"Error: Input directory does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    if not args.input.is_dir():
        print(f"Error: Input path is not a directory: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Find all files to process
    files_to_process = find_files(args.input)
    
    if not files_to_process:
        print(f"No files found in {args.input}")
        sys.exit(0)
    
    print(f"Found {len(files_to_process)} file(s) to process")
    
    # Process each file
    successful = 0
    failed = 0
    
    for input_file in files_to_process:
        if process_file(input_file):
            successful += 1
        else:
            failed += 1
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Processing complete:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(files_to_process)}")
    print(f"{'='*50}")
    
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
