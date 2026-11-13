# Moving Average Price Calculator

A Python application that calculates trailing moving averages for two financial instruments using historical price observations. Calculated results are stored in a local JSON cache for future retrieval.

The application supports both command-line execution and a REST API built with FastAPI.

## Requirements

- Python 3.13 (tested version)
- FastAPI
- Uvicorn

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/IzaSurma/Nykredit_tech_excercise.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Nykredit_tech_excercise
   ```

3. Verify your Python installation:

   ```bash
   python --version
   ```

4. Install the required dependencies:

   ```bash
   python -m pip install fastapi uvicorn
   ```

## Usage

### Calculate Moving Averages

Run the following command from the project root:

```bash
python -m src.runners.moving_average <window_size>
```

Example:

```bash
python -m src.runners.moving_average 3
```

This calculates the trailing 3-calendar-day moving average for both instruments and saves the results to `data/moving_average_cache.json`.

The window includes the current observation date and the preceding `window_size - 1` calendar days.

Only available, valid observations within the window are included in the calculation.

### Retrieve Cached Results

Run the following command:

```bash
python -m src.runners.retrieve_results <window_size>
```

Example:

```bash
python -m src.runners.retrieve_results 3
```

This retrieves previously calculated moving averages for both instruments using the specified window size.

If no cached results exist for that window size, the application returns `None`.

## REST API

The application also exposes two endpoints using FastAPI.

### Start the API Server

From the project root, run:

```bash
python -m uvicorn src.api.api:app --reload
```

By default, the API is available at:

`http://127.0.0.1:8000`

Interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

### Calculate Moving Averages

**Endpoint:** `GET /calculate`

Example request:

```http
GET http://127.0.0.1:8000/calculate?window_size=3
```

This calculates moving averages for all instruments, caches the results, and returns them as JSON.

### Retrieve Cached Moving Averages

**Endpoint:** `GET /results`

Example request:

```http
GET http://127.0.0.1:8000/results?window_size=3
```

This retrieves previously cached moving averages for the requested window size.

If no cached results exist, the API returns HTTP `404`.

## Key Assumptions

- **Calendar-day window:** Moving averages are calculated using calendar days rather than a fixed number of trading observations. Only available observations within the specified window are included.
- **Missing prices:** Observations containing `null` or nonnumeric prices are excluded from calculations.
- **Invalid dates:** Dates must follow the `YYYY-MM-DD` format. Invalid dates are reported and excluded.
- **Outliers:** Unusually high or negative prices are retained if they are valid numeric values. No automatic outlier correction is applied because this could alter the original financial data.
- **Partial windows:** Moving averages are calculated even when fewer observations than the requested window size are available.
- **Caching:** Results are stored locally in JSON files and identified by their window size. Recalculating the same window size overwrites the previously cached results.

## Unfinished Work and Next Steps

The application implements the core moving-average calculation, JSON caching, result retrieval, and REST API endpoints.

Given more time, I would focus on:

1. **Automated testing:** Add unit tests using `pytest` to verify moving-average calculations, invalid dates, missing prices, empty datasets, and cache retrieval.
2. **Improved input validation:** Introduce stricter validation and clearer error messages for invalid window sizes and malformed input data.
3. **Outlier handling:** Investigate unusually high and negative prices and define an appropriate handling strategy based on business requirements.
4. **Cache invalidation:** Detect changes to the input dataset and invalidate outdated cached results.
5. **Performance optimization:** Improve the moving-average algorithm for larger datasets by avoiding repeated scans of all observations.
6. **API improvements:** Add endpoints for retrieving results for a specific instrument or observation date, and improve response naming and validation.

## Tools and Technologies Used

- **Python 3.13:** Main programming language used to implement the application.
- **Python standard library:** Used `json` for reading and writing data, `datetime` for date calculations, `pathlib` for file management, and `argparse` for command-line interfaces.
- **FastAPI:** Framework used to expose the calculation and retrieval functionality through REST API endpoints.
- **Uvicorn:** ASGI server used to run the FastAPI application locally.
- **JSON:** Used for both historical input data and persistent caching of calculated results.
- **Git and GitHub:** Used for version control and storing the project repository.
- **ChatGPT (OpenAI):** Used as an AI-assisted development tool to discuss implementation approaches, troubleshoot Python errors, review code, and improve documentation. The application logic and implementation decisions were reviewed and integrated into the project by the developer.

## Development Approach

The solution was implemented using Python and its standard library for the core calculations and caching functionality, minimizing external dependencies.

FastAPI was added to make the existing functionality accessible through HTTP endpoints without duplicating the calculation logic.

The implementation prioritizes readability, modularity, and straightforward result retrieval over advanced optimizations.