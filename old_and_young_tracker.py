from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import time

def run_tracker(target_url, category_name):
    print(f"\n🚀 Launching Tracker for: {category_name}")
    
    options = Options()
    options.add_argument("--headless") # Comment this out to see the browser in action!
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(target_url)
        
        # Wait for the products to actually render
        print("⏳ Waiting for page to render...")
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        
        # Give JS a few extra seconds to breathe
        time.sleep(5) 

        # Broad capture of all text in product-like containers
        items = driver.find_elements(By.CSS_SELECTOR, "li, div[class*='product'], div[class*='card']")
        
        data = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        for item in items:
            text = item.text
            if ("NGN" in text or "₦" in text) and len(text) > 10:
                # Split text into lines to separate Name from Price
                parts = text.split('\n')
                name = parts[0]
                
                # Find the line that looks like a price
                price_line = next((p for p in parts if "NGN" in p or "₦" in p), None)
                
                if price_line:
                    # Strip everything but numbers
                    clean_price = "".join(filter(str.isdigit, price_line.split('.')[0]))
                    if clean_price:
                        data.append({
                            'Date': timestamp,
                            'Category': category_name,
                            'Item': name,
                            'Price_NGN': int(clean_price)
                        })

        if data:
            df = pd.DataFrame(data).drop_duplicates(subset=['Item'])
            print(f"✅ Found {len(df)} items!")
            return df
        else:
            print("❌ No items found. The site might be heavily protected.")
            return pd.DataFrame()

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return pd.DataFrame()
    finally:
        driver.quit()

if __name__ == "__main__":
    # Task 1: Baby Meds
    baby_df = run_tracker("https://healthplusnigeria.com/collections/baby-care", "Baby_Meds")
    
    # Task 2: Senior/Chronic Meds
    senior_df = run_tracker("https://medplusnig.com/product-category/health/chronic-care/", "Senior_Meds")
    
    # Merge and Save
    final_report = pd.concat([baby_df, senior_df], ignore_index=True)
    
    if not final_report.empty:
        final_report.to_csv('old_and_young_prices.csv', index=False)
        print("\n🏆 MISSION ACCOMPLISHED: 'old_and_young_prices.csv' is ready.")
    
    input("\nPress Enter to exit...")