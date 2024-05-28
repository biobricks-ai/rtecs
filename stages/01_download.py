from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, dotenv, os, pandas as pd

dotenv.load_dotenv()

os.mkdir('download', exist_ok=True)

# Initialize the WebDriver (ChromeDriver should be in your PATH)
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": os.path.abspath('download/pdfs'),  # Set the download directory
    "download.prompt_for_download": False,  # Disable download prompt
    "plugins.always_open_pdf_externally": True  # Open PDFs externally (not in Chrome)
}
options.add_experimental_option("prefs", prefs)

# Initialize the WebDriver (ChromeDriver should be in your PATH)
driver = webdriver.Chrome(options=options)

# Open the browser and navigate to the login page
driver.get('https://msdssrc.net/')  # Change this to the URL of the login page

# Allow some time for the page to load
time.sleep(2)

# Find the login form elements and enter credentials
username_field = driver.find_element(By.NAME, 'username')  # Change 'username' to the name or id of the username field
password_field = driver.find_element(By.NAME, 'passwd')  # Change 'password' to the name or id of the password field

username_field.send_keys(os.getenv('username'))  # Replace with your username
password_field.send_keys(os.getenv('password'))  # Replace with your password

# Submit the form
password_field.send_keys(Keys.RETURN)

# Allow some time for the login process to complete
time.sleep(3)

search_field = driver.find_element(By.ID, 'btnSearch') 
search_field.click()

def get_sheet_data():
    # get the table
    table = driver.find_element(By.CLASS_NAME, 'w3-table-all')
    df = pd.read_html(table.get_attribute('outerHTML'))[0]
    
    # get hrefs
    links = [l.get_attribute('href') for l in driver.find_elements(By.TAG_NAME, 'a')]
    df['View'] = [l for l in links if 'download.php?sheet_ID=' in l]
    
    return df

page = 1
dfs = []
while True:
    print(page)
    dfs += [get_sheet_data()]
    try:
        next_button = driver.find_element(By.XPATH, f'//button[text()="{page + 1}"]')
        next_button.click()
        page += 1
        time.sleep(1)
    except:
        break
    
df = pd.concat(dfs)
df = df.drop_duplicates()
df['sheet_id'] = df['View'].str.extract('sheet_ID=(\d+)').astype(int)
# create filenames from sheet_id
df['filename'] = df['sheet_id'].astype(str) + '.pdf'

# write df to download/sds.csv
df.to_csv('download/sds.csv', index=False)

hrefs = df['View'].tolist()
filenames = df['filename'].tolist()
# download all hrefs (slowly) into download/sheets. give them product names
for i, (href, filename) in enumerate(zip(hrefs, filenames)):
    print(filename)
    # if filename exists, skip
    if os.path.exists(f'download/pdfs/{filename}'):
        continue
    driver.get(href)
    # Allow some time for the download to complete
    time.sleep(3)
    # get the most recent download and rename it
    os.rename('download/pdfs/sheet.pdf', f'download/pdfs/{filename}')

# zip the pdfs directory
import shutil
shutil.make_archive('download/sds', 'zip', 'download/pdfs')
driver.quit()