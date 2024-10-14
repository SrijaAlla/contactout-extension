from dotenv import load_dotenv
load_dotenv() 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import os

# Load environment variables from the .env file
load_dotenv()

# Get LinkedIn credentials from the .env file
linkedin_email = os.getenv('LINKEDIN_EMAIL')
linkedin_password = os.getenv('LINKEDIN_PASSWORD')
linkedin_self = os.getenv('LINKEDIN_URL')

# chrome_profile_path = "C:/Users/srija/AppData/Local/Google/Chrome/User Data/Profile 1"

chrome_options = Options()

chrome_options.add_extension('JJDEMEIFFADMMJHKBBPGLGNLGEAFOMJO_5_11_7_0.crx')
    
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 30)
driver.get('https://www.linkedin.com/login')



wait = WebDriverWait(driver, 10)

# Login
username = driver.find_element(By.XPATH, "//input[@id = 'username']")
password = driver.find_element(By.XPATH, "//input[@id = 'password']")
username.send_keys(linkedin_email)
password.send_keys(linkedin_password)
submit = driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(20)
actions = ActionChains(driver)
driver.get(linkedin_self)
print("Log in into contactout")
time.sleep(60)


def extract_contact_info(profile_url):
    try:
        driver.get(profile_url)

        print("entered linkedin profile")
        iframe = driver.find_element(By.XPATH,"/html/body/iframe[1]")
        driver.switch_to.frame(iframe)

        time.sleep(30)

        pb7_divs = driver.find_elements(By.XPATH, "//div[contains(@class,'pb-7')]")

        email = driver.find_elements(By.XPATH,"/html/body/div/div/div[3]/div/div/div[1]/div/div[2]/div/div[2]/button")
        for index, button in enumerate(email):
            button.click()
            print("Email")
            time.sleep(10)
            parent_div = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div")))
            spans = parent_div.find_elements(By.XPATH, "/html/body/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div[1]/span")
            for index, span in enumerate(spans):
                print(f"Span {index + 1}: Text = {span.text}")


        phone_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div/div/div[1]/div/div[3]/div/div[2]/button")))
        print("Phone")
        phone_button.click()

        time.sleep(20)
        try: 
            parent_div = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[3]")))
            spans = parent_div.find_elements(By.XPATH, "/html/body/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/span")
            for index, span in enumerate(spans):
                print(f"Span {index + 1}: Text = {span.text}")
        except:
            print("Could not get phone number")
        driver.switch_to.default_content()

        time.sleep(20)
        print("Extracted contact")
    except Exception as e:
        print("Could not extract contact information", e)

try:
    # Open the text file containing LinkedIn profile URLs (each on a new line)
    with open("linkedin_profiles.txt", "r") as file:
        linkedin_profiles = file.readlines()
    
    # Clean up the URLs (remove any whitespace or newline characters)
    linkedin_profiles = [url.strip() for url in linkedin_profiles if url.strip()]
    
    # Loop through each LinkedIn profile URL
    for profile_url in linkedin_profiles:
        extract_contact_info(profile_url)  
        time.sleep(10) 

except FileNotFoundError:
    print("The file 'linkedin_profiles.txt' was not found.")
except Exception as e:
    print(f"An error occurred while processing the profiles: {e}")     