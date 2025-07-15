#!/usr/bin/env python3
import re

def split_chapters(input_file):
    """Split the Harry Potter text file into individual chapter files."""
    
    # Read the entire file
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find all chapter positions
    chapter_matches = list(re.finditer(r'CHAPTER [A-Z]+', content))
    
    if not chapter_matches:
        print("No chapters found!")
        return
    
    # Create chapter files
    for i, match in enumerate(chapter_matches):
        chapter_title = match.group()
        start_pos = match.start()
        
        # Find the end position (start of next chapter or end of file)
        if i + 1 < len(chapter_matches):
            end_pos = chapter_matches[i + 1].start()
        else:
            end_pos = len(content)
        
        # Extract chapter content
        chapter_content = content[start_pos:end_pos].strip()
        
        # Create filename
        filename = f"chapter-{i+1:02d}.txt"
        
        # Write the chapter file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(chapter_content)
        
        print(f"Created {filename} ({chapter_title})")

if __name__ == "__main__":
    split_chapters("harry_potter_sorcerers_stone.txt") 