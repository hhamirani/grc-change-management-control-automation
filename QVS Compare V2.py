import os
from datetime import datetime
import hashlib
import sys
from contextlib import contextmanager # Import contextmanager

# --- Custom Tee Context Manager ---
@contextmanager
def tee_output(filename, encoding='utf-8'):
    """
    Context manager to tee stdout to both console and a file.
    """
    original_stdout = sys.stdout
    log_file = None
    try:
        log_file = open(filename, 'w', encoding=encoding)
        sys.stdout = Tee(original_stdout, log_file)
        yield # Code inside the 'with' block will execute here
    finally:
        sys.stdout = original_stdout # Restore original stdout
        if log_file:
            log_file.close() # Close the file

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()

# --- Utility Functions ---
def get_file_metadata(file_path):
    """
    Retrieves relevant metadata for a given file path, including its MD5 hash.
    Returns a dictionary with 'created_date', 'modified_date', 'size_bytes',
    'md5_hash', or None if an error occurs.
    """
    try:
        stat_info = os.stat(file_path)
        created_timestamp = stat_info.st_ctime
        modified_timestamp = stat_info.st_mtime
        size_bytes = stat_info.st_size
        md5_hash = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''): # More Pythonic way to read in chunks
                md5_hash.update(chunk)
        return {
            'created_date': datetime.fromtimestamp(created_timestamp),
            'modified_date': datetime.fromtimestamp(modified_timestamp),
            'size_bytes': size_bytes,
            'md5_hash': md5_hash.hexdigest()
        }
    except FileNotFoundError:
        print(f"Warning: File '{file_path}' not found for metadata retrieval.")
        return None
    except OSError as e:
        print(f"Warning: Could not get metadata for '{file_path}': {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while getting metadata for '{file_path}': {e}")
        return None

def compare_files(file1_path, file2_path):
    """
    Compres the contents of two text files line by line and returns a list
    of differences. Handles file existence checks internally.
    """
    if not os.path.exists(file1_path):
        print(f"Error: File '{file1_path}' not found for comparison.")
        return None
    if not os.path.exists(file2_path):
        print(f"Error: File '{file2_path}' not found for comparison.")
        return None

    differences = []
    with open(file1_path, 'r', encoding='utf-8') as f1, \
         open(file2_path, 'r', encoding='utf-8') as f2:
        for i, (line1, line2) in enumerate(zip(f1, f2)): # Iterate lines with zip
            if line1 != line2:
                differences.append({
                    'line_num': i + 1,
                    'file1_content': line1,
                    'file2_content': line2
                })
        # Handle files with different numbers of lines
        remaining_lines_f1 = f1.readlines()
        for i, line1 in enumerate(remaining_lines_f1):
            differences.append({
                'line_num': len(f2.readlines()) + i + 1, # This part needs adjustment if f2 is shorter
                'file1_content': line1,
                'file2_content': ""
            })

        remaining_lines_f2 = f2.readlines()
        for i, line2 in enumerate(remaining_lines_f2):
            differences.append({
                'line_num': len(f1.readlines()) + i + 1, # This part needs adjustment if f1 is shorter
                'file1_content': "",
                'file2_content': line2
            })
    return differences
# --- Corrected and Simplified compare_files ---
def compare_files(file1_path, file2_path):
    """
    Compares the contents of two text files line by line and returns a list
    of differences. Handles file existence checks internally.
    """
    if not os.path.exists(file1_path):
        print(f"Error: File '{file1_path}' not found for comparison.")
        return None
    if not os.path.exists(file2_path):
        print(f"Error: File '{file2_path}' not found for comparison.")
        return None

    differences = []
    with open(file1_path, 'r', encoding='utf-8') as f1, \
         open(file2_path, 'r', encoding='utf-8') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    max_len = max(len(lines1), len(lines2))

    for i in range(max_len):
        line_num = i + 1
        line1_content = lines1[i] if i < len(lines1) else ""
        line2_content = lines2[i] if i < len(lines2) else ""

        if line1_content != line2_content:
            differences.append({
                'line_num': line_num,
                'file1_content': line1_content.strip(), # strip here for consistency
                'file2_content': line2_content.strip()  # strip here for consistency
            })
    return differences


# --- Main Script Execution ---
if __name__ == "__main__": # Good practice to wrap main logic
    file1_name = 'baseline.qvs.txt'
    file2_name = 'new.qvs.txt'

    # Generate timestamp for filename
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d_%I-%M-%S%p")
    output_filename = f'QVS_Compare_{timestamp_str}.txt'

    # Use the tee_output context manager
    with tee_output(output_filename) as _: # The 'as _' means we don't need the yielded value
        print(f"Comparing contents of '{file1_name}' and '{file2_name}'...\n")

        diffs = compare_files(file1_name, file2_name)

        if diffs is None:
            # Error message already printed by compare_files
            pass
        elif diffs:
            print(f"--- Content Differences Found ({len(diffs)} total) ---")
            for diff in diffs:
                print(f"Line {diff['line_num']}:")
                # Using the stripped content from the dictionary
                print(f"  File1: {diff['file1_content']}")
                print(f"  File2: {diff['file2_content']}")
            print("\n" + "="*50 + "\n")
        else:
            print(f"No content differences found between {file1_name} and {file2_name}.\n")
            print("="*50 + "\n")

        print("--- File Metadata for SOX Compliance ---")

        metadata_file1 = get_file_metadata(file1_name)
        if metadata_file1:
            print(f"\nMetadata for '{file1_name}':")
            print(f"  Created Date:    {metadata_file1['created_date']}")
            print(f"  File Size:       {metadata_file1['size_bytes']} bytes")
            print(f"  MD5 Hash:        {metadata_file1['md5_hash']}")
        else:
            print(f"\nCould not retrieve metadata for '{file1_name}'.")

        metadata_file2 = get_file_metadata(file2_name)
        if metadata_file2:
            print(f"\nMetadata for '{file2_name}':")
            print(f"  Created Date:    {metadata_file2['created_date']}")
            print(f"  File Size:       {metadata_file2['size_bytes']} bytes")
            print(f"  MD5 Hash:        {metadata_file2['md5_hash']}")
        else:
            print(f"\nCould not retrieve metadata for '{file2_name}'.")

        print("\n" + "="*50 + "\n")

        print("SOX Compliance Note:")
        print("- 'Modified Date' and 'Created Date' are critical for audit trails and verifying when and how changes occurred.")
        print("- 'File Size' changes also indicate content modification.")
        print("- **MD5 Hash** provides a cryptographic fingerprint. If the MD5 hashes of two versions of a file differ, their content is not identical, serving as definitive proof of modification.")

    print(f"✅ Output successfully captured in '{output_filename}'")
