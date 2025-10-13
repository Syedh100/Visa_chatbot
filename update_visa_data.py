import requests
from bs4 import BeautifulSoup
import os
import time

def fetch_gov_uk_visa_info():
    base_url = "https://www.gov.uk/browse/visas-immigration"
    print("🔍 Fetching visa links from GOV.UK...")

    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch main page: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Find visa-related links
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if "/visas" in href or "/immigration" in href:
            full_url = href if href.startswith("https") else f"https://www.gov.uk{href}"
            if full_url not in links:
                links.append(full_url)

    print(f"✅ Found {len(links)} visa-related pages.")

    # Crawl and extract content from each page
    collected_data = []
    for i, url in enumerate(links[:15]):  # Limit to 15 pages for speed (can increase later)
        print(f"📄 Fetching page {i+1}/{len(links)}: {url}")
        try:
            # Add delay to be respectful to the server
            if i > 0:
                time.sleep(1)
                
            page = requests.get(url, timeout=10)
            page.raise_for_status()
            page_soup = BeautifulSoup(page.text, "html.parser")

            # Extract readable text only
            paragraphs = [p.get_text(strip=True) for p in page_soup.find_all("p")]
            title = page_soup.find("h1").get_text(strip=True) if page_soup.find("h1") else url
            page_text = "\n".join(paragraphs)

            # Only add if we got meaningful content
            if page_text.strip() and len(page_text) > 100:
                collected_data.append(f"\n\n---\n## {title}\nSource: {url}\n\n{page_text}")
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout for {url}")
        except Exception as e:
            print(f"⚠️ Skipped {url} due to error: {e}")

    # Save to the knowledge base file
    os.makedirs("knowledge_base", exist_ok=True)
    file_path = os.path.join("knowledge_base", "uk_visa_info.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(collected_data))

    print(f"\n✅ Visa data successfully saved to {file_path}")

if __name__ == "__main__":
    fetch_gov_uk_visa_info()