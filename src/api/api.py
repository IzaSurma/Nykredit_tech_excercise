from pathlib import Path

from fastapi import FastAPI, HTTPException

from src.runners.moving_average import (
    cache_moving_averages,
    calculate_moving_average_price,
)
from src.runners.retrieve_results import retrieve_results

app = FastAPI()

cache_file = Path("data/moving_average_cache.json")


@app.get("/calculate")
def calculate(window_size: int):
    moving_average_price = calculate_moving_average_price(window_size)
    cache_moving_averages(window_size, moving_average_price)

    return {
        "window_size": window_size,
        "average_price": moving_average_price
    }
    

@app.get("/results")
def retrieve(window_size: int):
    moving_average_price = retrieve_results(window_size)

    if moving_average_price is None:
        raise HTTPException(
            status_code=404,
            detail="No cached result found"
        )

    return {
        "window_size": window_size,
        "average_price": moving_average_price
    }