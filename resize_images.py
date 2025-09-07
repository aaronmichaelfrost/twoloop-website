#!/usr/bin/env python3
"""
Script to resize all PNG images in docs/item-sprites to 100x100px
and save them to docs/item-sprites-small
"""

import os
import sys
from PIL import Image
import shutil

def resize_images():
    source_dir = "docs/item-sprites"
    target_dir = "docs/item-sprites-small"
    
    # Create target directory if it doesn't exist
    if os.path.exists(target_dir):
        print(f"Removing existing {target_dir} directory...")
        shutil.rmtree(target_dir)
    
    print(f"Creating {target_dir} directory...")
    os.makedirs(target_dir, exist_ok=True)
    
    # Counter for processed images
    count = 0
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.png'):
                # Get the source file path
                source_path = os.path.join(root, file)
                
                # Create the relative path from source_dir
                rel_path = os.path.relpath(source_path, source_dir)
                
                # Create the target path
                target_path = os.path.join(target_dir, rel_path)
                
                # Create target subdirectory if needed
                target_subdir = os.path.dirname(target_path)
                os.makedirs(target_subdir, exist_ok=True)
                
                try:
                    # Open and resize the image
                    with Image.open(source_path) as img:
                        # Convert to RGBA if not already (to handle transparency)
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')
                        
                        # Resize to 100x100 with high quality resampling
                        resized_img = img.resize((100, 100), Image.Resampling.LANCZOS)
                        
                        # Save the resized image
                        resized_img.save(target_path, 'PNG', optimize=True)
                        
                        count += 1
                        print(f"Resized {count}: {rel_path}")
                        
                except Exception as e:
                    print(f"Error processing {source_path}: {e}")
    
    print(f"\nCompleted! Resized {count} images to 100x100px in {target_dir}")

if __name__ == "__main__":
    try:
        resize_images()
    except ImportError:
        print("Error: PIL (Pillow) is required. Install it with: pip install Pillow")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
