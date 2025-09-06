#!/usr/bin/env python3
"""
Script to transfer content from 01module_old HTML files to 01module files
while preserving the new template structure.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def extract_old_content(old_file_path):
    """Extract the main content from the old HTML file."""
    with open(old_file_path, 'r', encoding='utf-8') as f:
        old_html = f.read()
    
    soup = BeautifulSoup(old_html, 'html.parser')
    
    # Extract title
    title = soup.find('title')
    title_text = title.text if title else "Untitled"
    
    # Extract main content
    main = soup.find('main')
    if not main:
        # If no main tag, try to get body content
        body = soup.find('body')
        if body:
            # Remove header and footer if present
            header = body.find('header')
            footer = body.find('footer')
            if header:
                header.decompose()
            if footer:
                footer.decompose()
            main = body
    
    return {
        'title': title_text,
        'content': str(main) if main else "",
        'has_mermaid': 'mermaid' in old_html.lower()
    }

def update_new_file(new_file_path, old_content):
    """Update the new file with content from the old file."""
    with open(new_file_path, 'r', encoding='utf-8') as f:
        new_html = f.read()
    
    soup = BeautifulSoup(new_html, 'html.parser')
    
    # Update title
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = old_content['title']
    
    # Update meta description
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc:
        # Extract a description from the title
        desc_text = old_content['title'].replace(' - ', '. ').replace(':', '.')
        meta_desc['content'] = desc_text
    
    # Find lesson body div
    lesson_body = soup.find('div', class_='lesson-body')
    
    if lesson_body and old_content['content']:
        # Parse the old content
        old_soup = BeautifulSoup(old_content['content'], 'html.parser')
        
        # Clear existing placeholder content
        lesson_body.clear()
        
        # Process sections from old content
        if old_soup.find('main'):
            main_content = old_soup.find('main')
            sections = main_content.find_all('section')
            
            for section in sections:
                # Fix class names (underscore to hyphen)
                if section.get('class'):
                    new_classes = []
                    for cls in section.get('class'):
                        new_classes.append(cls.replace('_', '-'))
                    section['class'] = new_classes
                
                # Fix all nested class names
                for elem in section.find_all(class_=True):
                    if elem.get('class'):
                        new_classes = []
                        for cls in elem.get('class'):
                            new_classes.append(cls.replace('_', '-'))
                        elem['class'] = new_classes
                
                lesson_body.append(section)
        else:
            # If no main tag, just append all content
            for child in old_soup.children:
                if child.name:  # Skip text nodes
                    lesson_body.append(child)
    
    # Add mermaid script if needed
    if old_content['has_mermaid']:
        head = soup.find('head')
        if head and not soup.find('script', string=re.compile('mermaid')):
            mermaid_script = soup.new_tag('script', type='module')
            mermaid_script.string = """
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true
            }
        });"""
            head.append(mermaid_script)
    
    # Update the lesson header h1
    lesson_h1 = soup.find('header', class_='lesson-header')
    if lesson_h1:
        h1 = lesson_h1.find('h1')
        if h1:
            # Extract main title from full title
            title_parts = old_content['title'].split(' - ')
            if len(title_parts) > 1:
                h1.string = title_parts[-1]
            else:
                title_parts = old_content['title'].split(': ')
                if len(title_parts) > 1:
                    h1.string = ': '.join(title_parts[1:])
                else:
                    h1.string = old_content['title']
    
    return str(soup.prettify())

def process_all_files():
    """Process all HTML files from 01module_old to 01module."""
    old_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module_old")
    new_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module")
    
    # Get list of HTML files
    html_files = list(old_dir.glob("*.html"))
    
    print(f"Found {len(html_files)} HTML files to process")
    
    successful = 0
    failed = 0
    
    for old_file in html_files:
        filename = old_file.name
        new_file = new_dir / filename
        
        # Skip if new file doesn't exist
        if not new_file.exists():
            print(f"  ⚠️  Skipping {filename} - new file doesn't exist")
            continue
        
        try:
            print(f"  Processing {filename}...")
            
            # Extract content from old file
            old_content = extract_old_content(old_file)
            
            # Update new file with old content
            updated_html = update_new_file(new_file, old_content)
            
            # Write updated content
            with open(new_file, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            
            print(f"  ✓  Successfully updated {filename}")
            successful += 1
            
        except Exception as e:
            print(f"  ✗  Failed to process {filename}: {str(e)}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {successful + failed}")

if __name__ == "__main__":
    print("Starting content transfer from 01module_old to 01module...")
    print("="*50)
    process_all_files()
