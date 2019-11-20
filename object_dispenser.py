import dependency_injector
import containers
from bus_service import BusService


class ObjectDispenser(object):

    @staticmethod
    def get_driver_object() -> dependency_injector.providers.Factory:
        return containers.DriverContainer.driver_object_factory()

    @staticmethod
    def get_ticket_order_object() -> dependency_injector.providers.ThreadSafeSingleton:
        return containers.TicketOrderContainer.ticket_order_object_singleton()

    @staticmethod
    def get_peterpan_object() -> dependency_injector.providers.ThreadSafeSingleton:
        return containers.PeterpanContainer.peterpan_object_singleton()

    @staticmethod
    def get_greyhound_object() -> dependency_injector.providers.ThreadSafeSingleton:
        return containers.GreyhoundContainer.greyhound_object_singleton()


    @staticmethod
    def get_bus_service_object(bus_service_name: str) -> dependency_injector.providers.ThreadSafeSingleton:
        if bus_service_name.lower() == 'peterpan':
            return ObjectDispenser.get_peterpan_object()
        elif bus_service_name.lower() == 'greyhound':
            return ObjectDispenser.get_greyhound_object()
        else:
            return None
