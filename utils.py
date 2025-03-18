import re
from datetime import datetime
from bs4 import element

def filter_thumbnail(tag: element.Tag) -> bool:
    """
    Filters out html tags that do not contain a brochure thumbnail link.

    Args:
        tag (element.Tag): The tag to be checked.

    Returns:
        bool: True if the tag is an image tag with a thumbnail link, False otherwise.
    """
    return tag.name == "img" and (tag.has_attr("data-src") or tag.has_attr("src"))

def validity_check(validity: str) -> tuple[bool, dict]:
    """
    Checks if a brochure is currently valid based on its validity string.

    Args:
        validity (str): The validity string to be checked.

    Returns:
        tuple[bool, dict]: A tuple containing a boolean indicating if the brochure is valid and a dictionary with parsed validity information.
    """
    now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # Checks if validity string contains a date range
    range_match = re.search(r"(\d{2}\.\d{2}\.\d{4})\s*-\s*(\d{2}\.\d{2}\.\d{4})", validity)
    if range_match:
        start_date = datetime.strptime(range_match.group(1), "%d.%m.%Y").date().strftime("%Y-%m-%d")
        end_date = datetime.strptime(range_match.group(2), "%d.%m.%Y").date().strftime("%Y-%m-%d")
        return (start_date <= now <= end_date, {
            "valid_from": start_date,
            "valid_to": end_date,
            "parsed_time": now
        })
    
    # Checks if validity string only contains the start date
    single_date_match = re.search(r"(\d{2}\.\d{2}\.\d{4})", validity)
    if single_date_match:
        start_date = datetime.strptime(single_date_match.group(1), "%d.%m.%Y").date().strftime("%Y-%m-%d")
        return (start_date <= now, {
            "valid_from": start_date,
            "parsed_time": now
        })
    
    return False, {}

