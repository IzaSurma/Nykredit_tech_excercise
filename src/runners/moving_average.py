import argparse
import json

from src.data_parser import DataParser

DATA_DIR = DataParser._project_root() / "data"
CACHE_FILE = DATA_DIR / "moving_average_cache.json"

def main():
    parser = argparse.ArgumentParser(description="Calculate moving averages for all instruments.")
    parser.add_argument("window_size", type=int, help="Moving average window size in calendar days")

    args = parser.parse_args()

    results = calculate_moving_average_price(args.window_size)

    print(json.dumps(results, indent=4))

def calculate_moving_average_price(window_size: int):
    
    with open(DATA_DIR / "input_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    data_parser = DataParser(data, window_size)   

    moving_averages = data_parser.calculate_moving_average()
    data_parser.cache_results(CACHE_FILE, moving_averages)

    return moving_averages


if __name__ == "__main__":
    main()