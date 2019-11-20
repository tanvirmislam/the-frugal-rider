import pandas as pd
from abc import ABCMeta, abstractmethod
from driver import Driver
from ticket_order import TicketOrder


class BusService(metaclass=ABCMeta):

    def __init__(self, browser_driver: Driver, bus_ticket_order: TicketOrder) -> None:
        # Initialize variables
        self.name = None
        self.url = None
        self.is_session_running = False
        self.driver = browser_driver
        self.order = bus_ticket_order
        self.schedule_df = pd.DataFrame(columns=['date', 'departure time', 'arrival time'])

        # Call function implemented by child classes
        self.set_name()
        self.set_url()


    @abstractmethod
    def search(self) -> bool:
        pass

    @abstractmethod
    def scrape(self) -> None:
        pass

    @abstractmethod
    def set_name(self) -> None:
        pass

    @abstractmethod
    def set_url(self) -> None:
        pass

    def setup_ticket_order(self, dep_city: str, arr_city: str, dep_date: str) -> bool:
        return self.order.setup(dep_city, arr_city, dep_date)

    def start_session(self, is_headless: bool = False, width: int = 1920, height: int = 1080):
        self.driver.init_driver(is_headless, width, height)
        self.is_session_running = True
        self.driver.get_url(self.url)

    def end_session(self):
        self.driver.quit()
        self.is_session_running = False

