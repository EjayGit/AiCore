import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException#
from webdriver_manager.chrome import ChromeDriverManager

class Scraper:
    def __init__(self, url: str = 'https://www.zoopla.co.uk'):
        self.driver = Chrome(ChromeDriverManager().install())
        self.driver.get(url)

    def acceptCookies(self, xpath: str = '//button[@id="save"]'):
        try:
            time.sleep(2)
            search_bar = self.driver.switch_to.frame('gdpr-consent-notice')
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))# -> does not work => search_bar.click()#
            self.driver.find_element(By.XPATH, xpath).click()
        except TimeoutException:
            print('No cookies found')

    def lookForSearchBar(self, xpath: str = '//input[@id="filters-location-mobile"]'):
        try:
            time.sleep(1)
            search_bar = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
            search_bar.click()
            return search_bar
        except TimeoutException:
            print('No search bar found')
            return None

    def sendKeysToSearchBar(self, text):
        search_bar = self.lookForSearchBar()
        if search_bar:
            search_bar.send_keys(text)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(3)
        else:
            raise Exception('No search bar found')

    def findPages(self):
        # Look for <div data-testid='pagination'>, and the text (isdigit) in the <a> of the second to last <li> is the last page number needed. Put into lastPage.
        pages = bot.driver.find_elements(By.XPATH, "//div[@data-testid='pagination']//*[starts-with(@aria-label, 'Page ')]")
        lastPage = int(pages[-1].text)
        return lastPage

    def extractPageData(self):
        propertyList = []
        properties = self.driver.find_elements(By.XPATH, "//div[starts-with(@data-testid, 'search-result_listing_')]")
        for property in properties:
            propertyList.append(property.text.splitlines())

#https://www.zoopla.co.uk/for-sale/property/cambridgeshire/cambridge/?q=Cambridge&results_sort=newest_listings&search_source=home&pn=3

#//*[@id="__next"]/div[3]/div[2]/main/div[2]/div[3]/ul/li[8]/a
#//*[@id="__next"]/div[3]/div[2]/main/div[2]/div[3]/ul/li[9]/a



    def navThroughPages(self):
        lastPage = bot.findPages()
        for page in range(2,lastPage+1):
            # Find and select the page to be scraped.
            xpath = f'//div[@data-testid="pagination"]//*[@aria-label, "Page {page}"]'
            test1 = self.driver.find_element(By.XPATH, xpath)
            # For each property, locate desired data and append data into JSON format { Key: Value[0], Value[1] Value[x] }.
            extractPageData()
            


# If you are running the script directly, run, otherwise ignore (if importing it).
if __name__ == '__main__':
    
    # Initiate dict and obj
    propertyDetails = {"Type": [], "Guide Price": [], "Bedrooms": [], "Bathrooms": [], "Receptions": []}
    
    # Navigate to first page of list.
    bot = Scraper()
    bot.acceptCookies()
    bot.sendKeysToSearchBar('Cambridge')
    bot.navThroughPages()
    
    
    # soup = BeautifulSoup(html, 'lxml')
    # item = soup.find('',{'class':'issuePanelContainer'})
    # last_item = item.find_all('div')[-1]

    

        # Locate desired data and append data into JSON format { Key: Value[0], Value[1] Value[x] }.
        # Type of property ['flat', 'detached', 'semi-detached', 'terrace', 'terraced', 'maisonette', 'bungalow']
        
        # Guide Price

        # Bedrooms

        # Bathrooms

        # Receptions

