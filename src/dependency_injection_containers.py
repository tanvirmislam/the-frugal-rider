import dependency_injector.containers as containers
import dependency_injector.providers as providers

from driver import Driver
from ticket_order import TicketOrder
from bus_services.peterpan import Peterpan
from bus_services.greyhound import Greyhound


class DriverContainer(containers.DeclarativeContainer):
    driver_object_factory = providers.Factory(Driver)


class TicketOrderContainer(containers.DeclarativeContainer):
    ticket_order_object_singleton = providers.ThreadSafeSingleton(TicketOrder)


class PeterpanContainer(containers.DeclarativeContainer):
    peterpan_object_singleton = providers.ThreadSafeSingleton(Peterpan, DriverContainer.driver_object_factory, TicketOrderContainer.ticket_order_object_singleton)


class GreyhoundContainer(containers.DeclarativeContainer):
    greyhound_object_singleton = providers.ThreadSafeSingleton(Greyhound, DriverContainer.driver_object_factory, TicketOrderContainer.ticket_order_object_singleton)
