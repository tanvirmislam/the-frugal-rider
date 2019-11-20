import time
import calendar
import threading

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bus_service import BusService
from driver import Driver
from ticket_order import TicketOrder


class Peterpan(BusService):

    def __init__(self, browser_driver: Driver, bus_ticket_order: TicketOrder) -> None:
        # Call superclass constructor
        super().__init__(browser_driver, bus_ticket_order)

        # Full XPATH's of required elements
        self.oneway_radiobutton_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[1]/div[1]/div/div[1]/label/span'
        self.departure_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/input'
        self.departure_cities_list_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/ul/li[*]'
        self.departure_city_clickable_xpath_relative_to_list = './/a'
        self.departure_city_name_xpath_relative_to_list = './/a/span'

        self.arrival_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/input'
        self.arrival_cities_list_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/ul/li[*]'
        self.arrival_city_clickable_xpath_relative_to_list = './/a'
        self.arrival_city_name_xpath_relative_to_list = './/a/span'

        self.date_box_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div[1]/div/input'
        self.submit_button_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[3]/button'

        self.calendar_month_name_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div/div/div[1]/div[2]/div'
        self.calendar_prev_month_button_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/i'
        self.calendar_next_month_button_xpath = '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div/div/div[1]/div[3]/i'
        self.calendar_row_class = 'DayPicker-Week'
        self.calendar_cell_xpath_relative_to_row = './/div[@class="DayPicker-Day"][@aria-disabled="false"]'

        self.delay_for_arrival_city_load = 0.5


    def select_cities(self) -> bool:
        print('\n> Peterpan [' + str(threading.current_thread().name) + ']: Selecting departure city')

        # Get Web elements by XPATH
        departure_element = self.driver.get_element(By.XPATH, self.departure_xpath)
        arrival_element = self.driver.get_element(By.XPATH, self.arrival_xpath)

        # Scroll to departure city box, and click it to expand the list
        self.driver.move_to_element(departure_element)
        departure_element.click()

        # Get the list elements after the drop-down appears
        departure_cities_li_elements = self.driver.get_elements(By.XPATH, self.departure_cities_list_xpath)

        # Iterate the list and select the correct city
        for li_element in departure_cities_li_elements:
            # Get the city name element
            city_name_element = self.driver.get_relative_element(li_element, By.XPATH, self.departure_city_name_xpath_relative_to_list)
            # print(city_name_element.get_attribute('innerHTML'))

            # Check the name and select if found
            if self.order.departure_city in city_name_element.get_attribute('innerHTML'):
                self.driver.move_to_element(city_name_element)
                city_name_element.click()
                break

        print('\n> Peterpan [' + str(threading.current_thread().name) + ']: Selecting arrival city')

        # Scroll to departure city box, and click it to expand the list
        self.driver.move_to_element(arrival_element)
        arrival_element.click()

        # Wait for arrival cities to load based on departure city selection
        time.sleep(self.delay_for_arrival_city_load)

        # Get the list elements after the drop-down appears
        arrival_cities_li_elements = self.driver.get_elements(By.XPATH, self.arrival_cities_list_xpath)

        for li_element in arrival_cities_li_elements:
            # Get the city name element
            city_name_element = self.driver.get_relative_element(li_element, By.XPATH, self.departure_city_name_xpath_relative_to_list)
            # print(city_name_element.get_attribute('innerHTML'))

            # Check the name and select if found
            if self.order.arrival_city in city_name_element.get_attribute('innerHTML'):
                self.driver.move_to_element(city_name_element)
                city_name_element.click()
                break

        return True


    def select_date(self) -> None:
        print('\n> Peterpan [' + str(threading.current_thread().name) + ']: Selecting departure date')

        # Get Web elements by XPATH
        date_box_element = self.driver.get_element(By.XPATH, self.date_box_xpath)

        # Move the date picker into view, and click to expand calender
        self.driver.move_to_element(date_box_element)
        date_box_element.click()

        # Navigate to the right year / month on the calendar
        calendar_month_name_elem = self.driver.get_element(By.XPATH, self.calendar_month_name_xpath)
        calendar_prev_month_button_elem = self.driver.get_element(By.XPATH, self.calendar_prev_month_button_xpath)
        calendar_next_month_button_elem = self.driver.get_element(By.XPATH, self.calendar_next_month_button_xpath)

        self.driver.move_to_element(calendar_month_name_elem)

        # month name (abbreviated) to month number conversion dict
        month_abbr_to_num = {name.lower(): num for (num, name) in list(enumerate(calendar.month_abbr)) if num}

        is_month_found = False

        while not is_month_found:
            # Read current month and year
            curr_month_and_year = calendar_month_name_elem.get_attribute('innerHTML')
            # print(curr_month_and_year)

            # Separate out month and year name
            [curr_month, curr_year] = curr_month_and_year.split(' ')
            curr_year = int(curr_year)

            # Check them against the ticket order
            if self.order.departure_date.month_name() == curr_month and self.order.departure_date.year == curr_year:
                is_month_found = True
            elif curr_year < self.order.departure_date.year:
                calendar_next_month_button_elem.click()
            elif curr_year > self.order.departure_date.year:
                calendar_prev_month_button_elem.click()
            elif month_abbr_to_num[curr_month.lower()[:3]] < month_abbr_to_num[self.order.departure_date.month_name().lower()[:3]]:
                calendar_next_month_button_elem.click()
            elif month_abbr_to_num[curr_month.lower()[:3]] > month_abbr_to_num[self.order.departure_date.month_name().lower()[:3]]:
                calendar_prev_month_button_elem.click()


        # Iterate through the dates in the current month to find and click on the ticket order date
        calendar_row_elements = self.driver.get_elements(By.CLASS_NAME, self.calendar_row_class)

        is_date_found = False
        i = 0

        while not is_date_found and i < len(calendar_row_elements):
            # Get the list of date cell elements in the calendar's current row
            calendar_cell_elements = self.driver.get_relative_elements(calendar_row_elements[i], By.XPATH, self.calendar_cell_xpath_relative_to_row)
            j = 0

            while not is_date_found and j < len(calendar_cell_elements):
                curr_date = int(calendar_cell_elements[j].get_attribute('innerHTML'))
                # print(curr_date)

                if curr_date == self.order.departure_date.day:
                    is_date_found = True
                    self.driver.move_to_element(calendar_cell_elements[j])
                    calendar_cell_elements[j].click()

                j += 1

            i += 1

        self.driver.press_key(Keys.TAB)

    def submit_search(self) -> None:
        print('\n> Peterpan [' + str(threading.current_thread().name) + ']: Submitting search')

        # Get the submit button WebElement
        submit_button_element = self.driver.get_element(By.XPATH, self.submit_button_xpath)

        # Move the button into view
        self.driver.move_to_element(submit_button_element)

        # Click
        submit_button_element.click()


    def search(self) -> bool:
        # If session has not been started, return False
        if not self.is_session_running:
            print('Error: session is not running')
            return False

        try:
            # Make selections
            self.select_cities()
            self.select_date()
            self.submit_search()
            time.sleep(10)
            return True

        except Driver.failure_exceptions as e:
            Driver.print_failure(e)
            return False

    def scrape(self):
        pass


    def set_name(self):
        self.name = 'peterpan'


    def set_url(self):
        self.url = 'https://peterpanbus.com/'
