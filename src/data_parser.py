import json
from datetime import date, timedelta


def convert(date_str):
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        print(f"Invalid date format: {date_str}")
        return None

def calculate_moving_average(data, window_size):
    if window_size <= 0:
        raise ValueError("Window size must be positive")

    results = {}

    for instrument, prices in data.items():
        if instrument == "Description":
            continue

        valid_prices = []

        for item in prices:
            item_date = convert(item["date"])
            item_price = item["price"]

            if item_date is not None and isinstance(item_price, (int, float)) and not isinstance(item_price, bool):
                valid_prices.append({
                    "date": item_date,
                    "price": item_price
                })

        sorted_prices = sorted(
            valid_prices,
            key=lambda x: x["date"]
        )

        moving_averages = []

        for item in sorted_prices:
            current_date = item["date"]
            window_start = current_date - timedelta(days=window_size - 1)

            window_prices = [
                p["price"]
                for p in sorted_prices
                if window_start <= p["date"] <= current_date
            ]

            if window_prices:
                average = sum(window_prices) / len(window_prices)

                moving_averages.append({
                    "date": current_date.isoformat(),
                    "moving_average": average
                })

        results[instrument] = moving_averages

    return results

def cache_results(cache_file, window_size, results):
    window_size = f"{window_size}_days"

    if cache_file.exists():
        with cache_file.open("r", encoding="utf-8") as file:
            cache = json.load(file)
    else:
        cache = {
            "Description": "Average price calculated for the specified time period", 
            "data": {}
            }

    cache["data"][window_size] = {
        "results": results
    }
    with cache_file.open("w", encoding="utf-8") as file:
        json.dump(cache, file, indent=4)

def retrieve_cached_results(cache_file, window_size):

    if cache_file.exists():
        with cache_file.open("r", encoding="utf-8") as file:
            cache = json.load(file)

        window_size = f"{window_size}_days"

        if window_size in cache["data"]:
            return cache["data"][window_size]["results"]
            
    return None


