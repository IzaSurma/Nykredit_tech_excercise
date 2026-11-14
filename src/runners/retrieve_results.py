import argparse

from src.data_parser import DataParser

DATA_DIR = DataParser._project_root() / "data"

CACHE_FILE = DATA_DIR / "moving_average_cache.json"

def retrieve_results(window_size: int):
    moving_average_price = DataParser.retrieve_cached_results(CACHE_FILE, window_size)
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