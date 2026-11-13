import argparse
from pathlib import Path

from src.data_parser import retrieve_cached_results


def project_root():
        for parent in Path(__file__).resolve().parents:
            if (parent / "data").is_dir():
                return parent
        raise FileNotFoundError("Could not find project root containing data")

cache_file = project_root() / "data" / "moving_average_cache.json"

def retrieve_results(window_size: int):
    moving_average_price = retrieve_cached_results(cache_file, window_size)
    return moving_average_price

def main() -> None:
    
    parser = argparse.ArgumentParser(description="Retrieve moving average price for a given window size.")
    parser.add_argument("window_size", type=int, help="Moving average window size in calendar days")
    args = parser.parse_args()

    window_size = args.window_size
    moving_average_price = retrieve_results(window_size)

    print(f"Moving average price for the selected window size ({window_size} days): {moving_average_price}")

if __name__ == "__main__":
    main()