import pandas as pd
import containers
import concurrent.futures
from concurrent import futures
from bus_service import BusService


class ServiceManager:

    def __init__(self):
        self.ticket_order = containers.TicketOrderContainer.ticket_order_object_singleton()
        self.bus_services = [
            containers.PeterpanContainer.peterpan_object_singleton(),
            containers.GreyhoundContainer.greyhound_object_singleton()
        ]
        self.max_threads = 5
        self.__schedules_list = []

    def setup_ticket_order(self, dep_city: str, arr_city: str, dep_date: str) -> bool:
        return self.ticket_order.setup(dep_city, arr_city, dep_date)

    def find_tickets(self):
        if self.ticket_order.status is False:
            print('Error: incomplete order')
            return

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            thread_list = []

            for bus in self.bus_services:
                thread_list.append(executor.submit(self.__find_subroutine, bus))

            (finished, pending) = futures.wait(thread_list, return_when=futures.ALL_COMPLETED)

    def __find_subroutine(self, bus_service_object: BusService):
        # Start session
        bus_service_object.start_session()

        # Search, and scrape if search is successful
        if bus_service_object.search():
            bus_service_object.scrape()

        # End session
        bus_service_object.end_session()

        # Obtain schedules
        self.__schedules_list.append(bus_service_object.schedules)

    def get_bus_service_obj(self, bus_service_name: str):
        for bus in self.bus_services:
            if bus.name.lower() == bus_service_name.lower():
                return bus
        return None

    def get_combined_schedules(self):
        combined_schedule = pd.concat(self.__schedules_list, ignore_index=True)
        combined_schedule.sort_values(by='price', inplace=True)
        return combined_schedule
