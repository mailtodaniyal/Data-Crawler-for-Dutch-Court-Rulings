import time
import random

# Simulated case data for demonstration purposes
FAKE_CASES = [
    {"ECLI Number": "ECLI:NL:2025:0001", "Date": "2025-03-29", "Court Name": "Supreme Court", "Title": "Case A", "Full Text": "Lorem ipsum dolor sit amet."},
    {"ECLI Number": "ECLI:NL:2025:0002", "Date": "2025-03-28", "Court Name": "District Court", "Title": "Case B", "Full Text": "Consectetur adipiscing elit."},
    {"ECLI Number": "ECLI:NL:2025:0003", "Date": "2025-03-27", "Court Name": "Appeal Court", "Title": "Case C", "Full Text": "Sed do eiusmod tempor incididunt."}
]

def simulate_scraping():
    print("Starting fake scraping process...")
    
    for i, case in enumerate(FAKE_CASES, start=1):
        time.sleep(random.uniform(1, 2))  # Simulating a delay like real scraping
        print(f"Scraped case {i}: {case['ECLI Number']} - {case['Title']}")
    
    print("Scraping complete! Showing sample data:")
    for case in FAKE_CASES:
        print(f"\nTitle: {case['Title']}\nDate: {case['Date']}\nCourt: {case['Court Name']}\nFull Text: {case['Full Text'][:50]}...")

if __name__ == "__main__":
    simulate_scraping()
