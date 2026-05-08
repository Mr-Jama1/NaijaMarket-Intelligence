import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import time

def scrape_cars_stealth():
    print("👻 Launching Ghost Protocol Scraper...")
    
    # 1. Initialize Undetected Chromedriver
    options = uc.ChromeOptions()
    # options.add_argument('--headless') # Keep it visible for the first run to see if it works
    
    driver = uc.Chrome(options=options)
    
    try:
        url = "https://jiji.ng/cars" 
        driver.get(url)
        
        print("⏳ Waiting for the 'Anti-Bot' to clear...")
        time.sleep(10) # Give it time to solve any hidden challenges
        
        # 2. Scroll down to load "Lazy" items
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(3)

        # 3. Find Product Cards
        # Jiji usually uses 'b-list-advert-base' or 'qa-advert-list-item'
        items = driver.find_elements(By.CSS_SELECTOR, "div[class*='advert'], .b-list-advert-base")
        
        car_loot = []
        timestamp = datetime.now().strftime("%Y-%m-%d")

        for item in items:
            try:
                text = item.text
                if '₦' in text or 'NGN' in text:
                    lines = text.split('\n')
                    # Structure usually: [Title, Price, Location, Year/Condition]
                    car_loot.append({
                        'Date': timestamp,
                        'Title': lines[0],
                        'Price': next((l for l in lines if '₦' in l), "N/A"),
                        'Info': " | ".join(lines[1:4])
                    })
            except:
                continue

        if car_loot:
            df = pd.DataFrame(car_loot).drop_duplicates(subset=['Title', 'Price'])
            df.to_csv('nigeria_car_market_large.csv', index=False)
            print(f"🏆 MISSION COMPLETE: Captured {len(df)} cars!")
        else:
            print("❌ Still no data. They've updated the Shield. Checking page source...")
            # Debug: print(driver.page_source[:500]) 

    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_cars_stealth()
    input("\nPress Enter to exit...")