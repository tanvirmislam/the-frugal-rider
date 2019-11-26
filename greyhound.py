import pandas as pd
import time

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bus_service import BusService
from driver import Driver
from ticket_order import TicketOrder


class Greyhound(BusService):

    def __init__(self, browser_driver: Driver, bus_ticket_order: TicketOrder) -> None:
        # Call superclass constructor
        super().__init__(browser_driver, bus_ticket_order)

        # Full Xpath
        self.departure_city_text_box_xpath = '/html/body/div[3]/main/section[1]/div/div/form/div[1]/div[1]/div[1]/div/input[1]'
        self.departure_city_autocomplete_lists_xpath = '/html/body/div[3]/main/section[1]/div/div/form/div[1]/div[1]/div[1]/div/ul/li[*][@class="ui-menu-item"]'
        self.departure_city_name_xpath_relative_to_list_item = './/div'

        self.arrival_city_text_box_xpath = '/html/body/div[3]/main/section[1]/div/div/form/div[1]/div[1]/div[2]/div/input[1]'
        self.arrival_city_autocomplete_lists_xpath = '/html/body/div[3]/main/section[1]/div/div/form/div[1]/div[1]/div[2]/div/ul/li[*][@class="ui-menu-item"]'
        self.arrival_city_name_xpath_relative_to_list_item = './/div'

        self.depart_date_box_id = 'datepicker-from'
        self.depart_datepicker_calendar_div_id = 'ui-datepicker-div'
        self.depart_datepicker_prev_month_button_xpath_relative_to_calendar_div = './/div/a[1]'
        self.depart_datepicker_next_month_button_xpath_relative_to_calendar_div = './/div/a[2]'
        self.depart_datepicker_month_name_xpath_relative_to_calendar_div = './/div/div/span[1]'
        self.depart_datepicker_year_xpath_relative_to_calendar_div = './/div/div/span[2]'
        self.depart_datepicker_calendar_rows_xpath_relative_to_calendar_div = './/table/tbody/tr[*]'
        self.depart_datepicker_calendar_cells_xpath_relative_to_row = './/td[*][@data-handler="selectDay"][@data-event="click"]'
        self.depart_datepicker_calendar_day_xpath_relative_to_cell = './/a'

        self.depart_date_box_xpath = '/html/body/div[3]/main/section[1]/div/div/form/div[1]/div[2]/div/div/div/div/input'
        self.depart_datepicker_prev_month_button_xpath = '/html/body/div[3]/main/section[1]/div/div/form/div[1]/div[2]/div/div/div/div/div/div/a[1]'
        self.depart_datepicker_next_month_button_xpath = '/html/body/div[3]/main/section[1]/div/div/form/div[1]/div[2]/div/div/div/div/div/div/a[2]'
        self.depart_datepicker_month_name_xpath = '/html/body/div[3]/main/section[1]/div/div/form/div[1]/div[2]/div/div/div/div/div/div/div/span[1]'
        self.depart_datepicker_year_xpath = '/html/body/div[3]/main/section[1]/div/div/form/div[1]/div[2]/div/div/div/div/div/div/div/span[2]'
        self.depart_datepicker_calendar_rows_xpath = '/html/body/div[3]/main/section[1]/div/div/form/div[1]/div[2]/div/div/div/div/div/table/tbody/tr[*]'

        self.submit_button_id = 'fare-search-btn'

        self.no_results_id = 'empty-calendar-message'

        self.result_cities_container_xpath = '/html/body/div[3]/main/section[2]/div/div[3]/div[3]/div[2]/div/div[1]'
        self.result_departure_city_xpath_relative_to_cities_container = 'div[1]/div[2]/div/span[1]'
        self.result_arrival_city_xpath_relative_to_cities_container = 'div[1]/div[2]/div/span[3]'

        self.result_container_class = 'condensed-fare-listing'
        self.trip_container_lists_xpath_relative_to_result_container = 'li[*][@class="fare"][@data-time-to-sell="Sellable"]'

        self.departure_time_xpath_relative_to_trip_container = 'div[1]/div[1]/div[1]/div[1]/div[2]/p[1]'
        self.arrival_time_xpath_relative_to_trip_container = 'div[1]/div[1]/div[1]/div[2]/p'
        self.arrival_day_diff_xpath_relative_to_trip_container = 'div[1]/div[1]/div[1]/div[2]/p/span'

        self.price_xpath_relative_to_trip_container = 'div[1]/div[2]/div[2]/div[1]/div[1]/span[2]'

        '/html/body/div[3]/main/section[2]/div/div[3]/div[3]/div[2]/div/div[2]/div/ul/li[2]'
        '/html/body/div[3]/main/section[2]/div/div[3]/div[3]/div[2]/div/div[2]/div/ul/li[2]/div[1]/div[2]/div[2]/div/div/div/span[1]'
        '/html/body/div[3]/main/section[2]/div/div[3]/div[3]/div[2]/div/div[2]/div/ul/li[3]/div[1]/div[2]/div[2]/div[1]/div[2]/a/span[2]/span'

        # Delay
        self.delay_for_autocomplete_suggestions = 1.0
        self.results_page_load_wait = 0.2

    def set_name(self):
        self.name = 'Greyhound'

    def set_url(self):
        self.home_url = 'https://greyhound.com/en'

    def select_cities(self) -> bool:
        self.display_message('Selecting departure city')

        # Fill departure city text
        departure_city_text_box_element = self.driver.get_element(By.XPATH, self.departure_city_text_box_xpath)
        self.driver.move_to_element(departure_city_text_box_element)
        self.driver.fill_text(departure_city_text_box_element, self.order.departure_city)

        # Wait for suggestions to show up
        time.sleep(self.delay_for_autocomplete_suggestions)

        # Look through the suggestions and click
        departure_city_list_elements = self.driver.get_elements(By.XPATH, self.departure_city_autocomplete_lists_xpath)
        is_departure_city_found = False
        # print('size of departure_city_list_elements: ' + str(len(departure_city_list_elements)))

        for li_element in departure_city_list_elements:
            curr_city = li_element.get_attribute('aria-label')
            # print(curr_city)

            if self.order.departure_city in curr_city:
                self.driver.move_to_element(li_element)
                li_element.click()
                is_departure_city_found = True
                break

        if not is_departure_city_found:
            self.display_message('Unable to find departure city')
            return False

        self.display_message('Selecting arrival city')

        # Fill arrival city text
        arrival_city_text_box_element = self.driver.get_element(By.XPATH, self.arrival_city_text_box_xpath)
        self.driver.move_to_element(arrival_city_text_box_element)
        self.driver.fill_text(arrival_city_text_box_element, self.order.arrival_city)

        # Wait for suggestions to show up
        time.sleep(self.delay_for_autocomplete_suggestions)

        # Look through the suggestions and click
        arrival_city_list_elements = self.driver.get_elements(By.XPATH, self.arrival_city_autocomplete_lists_xpath)
        is_arrival_city_found = False
        # print('size of arrival_city_list_elements: ' + str(len(arrival_city_list_elements)))

        for li_element in arrival_city_list_elements:
            curr_city = li_element.get_attribute('aria-label')
            # print(curr_city)

            if self.order.arrival_city in curr_city:
                self.driver.move_to_element(li_element)
                li_element.click()
                is_arrival_city_found = True
                break

        if not is_arrival_city_found:
            self.display_message('Unable to find arrival city')
            return False

        return True

    def select_dates(self) -> bool:
        self.display_message('Selecting departure date')

        if self.order.departure_date < pd.Timestamp(str(pd.datetime.now().date())):
            self.display_message('Invalid date')
            return False

        # Get Web elements by XPATH
        depart_date_box_element = self.driver.get_element(By.ID, self.depart_date_box_id)

        # Move the date picker into view, and click to expand calender
        self.driver.move_to_element(depart_date_box_element)
        depart_date_box_element.click()

        # Navigate to the right year / month on the calendar
        depart_datepicker_calendar_elem = self.driver.get_element(By.ID, self.depart_datepicker_calendar_div_id)

        depart_datepicker_month_name_elem = self.driver.get_relative_element(depart_datepicker_calendar_elem, By.XPATH, self.depart_datepicker_month_name_xpath_relative_to_calendar_div)
        depart_datepicker_year_elem = self.driver.get_relative_element(depart_datepicker_calendar_elem, By.XPATH, self.depart_datepicker_year_xpath_relative_to_calendar_div)
        depart_datepicker_prev_month_button_elem = self.driver.get_relative_element(depart_datepicker_calendar_elem, By.XPATH, self.depart_datepicker_prev_month_button_xpath_relative_to_calendar_div)
        depart_datepicker_next_month_button_elem = self.driver.get_relative_element(depart_datepicker_calendar_elem, By.XPATH, self.depart_datepicker_next_month_button_xpath_relative_to_calendar_div)
        self.driver.move_to_element(depart_datepicker_month_name_elem)

        is_month_found = False

        while not is_month_found:
            # Read current month and year
            curr_month = depart_datepicker_month_name_elem.get_attribute('innerHTML')
            curr_year = int(depart_datepicker_year_elem.get_attribute('innerHTML'))
            # print(str(curr_month) + ', ' + str(curr_year))

            # Check them against the ticket order
            if self.order.departure_date.month_name() == curr_month and self.order.departure_date.year == curr_year:
                is_month_found = True
            elif curr_year < self.order.departure_date.year:
                depart_datepicker_next_month_button_elem.click()
            elif curr_year > self.order.departure_date.year:
                depart_datepicker_prev_month_button_elem.click()
            elif self.month_abbr_to_num[curr_month.lower()[:3]] < self.month_abbr_to_num[self.order.departure_date.month_name().lower()[:3]]:
                depart_datepicker_next_month_button_elem.click()
            elif self.month_abbr_to_num[curr_month.lower()[:3]] > self.month_abbr_to_num[self.order.departure_date.month_name().lower()[:3]]:
                depart_datepicker_prev_month_button_elem.click()

            # Refresh element to avoid StaleElement error
            depart_datepicker_month_name_elem = self.driver.get_relative_element(depart_datepicker_calendar_elem, By.XPATH, self.depart_datepicker_month_name_xpath_relative_to_calendar_div)
            depart_datepicker_year_elem = self.driver.get_relative_element(depart_datepicker_calendar_elem, By.XPATH, self.depart_datepicker_year_xpath_relative_to_calendar_div)
            depart_datepicker_prev_month_button_elem = self.driver.get_relative_element(depart_datepicker_calendar_elem, By.XPATH, self.depart_datepicker_prev_month_button_xpath_relative_to_calendar_div)
            depart_datepicker_next_month_button_elem = self.driver.get_relative_element(depart_datepicker_calendar_elem, By.XPATH, self.depart_datepicker_next_month_button_xpath_relative_to_calendar_div)

        # Iterate through the dates in the current month to find and click on the ticket order date
        calendar_row_elements = self.driver.get_relative_elements(depart_datepicker_calendar_elem, By.XPATH, self.depart_datepicker_calendar_rows_xpath_relative_to_calendar_div)

        is_date_found = False
        i = 0

        while not is_date_found and i < len(calendar_row_elements):
            # Get the list of date cell elements in the calendar's current row
            calendar_cell_elements = self.driver.get_relative_elements(calendar_row_elements[i], By.XPATH, self.depart_datepicker_calendar_cells_xpath_relative_to_row)
            j = 0

            while not is_date_found and j < len(calendar_cell_elements):
                curr_date = int(self.driver.get_relative_element(calendar_cell_elements[j], By.XPATH, self.depart_datepicker_calendar_day_xpath_relative_to_cell).get_attribute('innerHTML'))
                # print(curr_date)

                if curr_date == self.order.departure_date.day:
                    is_date_found = True
                    self.driver.move_to_element(calendar_cell_elements[j])
                    calendar_cell_elements[j].click()

                j += 1

            i += 1

        self.driver.press_key(Keys.TAB)
        return True

    def submit_search(self) -> bool:
        self.display_message('Submitting search')

        # Get the submit button WebElement
        submit_button_element = self.driver.get_element(By.ID, self.submit_button_id)

        # Move the button into view
        self.driver.move_to_element(submit_button_element)

        # Click
        submit_button_element.click()

        return True

    def collect_data(self) -> bool:
        # If the results are loading, give it some time to finish
        is_results_page_loaded = False
        while not is_results_page_loaded:
            try:
                self.driver.get_element(By.CLASS_NAME, self.result_container_class)
                is_results_page_loaded = True
            except selenium.common.exceptions.NoSuchElementException:
                self.display_message('Results page still loading, waiting for it to finish..')
                time.sleep(self.results_page_load_wait)

        result_cities_container_element = self.driver.get_element(By.XPATH, self.result_cities_container_xpath)
        departure_city = self.driver.get_relative_element(result_cities_container_element, By.XPATH, self.result_departure_city_xpath_relative_to_cities_container).get_attribute('innerHTML')
        arrival_city = self.driver.get_relative_element(result_cities_container_element, By.XPATH, self.result_arrival_city_xpath_relative_to_cities_container).get_attribute('innerHTML')

        result_container_element = self.driver.get_element(By.CLASS_NAME, self.result_container_class)
        trip_container_elements = self.driver.get_relative_elements(result_container_element, By.XPATH, self.trip_container_lists_xpath_relative_to_result_container)

        for trip_element in trip_container_elements:
            # Check if the ticket is buy-able or sold out
            try:
                price_element = self.driver.get_relative_element(trip_element, By.XPATH, self.price_xpath_relative_to_trip_container)
            except selenium.common.exceptions.NoSuchElementException:
                # SOLD OUT
                continue

            price = float(price_element.get_attribute('innerHTML').partition('span>')[2])

            departure_time_element = self.driver.get_relative_element(trip_element, By.XPATH, self.departure_time_xpath_relative_to_trip_container)
            departure_time = departure_time_element.get_attribute('innerHTML').partition('<')[0].strip().upper()

            arrival_time_element = self.driver.get_relative_element(trip_element, By.XPATH, self.arrival_time_xpath_relative_to_trip_container)
            arrival_time = arrival_time_element.get_attribute('innerHTML').partition('<')[0].strip().upper()

            arrival_day_diff_element = self.driver.get_relative_element(trip_element, By.XPATH, self.arrival_day_diff_xpath_relative_to_trip_container)
            arrival_day_diff = arrival_day_diff_element.get_attribute('innerHTML')
            if arrival_day_diff != '':
                arrival_day_diff = arrival_day_diff.partition('(+')[2].partition('days')[0].strip()
                arrival_date = self.order.departure_date + pd.Timedelta(days=int(arrival_day_diff))
            else:
                arrival_date = self.order.departure_date

            self.schedules = self.schedules.append(pd.Series([self.name, self.order.departure_date, departure_time, departure_city,
                                                              arrival_date, arrival_time, arrival_city, price],
                                                             index=self.schedules.columns), ignore_index=True)

        return True
