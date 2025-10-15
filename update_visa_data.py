import requests
from bs4 import BeautifulSoup
import os
import time

def fetch_gov_uk_visa_info():
    url = "https://www.gov.uk/browse/visas-immigration"
    print("Getting visa info from gov.uk")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error getting page: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # find links
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/visas" in href or "/immigration" in href:
            full_url = href if href.startswith("https") else f"https://www.gov.uk{href}"
            if full_url not in links:
                links.append(full_url)

    print(f"Found {len(links)} pages")

    # get content from pages
    data = []
    for i, url in enumerate(links[:10]):
        print(f"Getting page {i+1}: {url}")
        try:
            if i > 0:
                time.sleep(1)
                
            page = requests.get(url, timeout=10)
            page.raise_for_status()
            page_soup = BeautifulSoup(page.text, "html.parser")

            # get text
            paragraphs = [p.get_text(strip=True) for p in page_soup.find_all("p")]
            title = page_soup.find("h1").get_text(strip=True) if page_soup.find("h1") else url
            page_text = "\n".join(paragraphs)

            if page_text.strip() and len(page_text) > 100:
                data.append(f"\n\n---\n## {title}\nSource: {url}\n\n{page_text}")
        except Exception as e:
            print(f"Error with {url}: {e}")

    # save to file
    os.makedirs("knowledge_base", exist_ok=True)
    file_path = os.path.join("knowledge_base", "uk_visa_info.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(data))

    print(f"Saved to {file_path}")

if __name__ == "__main__":
    fetch_gov_uk_visa_info()