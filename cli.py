# Author: Ivan Rachler
import argparse

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Parse hypermarket brochures from prospektmaschine.de")
    parser.add_argument("-c", "--concurrent", type=int, default=5, help="Number of concurrent requests")
    parser.add_argument("-r", "--retries", type=int, default=3, help="Number of retries for each request")
    parser.add_argument("-t", "--timeout", type=float, default=5.0, help="Request timeout in seconds")
    parser.add_argument("-d", "--delay", type=float, default=1.0, help="Delay between retries in seconds")
    parser.add_argument("-o", "--output", type=str, default="output.json", help="Output file name")
    args = parser.parse_args()
    if args.concurrent < 1:
        raise ValueError("Number of concurrent requests must be greater than 0")
    if args.retries < 1:
        raise ValueError("Number of retries must be greater than 0")
    if args.timeout < 0:
        raise ValueError("Timeout must be a non-negative number")
    if args.delay < 0:
        raise ValueError("Delay must be a non-negative number")
    return args