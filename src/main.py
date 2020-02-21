from service_manager import ServiceManager


def main() -> None:
    manager = ServiceManager()
    manager.setup_ticket_order('New York', 'Hartford', '2020-02-26')
    manager.find_tickets()

    print(manager.get_combined_schedules())


if __name__ == '__main__':
    main()
