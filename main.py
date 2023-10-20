#!/usr/bin/env python3

import os
import re
import sys


def extract_matching_blocks(content, keyword):
    # Simplified pattern to match both resource and data blocks
    block_pattern = r'(?:^|\n)((data|resource|module|variable|provider)\s+"[^"]+"(\s+"[^"]+")?\s*\{.*?\n\})'
    extracted_blocks = []

    matches = re.findall(block_pattern, content, re.DOTALL | re.MULTILINE)
    for match in matches:
        # Extracting the full block, which is the first element of the tuple
        block = match[0]
        if str.upper(keyword) in str.upper(block):
            extracted_blocks.append(block)

    return extracted_blocks


def main():
    if len(sys.argv) != 3:
        print("Usage: ./extract_resources.py <keyword> <path_to_directory>")
        sys.exit(1)

    keyword = sys.argv[1]
    path = sys.argv[2]
    extracted_resources = []

    # Get all .tf files in the current directory
    tf_files = [f"{path}/{f}" for f in os.listdir(path) if f.endswith('.tf')]

    for tf_file in tf_files:
        with open(tf_file, 'r') as file:
            content = file.read()
            matching_blocks = extract_matching_blocks(content, keyword)
            extracted_resources.extend(matching_blocks)

            # Removing the matched blocks from original file
            for block in matching_blocks:
                content = content.replace(block, "")

        with open(tf_file, 'w') as file:
            file.write(content)

    # Write the extracted resources to a new .tf file
    with open(f"{keyword}.tf", "w") as output_file:
        output_file.write("\n\n".join(extracted_resources))


if __name__ == "__main__":
    main()
