#!/usr/bin/env python3
"""
Simple script to resize all PNG files in docs/item-sprites to 100x100px
and save them in docs/item-sprites-small
"""

import os
import sys

try:
    from PIL import Image
    print("Pillow is available")
except ImportError:
    print("Pillow not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image

def resize_images():
    source_dir = "docs/item-sprites"
    target_dir = "docs/item-sprites-small"
    
    # Create target directory
    os.makedirs(target_dir, exist_ok=True)
    
    total_files = 0
    processed_files = 0
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.png'):
                total_files += 1
                
                source_path = os.path.join(root, file)
                
                # Create the same subdirectory structure in target
                rel_path = os.path.relpath(root, source_dir)
                if rel_path == '.':
                    target_subdir = target_dir
                else:
                    target_subdir = os.path.join(target_dir, rel_path)
                
                os.makedirs(target_subdir, exist_ok=True)
                target_path = os.path.join(target_subdir, file)
                
                try:
                    # Open and resize image
                    with Image.open(source_path) as img:
                        # Convert to RGBA if not already
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')
                        
                        # Resize to 100x100 with high quality resampling
                        resized = img.resize((100, 100), Image.Resampling.LANCZOS)
                        
                        # Save as PNG
                        resized.save(target_path, 'PNG', optimize=True)
                        
                        processed_files += 1
                        print(f"✓ {file}")
                        
                except Exception as e:
                    print(f"✗ Failed to process {file}: {e}")
    
    print(f"\nCompleted! Processed {processed_files}/{total_files} files")

if __name__ == "__main__":
    resize_images()
