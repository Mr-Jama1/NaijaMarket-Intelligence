import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import time
import random

def scrape_cars_multipage(max_pages=3):
    print(f"👻 Launching Multi-Page Ghost Scraper (Target: {max_pages} pages)")
    
    options = uc.ChromeOptions()
    # options.add_argument('--headless') # Keep visible to monitor progress
    driver = uc.Chrome(options=options)
    
    all_car_loot = []
    timestamp = datetime.now().strftime("%Y-%m-%d")

    try:
        for page_num in range(1, max_pages + 1):
            url = f"https://jiji.ng/cars?page={page_num}"
            print(f"📡 Processing Page {page_num}: {url}")
            
            driver.get(url)
            
            # 1. Wait for anti-bot & initial load
            time.sleep(random.randint(7, 12)) 
            
            # 2. Scroll to trigger lazy-loading of items
            driver.execute_script("window.scrollTo(0, 1200);")
            time.sleep(3)

            # 3. Extract items from the current page
            items = driver.find_elements(By.CSS_SELECTOR, "div[class*='advert'], .b-list-advert-base")
            
            page_items_count = 0
            for item in items:
                try:
                    text = item.text
                    if '₦' in text or 'NGN' in text:
                        lines = text.split('\n')
                        all_car_loot.append({
                            'Date': timestamp,
                            'Title': lines[0],
                            'Price': next((l for l in lines if '₦' in l), "N/A"),
                            'Info': " | ".join(lines[1:4])
                        })
                        page_items_count += 1
                except:
                    continue
            
            print(f"✅ Found {page_items_count} items on Page {page_num}")
            
            # 4. Human-like pause between pages
            if page_num < max_pages:
                wait_time = random.randint(5, 10)
                print(f"😴 Sleeping for {wait_time}s to avoid detection...")
                time.sleep(wait_time)

        # Save everything to one big CSV
        if all_car_loot:
            df = pd.DataFrame(all_car_loot).drop_duplicates(subset=['Title', 'Price'])
            df.to_csv('nigeria_car_market_bulk.csv', index=False)
            print(f"\n🏆 MISSION COMPLETE: Total {len(df)} unique cars saved!")
        else:
            print("❌ No data captured.")

    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Change 'max_pages' to however many pages you want to scrape
    scrape_cars_multipage(max_pages=5) 
    input("\nPress Enter to exit...")