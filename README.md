# Prospektmaschine Brochure Parser

A Python-based tool to scrape and parse hypermarket brochure data from the [prospektmaschine.de/hypermarkte](https://www.prospektmaschine.de/hypermarkte) website. This tool fetches brochure information, including titles, validity dates, links, and thumbnails, and outputs the data in JSON format.

---

## Features

- Asynchronous HTTP requests for efficient data fetching.
- Configurable options for concurrency, retries, timeouts, and delays.
- Parses brochure data, including:
  - Title
  - Validity period
  - Link to the brochure
  - Thumbnail image
- Outputs the parsed data to a JSON file.

---

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package manager)
- Use `pip install -r requirements.txt` to install the necessary libraries

---

### Example usage
- `py parser.py` to run with default options
- `py parser.py -h` to show available options
