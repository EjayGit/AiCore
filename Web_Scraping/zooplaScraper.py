import time
from selenium import webdriver
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
        except:
            print('No cookies found')

    def lookForSearchBar(self, xpath: str = '/html/body/div/main/div[1]/div[1]/div/div/div/div[2]/div/form/div/div[1]/div/div/div/div/div/div/input'):
        try:
            time.sleep(1)
            search_bar = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
            search_bar.click()
            return search_bar
        except:
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
        pages = self.driver.find_elements(By.XPATH, "//div[@data-testid='pagination']//*[starts-with(@aria-label, 'Page ')]")
        lastPage = int(pages[-1].text)
        return lastPage

    def extractPageData(self):
        propertyList = []
        properties = self.driver.find_elements(By.XPATH, "//div[starts-with(@data-testid, 'search-result_listing_')]")
        print(len(properties))
        for property_listing in properties:
            property_dictionary = dict()
            property_dictionary["Price"] = property_listing.find_element(by=By.XPATH, value=".//p[@class='css-1w7anck ekoq0qp31']").text
            time.sleep(2)
            propertyList.append(property_dictionary)
        print(propertyList)
        return propertyList

    """ def extractPageData(self):
        propertyList = []
        properties = self.driver.find_elements(By.XPATH, "//div[starts-with(@data-testid, 'search-result_listing_')]")
        for property in properties:
            text = property.text.splitlines()
            # Extract data from text.
            # For each element in text
            # Find the guide price then stop.
            for listNum in range(len(text)-1):
                # Check if the first char is "£"
                if "£" in text[listNum]:
                    # If it is, store position of listNum in strPos.
                    strPos = listNum
            propertyList.append()
        return propertyList """
    
    def navThroughPages(self):
        lastPage = self.findPages()
        for page in range(2,lastPage+1):
            # Find and select the page to be scraped.
            try:
                # Find and select the page to be scraped.
                self.extractPageData()
                next_page_button = self.driver.find_element(By.XPATH, '//li[@class="css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"]/a').get_attribute("href")
                self.driver.get(next_page_button)
                print("navigating to the next page...")
                # For each property, locate desired data and append data into JSON format { Key: Value[0], Value[1] Value[x] }.
            except:
                if lastPage + 1:
                    break
            


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

