import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def get_driver() -> webdriver:
    options = Options()
    options.add_argument("start-maximized");
    # options.headless = True

    return webdriver.Chrome(options=options)


def fill_input_element(elem, fill_text):
    elem.click()
    elem.clear()
    elem.send_keys(fill_text)
    elem.send_keys(Keys.TAB)


def peter_pan(driver: webdriver) -> None:
    url = 'https://peterpanbus.com/'

    departure_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/input'
    arrival_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/input'
    date_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div[1]/div/input'
    submit_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[3]/button'
    calendar_row_container_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[3]'

    print('Getting url: ' + url)
    driver.get(url)

    departure_elem = driver.find_element(By.XPATH, departure_xpath)
    arrival_elem = driver.find_element(By.XPATH, arrival_xpath)
    date_elem = driver.find_element(By.XPATH, date_xpath)
    submit_elem = driver.find_element(By.XPATH, submit_xpath)

    departure_city = 'Hartford, CT'
    arrival_city = 'New York (Port Authority), NY'
    departure_date = 'Nov 25 2019'

    print('Selecting departure city as: ' + departure_city)
    fill_input_element(departure_elem, departure_city)

    print('Selecting arrival city as: ' + arrival_city)
    fill_input_element(arrival_elem, arrival_city)

    print('Filling up date: ' + departure_date)
    date_elem.click()
    date_elem.clear()

    calendar_rows = driver.find_elements(By.CLASS_NAME, 'DayPicker-Week')
    is_found = False

    for row in calendar_rows:
        calendar_cells = driver.find_elements(By.XPATH, './/div[@class="DayPicker-Day"][@aria-disabled="false"]')

        for elem in calendar_cells:
            date_str = elem.get_attribute('aria-label')
            print(date_str)

            if date_str.find(departure_date) != -1:
                elem.click()
                is_found = True

            if is_found:
                break

        if is_found:
            break

    print('Clicking submit button')
    submit_elem.click()



def main() -> None:
    driver = get_driver()

    peter_pan(driver)

    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    
    # soup = BeautifulSoup(response.text)
    # print(soup.prettify())

    user_choice = input('Please click ENTER button to close application')
    if not user_choice:
        print("ABORTED")
        quit()


    
if __name__ == '__main__':
    main()
