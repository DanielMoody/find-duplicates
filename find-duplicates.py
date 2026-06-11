"""
Duplicate File Finder

A nondestructive utility that recursively scans a directory
for duplicate files.

Files are grouped by size before SHA-256 hashing to reduce
unnecessary processing. 0 byte files and links are skipped
"""

import os
import hashlib

#common macOS metadata files that aren't part of the intended script usage
IGNORE_FILES = {
    ".DS_Store",
    ".localized"
}
def calculate_file_hash(file_path):
    """Return the SHA-256 hash of a file."""

    hasher = hashlib.sha256()

    try:
        with open(file_path, "rb") as file: #read binary mode

            chunk = file.read(8192) #Read the file in chunks to avoid loading large files into memory.

            while chunk:
                hasher.update(chunk)
                chunk = file.read(8192)

        return hasher.hexdigest()

    except OSError as e:
        print(f"Could not read file {file_path}: {e}")
        return None


def precheck(directory):
    """Group files by size."""

    size_groups = {}
    stats = {
        "files_seen": 0,
        "files_skipped": 0,
    }
    for dirpath, _, filenames in os.walk(directory): 
        for filename in filenames:
            stats["files_seen"] += 1
            file_path = os.path.join(dirpath, filename)

            try:
                file_size = os.path.getsize(file_path)
                # Empty files are technically duplicates, but they are
                # not the target of  the tool and tend to
                # clutter the results.
                if file_size == 0:
                    stats["files_skipped"] += 1
                    continue
                # Links are skipped They are not additional copies
                # of file data and are not relevant to the intended cleanup task.
                if os.path.islink(file_path):
                    stats["files_skipped"] += 1
                    continue 
                if filename in IGNORE_FILES:
                    stats["files_skipped"] += 1
                    continue
                if file_size not in size_groups:
                    size_groups[file_size] = []
                size_groups[file_size].append(file_path)

            except OSError as e:
                print(f"Could not access {file_path}: {e}")

    return size_groups, stats


def get_candidate_files(size_groups):
    """Return files whose sizes match at least one other file."""
    # Files with unique sizes cannot be duplicates. Prechecking size saves time.

    candidates = []

    for files in size_groups.values():

        if len(files) > 1:
            candidates.extend(files)

    return candidates


def find_duplicates(directory):
    """Find duplicate files in the given directory."""
    # Store duplicates relative to the first file encountered.
    # For example, if A, B, and C are identical, the results
    # will contain (A, B) and (A, C).
    size_groups, stats = precheck(directory)    
    candidate_files = get_candidate_files(size_groups)
    stats["files_hashed"] = len(candidate_files)
    file_hashes = {}
    duplicates = []

    total_candidates = len(candidate_files)

    for index, file_path in enumerate(candidate_files, start=1):

        print(
            f"Processing file "
            f"{index} of {total_candidates}: "
            f"{file_path}"
        )

        file_hash = calculate_file_hash(file_path)

        if file_hash is None:
            continue

        if file_hash in file_hashes:
            duplicates.append(
                (file_hashes[file_hash], file_path)
            )
        else:
            file_hashes[file_hash] = file_path
    print("\nScan summary:")
    print(f"Files discovered: {stats['files_seen']:,}")
    print(f"Files skipped:    {stats['files_skipped']:,}")
    print(f"Files hashed:     {stats['files_hashed']:,}")
    return duplicates


def write_results(duplicates, output_file):
    """Write duplicate results to a file."""

    with open(output_file, "w") as file:

        if duplicates:

            file.write("Duplicate files found:\n\n")

            for original, duplicate in duplicates:
                file.write(
                    f"{original}\n"
                    f"{duplicate}\n\n"
                )

        else:
            file.write("No duplicate files found.\n")


def main():

    print(f"Current working directory: {os.getcwd()}") #convenience, so I know where I am

    directory = input("Folder to scan: ").strip()
    directory = os.path.expanduser(directory)
    directory = os.path.abspath(directory) #accepts both relative and absolute paths

    if not os.path.isdir(directory):
        print(f"Directory does not exist: {directory}")
        return

    print(f"Scanning: {directory}")

    duplicates = find_duplicates(directory)

    output_file = "DuplicateFiles.txt"

    write_results(duplicates, output_file)

    print(f"Results written to {output_file}")


if __name__ == "__main__": #could delete and just run main() since this is unlikely to be imported, but it's standard structure
    main()