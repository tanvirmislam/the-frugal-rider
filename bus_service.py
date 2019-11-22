import time
import threading
import pandas as pd
from abc import ABCMeta, abstractmethod
from driver import Driver
from ticket_order import TicketOrder


class BusService(metaclass=ABCMeta):

    def __init__(self, browser_driver: Driver, bus_ticket_order: TicketOrder) -> None:
        # Initialize variables
        self.name = None
        self.home_url = None
        self.is_session_running = False
        self.is_search_completed = False
        self.driver = browser_driver
        self.order = bus_ticket_order

        # Dataframes
        self.list_of_schedules = []
        self.columns = ['bus_service', 'departure_date', 'departure_time', 'departure_city', 'arrival_date', 'arrival_time', 'arrival_city', 'price']

        # Call function implemented by child classes
        self.set_name()
        self.set_url()

    def __str__(self):
        result =                                                                                                    \
            '\n-----------------------------------------------------------------------------------------------\n' + \
            '> ' + self.name +                                                                                      \
            ' [' + str(threading.current_thread().name) + '] Results: ' +                                           \
            '\n-----------------------------------------------------------------------------------------------\n' + \
            (self.get_combined_schedule()).to_string() +                                                                            \
            '\n-----------------------------------------------------------------------------------------------'

        return result

    @abstractmethod
    def set_name(self) -> None:
        pass

    @abstractmethod
    def set_url(self) -> None:
        pass

    @abstractmethod
    def select_cities(self) -> bool:
        pass

    @abstractmethod
    def select_dates(self) -> bool:
        pass

    @abstractmethod
    def submit_search(self) -> bool:
        pass

    @abstractmethod
    def collect_data(self) -> bool:
        pass

    def search(self) -> bool:
        # If session has not been started, return False
        if not self.is_session_running:
            print('Error: session is not running')
            return False

        try:
            # Select cities (implemented by child class)
            if not self.select_cities():
                return False

            # Select dates (implemented by child class)
            if not self.select_dates():
                return False

            # Submit search and wait till results appear
            old_html_element = self.driver.get_html_element()
            self.submit_search()  # implemented by child class
            self.driver.wait_till_page_load(old_html_element)

            self.is_search_completed = True
            return True

        except Driver.failure_exceptions as e:
            Driver.print_failure(e)
            self.is_search_completed = False
            return False

    def scrape(self) -> bool:
        # If session has not been started, return False
        if not self.is_session_running:
            print('Error: session is not running')
            return False
        # Else if the search is not completed, there is nothing to scrape
        elif not self.is_search_completed:
            print('Error: unable to scrape because of incomplete search')
            return False

        try:
            # Collect data (implemented by child class)
            if not self.collect_data():
                return False

            return True

        except Driver.failure_exceptions as e:
            Driver.print_failure(e)
            return False

    def setup_ticket_order(self, dep_city: str, arr_city: str, dep_date: str) -> bool:
        return self.order.setup(dep_city, arr_city, dep_date)

    def start_session(self, is_headless: bool = False, width: int = 1920, height: int = 1080):
        self.driver.init_driver(is_headless, width, height)
        self.is_session_running = True
        self.driver.get_url(self.home_url)

    def end_session(self):
        self.driver.quit()
        self.is_session_running = False

    def display_message(self, msg: str) -> None:
        full_msg = '\n> ' + self.name + ' [' + str(threading.current_thread().name) + ']: ' + msg
        print(full_msg)

    def get_combined_schedule(self) -> pd.DataFrame:
        if len(self.list_of_schedules) == 0:
            return pd.DataFrame(columns=self.columns)

        combined_df = pd.concat(self.list_of_schedules)
        combined_df.sort_values(by='price', inplace=True)
        return combined_df
