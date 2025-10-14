import requests
from bs4 import BeautifulSoup
import os
import time

# function to scrape visa info from gov.uk
def fetch_gov_uk_visa_info():
    base_url = "https://www.gov.uk/browse/visas-immigration"
    print("Getting visa information from GOV.UK...")

    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("Failed to load main page:", e)
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # find all visa-related links
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if "/visa" in href or "/immigration" in href:
            full_url = href if href.startswith("https") else f"https://www.gov.uk{href}"
            if full_url not in links:
                links.append(full_url)

    print(f"Found {len(links)} visa-related pages")

    # get text from each page
    visa_data = []
    for i, url in enumerate(links[:15]):  # limit to first 15 pages for speed
        print(f"Reading page {i+1}/{len(links)}: {url}")
        try:
            if i > 0:
                time.sleep(1)  # be polite to the server

            page = requests.get(url, timeout=10)
            page.raise_for_status()
            page_soup = BeautifulSoup(page.text, "html.parser")

            # get title and paragraphs
            title = page_soup.find("h1").get_text(strip=True) if page_soup.find("h1") else url
            paragraphs = [p.get_text(strip=True) for p in page_soup.find_all("p")]
            page_text = "\n".join(paragraphs)

            # only keep pages with useful info
            if len(page_text) > 100:
                visa_data.append(f"\n---\n{title}\n{url}\n\n{page_text}")

        except Exception as e:
            print(f"Skipped {url} because of an error:", e)

    # save all text to a file
    os.makedirs("Knowledge_base", exist_ok=True)
    file_path = os.path.join("Knowledge_base", "uk_visa_info.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(visa_data))

    print(f"\nDone! Saved visa info to {file_path}")


# run the script directly
if __name__ == "__main__":
    fetch_gov_uk_visa_info()