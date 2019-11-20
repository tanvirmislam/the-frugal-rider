import threading
import concurrent.futures
from concurrent import futures
from concurrent.futures.thread import ThreadPoolExecutor
from bus_service import BusService
from object_dispenser import ObjectDispenser


def find_tickets(bus_service_name: str, departure_city: str, arrival_city: str, departure_date: str) -> None:
    # Get the correct object
    bus_service_object = ObjectDispenser.get_bus_service_object(bus_service_name)

    if bus_service_object is None:
        print('Fatal error: unable to get ' + bus_service_name + ' object')
        return

    # Initiate ticket order
    bus_service_object.setup_ticket_order(departure_city, arrival_city, departure_date)

    # Start session
    bus_service_object.start_session()

    # Search and scrape
    bus_service_object.search()
    bus_service_object.scrape()

    # End session
    bus_service_object.end_session()
    print('\nWorker ' + str(threading.current_thread().name) + ' signing out.')


def main() -> None:
    # find_tickets('Peterpan', 'New York', 'Hartford', '2020-02-15')

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        search_1 = executor.submit(find_tickets, 'Peterpan', 'New York', 'Hartford', '2020-02-15')
        search_2 = executor.submit(find_tickets, 'Greyhound', 'New York', 'Hartford', '2020-02-15')

        thread_list = [search_1, search_2]

        (finished, pending) = futures.wait(thread_list, return_when=futures.ALL_COMPLETED)


if __name__ == '__main__':
    main()
