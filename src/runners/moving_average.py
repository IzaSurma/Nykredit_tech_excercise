import argparse
import json
from pathlib import Path

from src.data_parser import cache_results, calculate_moving_average


def project_root():
        for parent in Path(__file__).resolve().parents:
            if (parent / "data").is_dir():
                return parent
        raise FileNotFoundError("Could not find project root containing data")

data_dir = project_root() / "data"

def calculate_moving_average_price(window_size: int):
    
    with open(data_dir / "input_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    moving_averages = calculate_moving_average(data, window_size)

    return moving_averages

def cache_moving_averages(window_size: int, moving_averages: dict):
    cache_file = data_dir / "moving_average_cache.json"
    cache_results(cache_file, window_size, moving_averages)

def main():
    parser = argparse.ArgumentParser(description="Calculate moving averages for all instruments.")
    parser.add_argument("window_size", type=int, help="Moving average window size in calendar days")

    args = parser.parse_args()

    results = calculate_moving_average_price(args.window_size)
    cache_moving_averages(args.window_size, results)

    print(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()