#!/usr/bin/env python3
import re
import os

def split_chapters(input_file):
    """Split the Harry Potter text file into individual chapter files."""
    
    # Read the entire file
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find all chapter markers
    chapter_pattern = r'CHAPTER [A-Z]+'
    chapters = re.split(chapter_pattern, content)
    chapter_titles = re.findall(chapter_pattern, content)
    
    # Remove the first split (content before first chapter)
    if chapters and not chapters[0].strip():
        chapters = chapters[1:]
    
    # Create chapter files
    for i, (chapter_content, chapter_title) in enumerate(zip(chapters, chapter_titles), 1):
        filename = f"chapter-{i:02d}.txt"
        
        # Clean up the chapter content
        chapter_content = chapter_content.strip()
        
        # Write the chapter file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"{chapter_title}\n\n")
            f.write(chapter_content)
        
        print(f"Created {filename} ({chapter_title})")

if __name__ == "__main__":
    split_chapters("harry_potter_sorcerers_stone.txt") 