# Plex Watchlist RSS Formatter

This script fetches RSS feeds (specifically designed for Plex watchlists), parses the item data (Title, Release Year, Category, Link), and outputs a formatted text list. It also handles basic deduplication of items across multiple feeds.

## Features

- **Fetch & Parse**: Retrieves RSS XML from provided URLs.
- **Data Extraction**: Extracts Title, Year, Category (Type), and Link.
- **Deduplication**: Prevents duplicate entries based on the item link.
- **Formatted Output**: Generates a text file (`output.txt` or specified path), or prints directly with `--print`.
- **Blacklist**: Skips items whose titles appear in a manually maintained blacklist file.

## Prerequisites

- Python 3.6+
- `python-dotenv` library

## Installation

1.  **Clone the repository** (or download usage files):
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Create a `.env` file in the root directory. You can use `.env.example` as a template.
2.  Add your RSS feed URLs to the `RSS_URLS` variable, separated by commas.

    **Example `.env`**:
    ```env
    RSS_URLS=https://rss.plex.tv/feed1-uuid,https://rss.plex.tv/feed2-uuid
    ```

## Usage

Run the script from the command line:

```bash
python3 format.py
```

### Optional Flags

- `--remove-unreleased`: Filters out items with release years in the future (not yet released).
- `--output` / `-o`: Specify the path to the output file (default: `output.txt`).
- `--blacklist`: Path to the blacklist txt file.
- `--print`: Print the formatted output directly instead of writing to a file.

**Example with flags**:
```bash
python3 format.py --remove-unreleased --output my_watchlist.txt
python3 format.py --print
```

### Blacklist

Add titles to `blacklist.txt` (one per line) to exclude them from the output. Lines starting with `#` are treated as comments.

```text
# My blacklist
Some Movie I Don't Want
Another Show
```

Matching is case-insensitive. The blacklist file is not required — if it doesn't exist, no filtering is applied.

Upon success, an `output.txt` file will be generated in the same directory containing the formatted list of items.

## Output Format

The output file will contain entries in the following format:

```text
#1:
   Title: Movie Title
   Released: 2023
   Type: MOVIE
   Link: https://watch.plex.tv/movie/link-to-movie

#2:
   Title: Show Title
   Released: 2022
   Type: SHOW
   Link: https://watch.plex.tv/show/link-to-show
...
```
