# find-duplicates
A Python utility that identifies duplicate files using file size prechecks and SHA-256 content hashing.

## Performance Notes

The utility was tested against several real-world datasets.

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
