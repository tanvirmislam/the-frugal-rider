import platform
import sys
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from pathlib import Path


def get_driver(headless: bool = True, width :int = 1440, height: int = 900) -> webdriver:
    """
    :param headless: True if running in headless mode, False otherwise
    :param width: Chrome window width
    :param height: Chrome window height
    :return: Webdriver.Chrome instance when successful, None if error occurs
    """
    
    # ------------------------------------------------------------------
    # Detect system and locate appropriate chromedriver executable file
    # ------------------------------------------------------------------
    system_switcher = {
        'darwin': 'mac',
        'windows': 'windows',
        'linux': 'linux'
    }

    system_name = system_switcher.get(platform.system().lower(), None)
    if system_name is None:
        print('Invalid platform')
        return None

    version = '77'
    driver_file_name = system_name + '_chromedriver_' + version
    exec_path = Path.cwd() / 'chromedriver/' / driver_file_name

    if (not exec_path.exists()) or (not exec_path.is_file()):
        print('Chromedriver file not found')
        return None

    # -------------------
    # Set driver options
    # -------------------
    options = Options()
    if headless:
        options.headless = True
    else:
        options.headless = False
        options.add_argument("--kiosk")
        # options.add_argument("--start-maximized")
    
    # ----------------------------------
    # Create and return driver instance
    # ----------------------------------
    try:
        driver = webdriver.Chrome(options=options, executable_path=str(exec_path))
        if headless is True:
            driver.set_window_size(1440, 900)
        return driver
    except selenium.common.exceptions.WebDriverException:
        print('Incompatible chromedriver')
        return None


def fill_input_element(elem, fill_text):
    elem.click()
    elem.clear()
    elem.send_keys(fill_text)
    elem.send_keys(Keys.TAB)


def month_to_num(month):
    convertion_dict = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }

    return convertion_dict.get(month.lower()[:3], None)


def peter_pan(driver: webdriver) -> None:
    departure_city = 'Hartford, CT'
    arrival_city = 'New York (Port Authority), NY'
    departure_month = 'January'
    departure_day = '30'
    departure_year = '2020'
    departure_date = departure_month[:3] + ' ' + departure_day + ' ' + departure_year

    url = 'https://peterpanbus.com/'

    departure_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/input'
    departure_cities_list_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/ul/li[*]'
    departure_city_clickable_xpath_relative_to_list = './/a'
    departure_city_name_xpath_relative_to_list = './/a/span'
    
    arrival_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/input'    
    arrival_cities_list_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/ul/li[*]'
    arrival_city_clickable_xpath_relative_to_list = './/a'
    arrival_city_name_xpath_relative_to_list = './/a/span'

    date_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div[1]/div/input'
    submit_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[3]/button'
    
    calendar_month_name_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div/div/div[1]/div[2]/div'
    calendar_prev_month_button_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/i'
    calendar_next_month_button_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div/div/div[1]/div[3]/i'
    calendar_row_class = 'DayPicker-Week'
    calendar_cell_xpath_realtive_to_row = './/div[@class="DayPicker-Day"][@aria-disabled="false"]'

    print('Getting url: ' + url)
    driver.get(url)

    departure_elem = driver.find_element(By.XPATH, departure_xpath)
    arrival_elem = driver.find_element(By.XPATH, arrival_xpath)
    date_elem = driver.find_element(By.XPATH, date_xpath)
    submit_elem = driver.find_element(By.XPATH, submit_xpath)
    
    print('Selecting departure city as: ' + departure_city)
    departure_elem.click()
    departure_cities_li_elems = driver.find_elements(By.XPATH, departure_cities_list_xpath)
    for elem in departure_cities_li_elems:
        city_click_elem = elem.find_element(By.XPATH, departure_city_clickable_xpath_relative_to_list)
        city_name_elem = elem.find_element(By.XPATH, departure_city_name_xpath_relative_to_list)
        print(city_name_elem.get_attribute('innerHTML'))

        if city_name_elem.get_attribute('innerHTML') == departure_city:
            actions = ActionChains(driver)
            actions.move_to_element(city_name_elem).perform()
            actions.reset_actions()
            city_click_elem.click()
            break

    # fill_input_element(departure_elem, departure_city)

    print('Selecting arrival city as: ' + arrival_city)
    actions = ActionChains(driver)
    actions.move_to_element(arrival_elem).perform()
    actions.reset_actions()

    arrival_elem.click()
    arrival_cities_li_elems = driver.find_elements(By.XPATH, arrival_cities_list_xpath)
    print(len(arrival_cities_li_elems))
    for elem in arrival_cities_li_elems:
        city_click_elem = elem.find_element(By.XPATH, arrival_city_clickable_xpath_relative_to_list)
        city_name_elem = elem.find_element(By.XPATH, arrival_city_name_xpath_relative_to_list)
        print(city_name_elem.get_attribute('innerHTML'))

        if city_name_elem.get_attribute('innerHTML') == arrival_city:
            actions = ActionChains(driver)
            actions.move_to_element(city_name_elem).perform()
            actions.reset_actions()
            city_click_elem.click()
            break

    # fill_input_element(arrival_elem, arrival_city)

    print('Filling up date: ' + departure_date)
    date_elem.click()

    # Navigate to the right month on the calendar
    calendar_month_name_elem = driver.find_element(By.XPATH, calendar_month_name_xpath)
    calendar_prev_month_button_elem = driver.find_element(By.XPATH, calendar_prev_month_button_xpath)
    calendar_next_month_button_elem = driver.find_element(By.XPATH, calendar_next_month_button_xpath)
    
    is_month_found = False

    while not is_month_found:
        curr_month_and_year = calendar_month_name_elem.get_attribute('innerHTML')
        print(curr_month_and_year)
        [curr_month, curr_year] = curr_month_and_year.split(' ')

        if departure_month == curr_month and departure_year == curr_year:
            is_month_found = True
        elif int(curr_year) < int(departure_year):
            calendar_next_month_button_elem.click()
        elif int(curr_year) > int(departure_year):
            calendar_prev_month_button_elem.click()
        elif month_to_num(curr_month) < month_to_num(departure_month):
            calendar_next_month_button_elem.click()
        elif month_to_num(curr_month) > month_to_num(departure_month):
            calendar_prev_month_button_elem.click()
    
    calendar_row_elems = driver.find_elements(By.CLASS_NAME, calendar_row_class)
    is_date_found = False
    i = 0

    while not is_date_found and i < len(calendar_row_elems):
        calendar_cell_elems = calendar_row_elems[i].find_elements(By.XPATH, calendar_cell_xpath_realtive_to_row)
        j = 0

        while not is_date_found and j < len(calendar_cell_elems):
            curr_date = calendar_cell_elems[j].get_attribute('aria-label')
            print(curr_date)

            if curr_date.find(departure_date) != -1:
                is_date_found = True
                calendar_cell_elems[j].click()
            
            j += 1

        i += 1

    print('Clicking submit button')
    submit_elem.click()


def main() -> None:
    driver = get_driver(headless=False)

    if driver is None:
        sys.exit(1)

    peter_pan(driver)

    user_choice = input('Please click ENTER button to close application')
    if not user_choice:
        driver.quit()


if __name__ == '__main__':
    main()
