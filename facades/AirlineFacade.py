from FacadeBase import FacadeBase
from Flight import Flight
from Airline_Company import Airline_Company
from Country import Country
from datetime import datetime, timedelta
from NotLegalFlightTimesError import NotLegalFlightTimesError


class AirlineFacade(FacadeBase):

    def __init__(self, login_token):
        super().__init__()
        self.login_token = login_token

    def get_airline_flights(self):
        if self.login_token.role != 'Airline_Company':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get airline flights because your user role is not an airline.')
            return
        return self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.airline_company_id == self.login_token.id).all())

    def add_flight(self, flight):
        if self.login_token.role != 'Airline_Company':
            self.logger.logger.error(
                 f'You cannot use the token "{self.login_token}" to add flights because your user role is not an airline.')
            return
        if not isinstance(flight, Flight):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add flights because the flight "{flight}" is not a Flight object.')
            return
        if not self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == flight.origin_country_id).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add flights because the the origin country ID "{flight.origin_country_id}"'
                f'does not exists in the database.')
            return
        if not self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == flight.destination_country_id).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add flights because the the destination country ID "{flight.destination_country_id}"'
                f'does not exists in the database.')
            return
        if not isinstance(flight.departure_time, datetime) or not isinstance(flight.landing_time, datetime):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add flights because both departure time "{flight.departure_time}" '
                f'and landing time "{flight.landing_time}" must be datetime objects.')
            return
        if flight.departure_time + timedelta(minutes=1) > flight.landing_time:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add flights because '
                f'the time difference between departure time "{flight.departure_time}" and landing time "{flight.landing_time}" '
                f'is less than one minute.')
            raise NotLegalFlightTimesError
        if not isinstance(flight.remaining_tickets, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but the remaining_tickets'
                f' "{flight.remaining_tickets}" that was sent is not an integer.')
            return
        if flight.remaining_tickets < 1:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add flights because the remaining tickets'
                f' "{flight.remaining_tickets}" must be at least 1.')
            return
        flight.id = None
        flight.airline_company_id = self.login_token.id
        self.logger.logger.debug(
            f'You successfully used login token "{self.login_token}" to add the flight "{flight}" to the database.')
        self.repo.add(flight)
        return True

    def remove_flight(self, flight_id):
        if self.login_token.role != 'Airline_Company':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove a flight because your role is not an airline company.')
            return
        if not isinstance(flight_id, int):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove a flight because the flight ID "{flight_id}" '
                f'is not in the correct format.')
            return

        flight = self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.id == flight_id).all())
        if not flight:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove a flight because the flight ID "{flight_id}" '
                f'does not exists in the database.')
            return
        if self.login_token.id != flight[0].airline_company_id:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove a flight because the flight "{flight}" '
                f'does not belong to the login token airline company.')
            return
        self.logger.logger.debug(
             f'You successfully used login token "{self.login_token}" to remove the flight "{flight}" '
            f'from the database.')
        self.repo.delete_by_id(Flight, Flight.id, flight_id)
        return True

    def update_airline(self, airline):
        if self.login_token.role != 'Airline_Company':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update an airline because your role is not an Airline Company.')
            return
        if not isinstance(airline, Airline_Company):
            self.logger.logger.error(
                 f'You cannot use the token "{self.login_token}" to update an airline because the airline "{airline}" '
                f'is not an Airline Company object.')
            return
        airline_ = self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.id == self.login_token.id).all())
        if not airline_:
            self.logger.logger.error(
                 f'You cannot use the token "{self.login_token}" to update an airline because the airline "{airline}" '
                f' does not exists in the database.')
            return
        if self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.name == airline.name).all())\
                and self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.name == airline.name).all()) != airline_:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update an airline because the airline name "{airline.name}" '
                f'already exists in the database.')
            return
        if not self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == airline.country_id).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update an airline because the country ID "{airline.country_id}" '
                f'does not exists in the database.')
            return
        self.logger.logger.debug(
            f'You successfully used login token "{self.login_token}" to update airline "{airline}"')
        self.repo.update_by_id(Airline_Company, Airline_Company.id, self.login_token.id, {Airline_Company.name: airline.name,
                                                                                 Airline_Company.country_id: airline.country_id})
        return True

    def update_flight(self, flight):
        if self.login_token.role != 'Airline_Company':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a flight because your role is not an Airline Company.')
            return
        if not isinstance(flight, Flight):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a flight because the flight "{flight}" '
                f'is not a Flight object.')
            return
        if not isinstance(flight.id, int):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a flight because the flight ID "{flight.id}" '
                f'is not in correct format.')
            return
        flight_ = self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.id == flight.id).all())
        if not flight_:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a flight because the flight ID "{flight.id}" '
                f'does not exists in the database.')
            return
        if flight_[0].airline_company_id != self.login_token.id:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a flight because the flight with the flight ID "{flight.id}" '
                f'does not belong to the login token Airline Company.')
            return
        if not isinstance(flight.origin_country_id, int) or not isinstance(flight.destination_country_id, int):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a flight because both origin country ID "{flight.origin_country_id}" '
                f'and destination country ID"{flight.destination_country_id}" are in incorrect format.')
            return

        if not self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == flight.origin_country_id).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a flight because the origin country ID "{flight.origin_country_id}" '
                f'does not exists in the database.')
            return
        if not self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == flight.destination_country_id).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a flight because the destination country ID "{flight.destination_country_id}" '
                f'does not exists in the database.')
            return
        if not isinstance(flight.departure_time, datetime) or not isinstance(flight.landing_time, datetime):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a flight because both departure time "{flight.departure_time}" '
                f'and landing time "{flight.landing_time}" must be datetime objects.')
            return
        if flight.departure_time + timedelta(minutes=1) > flight.landing_time:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a flight because '
                f'the departure time "{flight.departure_time}" and landing time "{flight.landing_time}" '
                f'is less than one minute.')
            raise NotLegalFlightTimesError
        if not isinstance(flight.remaining_tickets, int):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a flight because the remaining tickets'
                f' "{flight.remaining_tickets}" are in incorrect format.')
            return
        if flight.remaining_tickets < 0:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a flight because the remaining tickets'
                f' "{flight.remaining_tickets}" must be at least 1.')
            return
        self.logger.logger.debug(
             f'You successfully used login token "{self.login_token}" to update a flight and updated the flight "{flight_[0]}" '
            f'to the flight "{flight}".')
        self.repo.update_by_id(Flight, Flight.id, flight.id, {Flight.origin_country_id: flight.origin_country_id,
                                                              Flight.destination_country_id: flight.destination_country_id,
                                                              Flight.departure_time: flight.departure_time,
                                                              Flight.landing_time: flight.landing_time,
                                                              Flight.remaining_tickets: flight.remaining_tickets})
        return True