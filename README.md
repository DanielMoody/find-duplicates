# find-duplicates
A Python utility that identifies duplicate files using file size prechecks and SHA-256 content hashing.

## Usage

Run the script:

```bash
python find-duplicates.py
```

You will be prompted for a directory to scan:

```text
Folder to scan:
/Users/example/Documents
```

The script accepts both relative and absolute paths.

## Output

Results are written to:

```text
DuplicateFiles.txt
```

If duplicates are found, the report lists the original file and any matching duplicates.

## Exclusions

The utility skips:

- Empty files
- Symbolic links
- `.DS_Store`
- `.localized`

## Performance Notes

The utility was tested against several datasets.

| Dataset Type | Files Scanned | Files Hashed |
|--------------|--------------:|-------------:|
| Development sandbox | 150,760 | 146,633 |
| Unorganized file collection | 5,055 | 1,004 |
| Organized file collection | 4,976 | 58 |

Files are grouped by size before hashing. Files with unique
sizes cannot be duplicates and are therefore excluded from
hashing.

These results are provided as examples of real-world usage and
should not be interpreted as formal performance benchmarks.
