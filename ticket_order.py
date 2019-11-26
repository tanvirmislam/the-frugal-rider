import pandas as pd
import traceback


class TicketOrder(object):

    def __init__(self):
        self.departure_city = None
        self.arrival_city = None
        self.departure_date = None
        self.status = False

    def setup(self, dep: str, arr: str, dep_date: str) -> bool:
        try:
            self.departure_date = pd.Timestamp(dep_date)
            self.departure_city = dep
            self.arrival_city = arr
            self.status = True
            return True
        except ValueError:
            print(
                '\n==========================\n'
                'Error: Invalid date input\n'
                'Correct format: YYYY-MM-DD'
                '\n==========================\n'
            )
            return False
