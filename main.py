#!/usr/bin/env python3

import os
import re
import json
import shutil
import argparse
from collections import defaultdict


# Load character substitution tables
with open("emoticons_table.json", "r", encoding="utf-8") as f:
    EMOTICONS_TABLE = json.load(f)
with open("chars_table.json", "r", encoding="utf-8") as f:
    CHARS_TABLE = json.load(f)


DELIMITER = "###"  # Safer delimiter that's unlikely to appear in phrases


def extract_phrases(decipher_russian=False, translate_emoticons=False):
    """Extract phrases from original game files and create unpatched versions."""
    # Setup directories
    if os.path.exists("not_patched"):
        shutil.rmtree("not_patched")
    os.makedirs("not_patched")

    # Regex patterns (preserved as per request)
    SPECIAL_PATTERN = re.compile(r"\[\[(?:\{.*?\})?(?P<PHRASE>.*?)(?:\{.*?\})?\|(?:.*?)\]\]\s*#line")
    BASIC_PATTERN = re.compile(r"\s*(?:(?P<NAME>\w*?)(?:\:))?(?:->)?\s*(?:\{.*?\})*(?:\[.*?\])*\s*(?P<PHRASE>.*?)(?:\{.*?\})?(?:\[\/.*?\])?\s*#line")

    phrases = []
    addresses = []

    for filename in os.listdir("original"):
        src_path = os.path.join("original", filename)
        dst_path = os.path.join("not_patched", filename)

        with open(src_path, "r", encoding="utf-8") as src_file, \
             open(dst_path, "w", encoding="utf-8") as dst_file:

            for line_num, line in enumerate(src_file, start=1):
                line = line.rstrip()
                
                # Apply emoticon substitutions if requested
                if translate_emoticons:
                    for emoticon, replacement in EMOTICONS_TABLE.items():
                        line = re.sub(re.escape(emoticon), replacement, line)

                # Find phrase matches
                match = SPECIAL_PATTERN.search(line) or BASIC_PATTERN.search(line)
                if not match:
                    dst_file.write(f"{line}\n")
                    continue
                
                # Extract phrase details
                name = match.groupdict().get("NAME", "Not Stated")
                start, end = match.span("PHRASE")
                phrase = line[start:end]

                # Apply Russian character substitution if needed
                if decipher_russian:
                    new_line = line[:start] + re.sub('|'.join(CHARS_TABLE.keys()), 
                                    lambda m: CHARS_TABLE[m.group()], phrase) + line[end:]
                    line = new_line
                    phrase = line[start:end]  # Get possibly modified phrase

                # Store extracted information
                phrases.append(f"{name}{DELIMITER}{phrase}")
                addresses.append(f"{filename}:{line_num}:{start}:{end}")
                dst_file.write(f"{line}\n")

    return phrases, addresses


def generate_translation_files(phrases, addresses):
    """Create files for translation and address mapping."""
    # Write collected phrases
    with open("original.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(phrases))
    
    # Handle existing translation file
    if os.path.exists("translated.txt"):
        response = input("translated.txt exists! Overwrite? [y/n]: ").strip().lower()
        if response == 'y':
            shutil.copy("original.txt", "translated.txt")
    else:
        shutil.copy("original.txt", "translated.txt")

    # Write address mapping
    with open("addresses.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(addresses))

def apply_patches():
    """Apply translated phrases to create patched game files."""
    # Read translation data
    with open("translated.txt", "r", encoding="utf-8") as trans_file, \
         open("addresses.txt", "r", encoding="utf-8") as addr_file:
        
        translations = [line.split(DELIMITER, 1)[-1].strip() for line in trans_file]
        addresses = [line.strip() for line in addr_file]

    # Validate input
    if len(translations) != len(addresses):
        raise ValueError("Mismatch between translations and addresses count")

    # Organize addresses by filename
    file_map = defaultdict(list)
    for idx, addr in enumerate(addresses):
        filename, line, start, end = addr.split(':', 3)
        file_map[filename].append((idx, int(line), int(start), int(end)))

    # Process files
    if os.path.exists("patched"):
        shutil.rmtree("patched")
    os.makedirs("patched")

    for filename in file_map:
        src_path = os.path.join("not_patched", filename)
        dst_path = os.path.join("patched", filename)

        with open(src_path, "r", encoding="utf-8") as src_file, \
             open(dst_path, "w", encoding="utf-8") as dst_file:

            lines = src_file.read().splitlines()
            for idx, line_num, start, end in file_map[filename]:
                if line_num-1 >= len(lines):
                    continue  # Skip invalid line numbers
                
                # Apply translation
                original = lines[line_num-1]
                lines[line_num-1] = original[:start] + translations[idx] + original[end:]

            dst_file.write("\n".join(lines))


def main():
    """Main CLI handler."""
    parser = argparse.ArgumentParser(description="Night in the Woods Translation Patcher")
    parser.add_argument("-p", "--patch", action="store_true", help="Apply existing translations")
    parser.add_argument("-r", "--rus", action="store_true", help="Decipher Russian characters")
    parser.add_argument("-e", "--emoticons", action="store_true", help="Translate emoticons")
    args = parser.parse_args()

    if args.patch:
        apply_patches()
        print("Patching complete!")
    else:
        phrases, addresses = extract_phrases(args.rus, args.emoticons)
        generate_translation_files(phrases, addresses)
        print("Translation files generated!")

if __name__ == "__main__":
    main()
