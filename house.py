from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import json
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

CHROME_PATH = os.getenv("CHROME_PATH")

ser = Service(CHROME_PATH)

chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=ser, options=chrome_options)

def login():
    """
    Logs into housing connect with the credentials given in environment variables

    Pre: webdriver is properly instantiated globally
    Post: webdriver will be logged in
    
    Example of Usage: login()
    """

    URL = "https://a806-housingconnectapi.nyc.gov/id4/account/login?returnUrl=%2Fid4%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Did_token%2520token%26client_id%3Dpublicweb%26state%3Daf6QSTjaGSHN1WXz9M3KMViRDjEJk1sSV8lR5Hin;%252Fsome-state;p1%253D1;p2%253D2%26redirect_uri%3Dhttps%253A%252F%252Fhousingconnect.nyc.gov%252FPublicWeb%252F%26scope%3Dopenid%2520profile%2520email%2520usermanagementapi%2520publicapi%26nonce%3Daf6QSTjaGSHN1WXz9M3KMViRDjEJk1sSV8lR5Hin"

    driver.get(URL)
    username = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID,"Username"))
    )
    password = driver.find_element(By.ID,"Password")

    username.send_keys(os.getenv("USERNAME"))
    password.send_keys(os.getenv("PASSWORD"))

    login = driver.find_element(By.ID,"loginBtn")

    login.click()
    # time.sleep(5)
    login = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(("xpath", "//button[@class='btn btn-light margin-left-20 shadow-2 hoverable']"))
    )

    login.click()

    time.sleep(3)

def apply(lotteryID):
    """
    Applys to a given lottery

    Parameters:
        lotteryID : string (ex: "1234") 
    
    Pre:
        webdriver is properly instantiated 
        login() has been called and user is successfully logged in

    Post:
        user applications will be updated
        user will receive a confirmation email

    Example of Usage: 
        apply("1234")
    
    """
    URL = "https://housingconnect.nyc.gov/PublicWeb/details/"+lotteryID

    driver.get(URL)

    time.sleep(3)

    apply = driver.find_element(By.ID, "apply-section")

    apply.click()

    time.sleep(2)

    terms_and_conditions = driver.find_element("xpath","//div[@class='mat-checkbox-inner-container']")

    terms_and_conditions.click()
    time.sleep(2)

    submit = driver.find_element('xpath',"//button[@class='btn btn-primary m-btn--pill']")

    submit.click()
    
    time.sleep(3)

##################################################
#  -Moves to next page- NO LONGER NEEDED
# 
# 
# 
##################################################

# URL = "https://housingconnect.nyc.gov/PublicWeb/search-lotteries"
# driver.get(URL)

# try:
#     elem = WebDriverWait(driver, 30).until(
#     EC.presence_of_element_located(("xpath", "//li[@class='pagination-next ng-star-inserted']")) #This is a dummy element
#     )
# except:
#     driver.quit()

# try:
#     nextPage = driver.find_element("xpath","//li[@class='pagination-next ng-star-inserted']")
#     nextPage.click()
# except:
#     driver.quit()

# time.sleep(50)

##################################################
#  gets lotteries
# 
# 
# 
##################################################

def getLotteries():
    """
    Will return all currently open rental lotteries filtered by parameters in environment variables

    returns:
        a list of ints representing lottery ids (Ex: [3709, 3636, 3541, 3663, 3573, 3599, 3546, 2926, 3452])
    
    Example of Usage:
        getLotteries()
    """

    searchAPI = "https://a806-housingconnectapi.nyc.gov/HPDPublicAPI/api/Lottery/SearchLotteries"

    data = {
    "UnitTypes": [
        1,
        2
    ],
    "NearbyPlaces": [],
    "NearbySubways": [],
    "Amenities": [],
    "Boroughs": [],
    "Neighborhoods": [],
    "HouseholdSize": os.getenv("HOUSEHOLD"),
    "Income": os.getenv("INCOME"),
    "HouseholdType": 1,
    "OwnerTypes": [],
    }

    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding" : "gzip, deflate, br",
        "Access-Control-Request-Headers": "content-type",
        "Accept" :  "application/json; text/plain; */*",
        "Content-Type": "application/json"
    }

    response = requests.post(searchAPI, headers=headers, json=data).json()['rentals']

    lotteryIDs = [i['lotteryId'] for i in response]

    print(lotteryIDs)

    return lotteryIDs

# print(lotteryIDs)

# lotteryURL = "https://housingconnect.nyc.gov/PublicWeb/details/"

def getApplications():
    """
    Gets all already completed applications

    Pre: 
        webdriver is properly globally instantiated
        login() has been called and user is successfully logged in

    Return:
        A list of ints representing all applications to which the user has already applied
        Ex: [3709, 3636, 3541, 3663, 3573, 3599, 3546, 2926, 3452]

    Example of Usage:
        getApplications()
    """
    return [3709, 3636, 3541, 3663, 3573, 3599, 3546, 2926, 3452]

def applyAll(need_to_apply):
    """
    Applies to all applications in a list
    
    Parameters:
        need_to_apply : list[strings] (ex: ["1234","2345","1369"]) 
    
    Pre:
        webdriver is properly instantiated 
        login() has been called and user is successfully logged in

    Post:
        user applications will be updated
        user will receive a confirmation email for each submitted application

    Example of Usage: 
        applyAll(["1234","2345","1369"])

    """
    for i in need_to_apply:
        apply(str(i))

def main():
    login()
    currentLotteryIDS = getLotteries()
    currentApps = getApplications()

    need_to_apply = list(set(currentLotteryIDS) - set(currentApps))

    applyAll(need_to_apply)

if __name__ == "__main__":
    main()
