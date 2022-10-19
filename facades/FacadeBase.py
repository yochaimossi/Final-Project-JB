from abc import ABC, abstractmethod
from datetime import datetime
from Flight import Flight
from DbRepo import DbRepo
from db_config import local_session
from Airline_Company import Airline_Company
from Country import Country
from User import User
from User_Role import User_Role
from sqlalchemy import extract
from Logger import Logger
from LoginToken import LoginToken


class FacadeBase(ABC):

    @abstractmethod
    def __init__(self):
        self.logger = Logger.get_instance()
        self.repo = DbRepo(local_session)
        self.login_token = LoginToken(id_=None, name='Anonymous', role='Anonymous')

    def get_all_flights(self):
        return self.repo.get_all(Flight)

    def get_flight_by_id(self, id_):
        if not isinstance(id_, int):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get flights by ID because the ID "{id_}" is not in the correct format.')
            return
        if id_ <= 0:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get flights by ID because the ID "{id_}" is not in the correct format.')
            return
        return self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.id == id_).all())

    def get_flights_by_airline_id(self, airline_id):
        if not isinstance(airline_id, int):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get flights by airline ID because the airline ID'
                f'"{airline_id}" is not in the correct format.')
            return
        if airline_id <= 0:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get flights by airline ID because the airline ID'
                f'"{airline_id}" is not in the correct format.')
            return
        air_line_ = self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.id == airline_id).all())
        if not air_line_:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get flights by airline ID because the airline ID'
                f'"{airline_id}" does not exists in the database.')
            return
        return self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.airline_company_id == airline_id).all())

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        if not isinstance(origin_country_id, int) or not isinstance(destination_country_id, int):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get flights by parameters because the origin county ID '
                f'"{origin_country_id}" and destination country ID "{destination_country_id}" '
                f'are not in the correct format')
            return
        if origin_country_id <= 0 or destination_country_id <= 0:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get flights by parameters because the origin county ID '
                f'"{origin_country_id}" and destination country ID "{destination_country_id}" '
                f'are not in the correct format')
            return
        if not isinstance(date, datetime):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get flights by parameters because the date '
                f'"{date}" that was sent must be a Datetime object')
            return
        return self.repo.get_by_condition(Flight,
                                          lambda query: query.filter(Flight.origin_country_id == origin_country_id,
                                                                     Flight.destination_country_id == destination_country_id,
                                                                     extract('year', Flight.departure_time) == date.year,
                                                                     extract('month', Flight.departure_time) == date.month,
                                                                     extract('day', Flight.departure_time) == date.day).all())

    def get_all_airlines(self):
        return self.repo.get_all(Airline_Company)

    def get_airline_by_id(self, id_):
        if not isinstance(id_, int):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get an airline by ID because the ID "{id_}" '
                f'is not in the correct format.')
            return
        if id_ <= 0:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get an airline by ID because the ID "{id_}" '
                f'is not in the correct format.')
            return
        return self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.id == id_).all())

    def create_user(self, user):
        if not isinstance(user, User):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to create a user because the user "{user}" '
                f'that was sent must be instance if the class User.')
            return
        if self.repo.get_by_condition(User, lambda query: query.filter(User.username == user.username).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to create a user because username '
                f'"{user.username}" already exists in the database.')
            return
        if self.repo.get_by_condition(User, lambda query: query.filter(User.email == user.email).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to create a user because the email "{user.email}" '
                f'already exists in the database.')
            return
        if not self.repo.get_by_condition(User_Role, lambda query: query.filter(User_Role.id == user.user_role).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to create a user because the user role '
                f'"{user.user_role}" does not exist in the database.')
            return
        user.id = None
        self.logger.logger.debug(f'You successfully used login token "{self.login_token}" to create a user and new user'
                                 f'"{user}" has ben added to the database.')
        self.repo.add(user)
        return True

    def get_all_countries(self):
        return self.repo.get_all(Country)

    def get_country_by_id(self, id_):
        if not isinstance(id_, int):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get country by ID because the ID "{id_}" is not in the correct format.')
            return
        if id_ <= 0:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get country by ID because the ID "{id_}" is not in the correct format.')
            return
        return self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == id_).all())

