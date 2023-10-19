import os
import mmap
from tqdm import tqdm


def count_files(directory):
    """Counts the number of files in a directory."""
    return sum([len(files) for _, _, files in os.walk(directory)])

def search_files_mmap(directory, sequence):
    file_count = sum([len(files) for _, _, files in os.walk(directory)])

    with tqdm(total=file_count, desc="Processing Files", ncols=100) as pbar:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)

                # Extract the hash (as the first part of the filename) and convert it to int
                hash_value_str = filename.split('_')[0]
                try:
                    hash_value = int(hash_value_str)
                except ValueError:
                    print(f"Invalid hash value '{hash_value_str}' in filename {filename}. Skipping.")
                    continue

                # Skip files with hash == 0
                # if hash_value == 0:
                #     pbar.update(1)
                #     continue

                try:
                    with open(filepath, 'rb') as file:
                        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                            offset = mmapped_file.find(sequence)
                            while offset != -1:
                                print(f"Found in {filepath} (hash dec: {hash_value}, hex: {hash_value:02x}) at offset (dec): {offset}, (hex): {offset:02x}")
                                offset = mmapped_file.find(sequence, offset + 1)
                except Exception as e:
                    print(f"Error processing {filepath}. Reason: {str(e)}")

                pbar.update(1)

def search_files(directory, sequence):
    file_count = sum([len(files) for _, _, files in os.walk(directory)])

    with tqdm(total=file_count, desc="Processing Files", ncols=100) as pbar:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)

                # Extract the hash (as the first part of the filename) and convert it to int
                hash_value_str = filename.split('_')[0]
                try:
                    hash_value = int(hash_value_str)
                except ValueError:
                    print(f"Invalid hash value '{hash_value_str}' in filename {filename}. Skipping.")
                    continue

                # # Skip files with hash == 0
                # if hash_value == 0:
                #     pbar.update(1)
                #     continue

                try:
                    with open(filepath, 'rb') as file:
                        content = file.read()
                        offset = content.find(sequence)
                        while offset != -1:
                            print(
                                f"Found in {filepath} (hash dec: {hash_value}, hex: {hash_value:02x}) at offset (dec): {offset}, (hex): {offset:02x}")
                            offset = content.find(sequence, offset + 1)
                except Exception as e:
                    print(f"Error processing {filepath}. Reason: {str(e)}")

                pbar.update(1)


if __name__ == '__main__':
    directory_path = "C:\\Users\\Jonathan Greve\\Downloads\\all_gw_files"
    # byte_sequence = b"\x55\xa4\x04\x01"
    # byte_sequence = b"\xba\x40\x04\x01\x00\x00"
    # byte_sequence = b"\x56\x9f\x04\x00"
    byte_sequence = b"\xc4\x32\x05\x01\x00\x00"
    search_files(directory_path, byte_sequence)
