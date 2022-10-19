from abc import ABC, abstractmethod
from data_access_objects.DbRepoPool import DbRepoPool
from logger.Logger import Logger


class BaseDbDataGen(ABC):

    @abstractmethod
    def __init__(self):
        self.repool = DbRepoPool.get_instance()
        self.repo = self.repool.get_connection()
        self.logger = Logger.get_instance()

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def generate_countries(self):
        pass

    @abstractmethod
    def generate_user_roles(self):
        pass

    @abstractmethod
    def create_user(self, j_son, user_role):
        pass

    @abstractmethod
    def generate_admin(self):
        pass

    @abstractmethod
    def generate_customers(self, num):
        pass

    @abstractmethod
    def generate_airline_companies(self, num):
        pass

    @abstractmethod
    def generate_flights_per_company(self, num):
        pass

    @abstractmethod
    def generate_tickets_per_customer(self, num):
        pass
