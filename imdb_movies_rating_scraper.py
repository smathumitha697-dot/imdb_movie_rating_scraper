import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.imdb.com/chart/top/")

print("Waiting for page to load. If a verification page appears, solve it now.")
print("You have 30 seconds.")
time.sleep(30)

print(driver.title)

rows = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
print("Rows found:", len(rows))

data = []
for i, row in enumerate(rows):
    try:
        title = row.find_element(By.CSS_SELECTOR, "a.ipc-title-link-wrapper").text
        rating = row.find_element(By.CSS_SELECTOR, "span[class*='rating-star']").text.split("\n")[0]
        data.append([i + 1, title, rating])
    except Exception as e:
        print("Row", i, "failed:", e)

print("Total collected:", len(data))

df = pd.DataFrame(data, columns=["rank", "title", "rating"])
df.to_csv("imdb_top_movies.csv", index=False)
print("Done! Data saved to imdb_top_movies.csv")

driver.quit()