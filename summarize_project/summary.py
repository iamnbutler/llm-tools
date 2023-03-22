import os
import glob

# Define the file types you want to search for (e.g., '*.txt', '*.py', etc.)
file_types = ['*.*']

# Define the forbidden filenames and folders
forbidden_files = ['project.txt', 's.py', 'package-lock.json', 'LICENSE']
forbidden_folders = ['.git', 'node_modules', '.vscode', 'gpt', '.next', '.contentlayer']

# Define the output filename
output_filename = 'project.txt'

def generate_file_tree(start_path):
    tree = ""
    for root, dirs, files in os.walk(start_path):
        # Skip the node_modules directory and its contents
        for dir_name in ["node_modules", ".git", "gpt"]:
            if dir_name in dirs:
                dirs.remove(dir_name)

        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree += f'{indent}{os.path.basename(root)}/\n'
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            tree += f'{sub_indent}{f}\n'
    return tree

def main():
    # Check if output.txt exists and delete it if it does
    if os.path.exists(output_filename):
        os.remove(output_filename)

    # Find all specified files in the current folder
    files_to_process = []
    for file_type in file_types:
        files_to_process.extend(glob.glob(f'**/{file_type}', recursive=True))

    # Filter out forbidden files and folders
    files_to_process = [f for f in files_to_process if os.path.basename(f) not in forbidden_files and not any(folder in os.path.dirname(f) for folder in forbidden_folders)]

    # Write the contents of the found files to the output file
    with open(output_filename, 'w') as output_file:
        # Add the introductory message
        output_file.write("Hi ChatGPT, I'm providing you this file so you have more context for our current conversation. You are an experienced software engineer discussing a problem or having a conversation with your peers.\n\n For results longer than 490 words or more than 3900 characters, you will add a page number to each result and stop at theend of a whole line when you get close to hitting that count. For example, if your response is at 487 words and at the end of a line and you need to add another 300 words to your response, add === End of page 1 === to the end of that reply so the conversation can be resumed from page 2.\n\n")

        # Generate and add the file tree to the output file
        output_file.write("File tree:\n")
        output_file.write(generate_file_tree(os.path.abspath('.')))
        output_file.write("\n")

        for file_path in files_to_process:
            # Separator line
            output_file.write('-' * 80 + '\n')

            # File statistics
            num_lines = sum(1 for _ in open(file_path))
            num_bytes = os.path.getsize(file_path)

            # Write a comment with the filename, path, total lines, and bytes
            output_file.write(f'# File: {os.path.abspath(file_path)} | Lines: {num_lines} | Bytes: {num_bytes}\n')

            # Write the contents of the file to the output file
            with open(file_path, 'r') as input_file:
                for line in input_file:
                    output_file.write(line)

            # Add a newline to separate the contents of different files
            output_file.write('\n')

if __name__ == '__main__':
    main()
