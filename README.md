# Selenium News Scraper

A lightweight and efficient Python-based web scraping tool for extracting news headlines and articles using **Selenium**. This repository provides a simple, customizable solution for collecting data from dynamic websites where static HTML parsing may not be sufficient.

---

## Features

- **Dynamic Website Support:**
    - Handles websites that load content with JavaScript
    - Works with various page structures and layouts

- **Automated Scraping:**
    - Extracts news headlines, article text, links, and metadata
    - Easily configurable to target multiple websites

- **Robust Error Handling:**
    - Retry mechanisms for failed requests
    - Graceful handling of missing or malformed elements

- **Export Options:**
    - Save results to CSV, JSON, or database-friendly formats
    - Ready for integration with downstream data pipelines

---

## Requirements

- Python 3.8 or newer (recommended)
- Google Chrome or Firefox (with matching WebDriver)
- Conda or virtualenv (recommended for isolated environment)

---

## Installation

1. Clone this repository:
    ```bash
    git clone [https://github.com/amirradnia99/selenium-news-scraper.git](https://github.com/amirradnia99/selenium-news-scraper.git)
    cd selenium-news-scraper
    ```

2. Create and activate a new virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux / macOS
    venv\Scripts\activate      # Windows
    ```

3. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Download and place the correct WebDriver (ChromeDriver or GeckoDriver) in your system PATH.

---

## Usage

1. **Prepare your input file** as an Excel sheet (`Data Availability.xlsx`) with at least one column named `Company`:

| Company |
|---|
| Tesla |
| Microsoft |
| Google |

2. **Run the scraper**:
    ```bash
    python scraper.py
    ```

---

## Configuration

1. **Update parameters** in the `main()` function inside `scraper.py` to customize behavior:

| Company | Published News |
|---|---|
| Tesla | Tesla plans new Gigafactory... |
| Microsoft | Microsoft announces AI updates... |

---

## Dependencies

- pandas
- selenium
- openpyxl
- logging (standard library)

---

## Notes

- Ensure your **WebDriver** version matches your installed browser version.
- Headless mode can be enabled for faster scraping and less resource usage.
- Respect website scraping policies and **Terms of Service**.
- Adjust `max_companies` and `max_pages` for testing or full dataset scraping.

---

## Example

```bash
# Example snippet from scraper.py
company_list = ["Tesla", "Microsoft", "Google"]
for company in company_list:
    news_text = get_company_news(driver, company, max_pages=3)
    print(news_text[:500])  # Preview first 500 characters
  
---

## License

MIT License © Amir Radnia

## Contact

For issues or questions, feel free to open an issue or contact me at amir.radnia99@gmail.com
