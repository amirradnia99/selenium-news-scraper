"""
News Scraper for Company Articles via Google News

This script extracts published news articles about companies listed in an Excel file
using Selenium with Chrome WebDriver. The results are saved into a new Excel file.

Author: Your Name
GitHub: https://github.com/yourusername
"""

import pandas as pd
import time
import logging
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# ------------------------- Logging -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ------------------------- Setup WebDriver -------------------------
def setup_driver(headless: bool = True) -> webdriver.Chrome:
    """
    Initialize and configure Chrome WebDriver.
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


# ------------------------- Extract Article Content -------------------------
def get_article_content(driver: webdriver.Chrome, url: str) -> str:
    """
    Extract content from a news article given its URL.
    """
    try:
        main_window = driver.current_window_handle
        driver.execute_script("window.open(arguments[0]);", url)
        time.sleep(2)

        new_window = [w for w in driver.window_handles if w != main_window][0]
        driver.switch_to.window(new_window)
        time.sleep(2)

        selectors = [
            '//article',
            '//div[contains(@class,"article-content")]',
            '//div[contains(@class,"post-content")]',
            '//div[contains(@class,"entry-content")]',
            '//div[contains(@class,"content")]',
            '//div[@id="content"]',
            '//main',
            '//div[contains(@class,"story")]',
            '//div[contains(@class,"body")]',
            '//div/p',
        ]

        content = ""
        for sel in selectors:
            try:
                elements = driver.find_elements(By.XPATH, sel)
                if elements:
                    for el in elements:
                        text = el.text.strip()
                        if text and len(text) > 100:
                            content += text + "\n\n"
                    if content:
                        break
            except Exception:
                continue

        if not content:
            try:
                body = driver.find_element(By.TAG_NAME, 'body')
                content = body.text[:2000]
            except Exception:
                content = "Could not extract content"

        driver.close()
        driver.switch_to.window(main_window)
        return content

    except Exception as e:
        try:
            driver.switch_to.window(main_window)
        except Exception:
            pass
        return f"Error extracting content: {str(e)}"


# ------------------------- Get News Articles -------------------------
def get_company_news(driver: webdriver.Chrome, company_name: str, max_pages: int = 2) -> str:
    """
    Scrape news articles for a given company from Google News.
    """
    news_list = []

    driver.get("https://www.google.com")
    time.sleep(2)

    # Search company name
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        search_box.clear()
        search_box.send_keys(company_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
    except Exception:
        logging.warning(f"Search failed for {company_name}")
        return ""

    # Click News tab
    try:
        news_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"News")]'))
        )
        news_tab.click()
        time.sleep(2)
    except Exception:
        logging.warning(f"No News tab found for {company_name}")
        return ""

    page_num = 1
    while True:
        logging.info(f"{company_name} - Processing page {page_num}")

        # Extract article links
        for i in range(1, 11):
            try:
                xpath = f'(//a[@jsname="YKoRaf"])[{i}]'
                link_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                url = link_element.get_attribute('href')
                title = link_element.text
                logging.info(f"Extracting article {i} on page {page_num}: {title[:50]}...")
                content = get_article_content(driver, url)
                news_list.append(f"{title}\n{content}")
                time.sleep(1)
            except Exception:
                continue

        # Stop if page limit reached
        if page_num >= max_pages:
            break

        # Try to click "Next"
        try:
            next_button = driver.find_element(By.ID, "pnnext")
            next_button.click()
            time.sleep(2)
            page_num += 1
        except Exception:
            logging.info("No more pages available.")
            break

    return "\n\n---\n\n".join(news_list)


# ------------------------- Main Program -------------------------
def main(
    input_file: str = "Data Availability.xlsx",
    output_file: str = "Companies_with_News_Content.xlsx",
    max_companies: int = 2,
    max_pages: int = 2
):
    """
    Main pipeline to read companies, scrape their news, and save results.
    """
    try:
        df = pd.read_excel(input_file)
        logging.info(f"Loaded Excel file with shape: {df.shape}")
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        return

    company_df = pd.DataFrame()
    company_df['Company'] = df.iloc[:, 0]
    company_df['Published News'] = ""

    driver = setup_driver(headless=True)

    try:
        for index, row in company_df.iterrows():
            company_name = row['Company']
            logging.info(f"=== Processing {index+1}/{len(company_df)}: {company_name} ===")
            news_text = get_company_news(driver, company_name, max_pages=max_pages)
            company_df.at[index, 'Published News'] = news_text
            logging.info(f"Finished extracting news for {company_name}")
            time.sleep(2)

            if (index + 1) >= max_companies:
                logging.info("Stopping due to max_companies limit (test mode).")
                break
    finally:
        driver.quit()

    try:
        company_df.to_excel(output_file, index=False)
        logging.info(f"Results saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving results: {e}")


if __name__ == "__main__":
    main()
