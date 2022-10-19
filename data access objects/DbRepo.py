from sqlalchemy import asc, text, extract
from Customer import Customer
from Administrator import Administrator
from Airline_Company import Airline_Company
from Country import Country
from Flight import Flight
from Ticket import Ticket
from User_Role import User_Role
from User import User
from datetime import datetime
from Logger import Logger
from sqlalchemy.exc import OperationalError


class DbRepo:
    def __init__(self, local_session):
        self.local_session = local_session
        self.logger = Logger.get_instance()

    def reset_auto_inc(self, table_class):
        try:
            self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE')
            self.local_session.commit()
            self.logger.logger.debug(f'Reset auto inc in {table_class} table')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_all(self, table_class):
        try:
            return self.local_session.query(table_class).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_all_limit(self, table_class, limit_num):
        try:
            return self.local_session.query(table_class).limit(limit_num).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_all_order_by(self, table_class, column_name, direction=asc):
        try:
            return self.local_session.query(table_class).order_by(direction(column_name)).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_by_column_value(self, table_class, column_value, value):
        try:
            return self.local_session.query(table_class).filter(column_value == value).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_by_condition(self, table_class, condition):
        try:
            return condition(self.local_session.query(table_class))
        except OperationalError as e:
            self.logger.logger.critical(e)

    def add(self, one_row):
        try:
            self.local_session.add(one_row)
            self.local_session.commit()
            self.logger.logger.debug(f'{one_row} has been added to the database')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def add_all(self, rows_list):
        try:
            self.local_session.add_all(rows_list)
            self.local_session.commit()
            self.logger.logger.debug(f'{rows_list} have been added to the database')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def delete_by_id(self, table_class, id_column_name, id_):
        try:
            self.local_session.query(table_class).filter(id_column_name == id_).delete(synchronize_session=False)
            self.local_session.commit()
            self.logger.logger.debug(f'A row with the id {id_} has been deleted from {table_class}')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def update_by_id(self, table_class, id_column_name, id_, data):
        try:
            self.local_session.query(table_class).filter(id_column_name == id_).update(data)
            self.local_session.commit()
            self.logger.logger.debug(f'A row with the id {id_} has been updated from {table_class}. the updated data is  {data}.')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_airlines_by_country(self, country_id):
        try:
            return self.local_session.query(Airline_Company).filter(Airline_Company.country_id == country_id).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_flights_by_destination_country_id(self, country_id):
        try:
            return self.local_session.query(Flight).filter(Flight.destination_country_id == country_id).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_flights_by_origin_country_id(self, country_id):
        try:
            return self.local_session.query(Flight).filter(Flight.origin_country_id == country_id).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_flights_by_departure_date(self, departure_date):
        try:
            return self.local_session.query(Flight).filter(extract('year', Flight.departure_date) == departure_date.year,
                                                           extract('month', Flight.departure_date) == departure_date.month,
                                                           extract('day', Flight.departure_date) == departure_date.day).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_flights_by_landing_date(self, landing_date):
        try:
            return self.local_session.query(Flight).filter(extract('year', Flight.departure_date) == landing_date.year,
                                                           extract('month', Flight.departure_date) == landing_date.month,
                                                           extract('day',
                                                                   Flight.departure_date) == landing_date.day).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_flights_by_customer(self, customer_id):
        try:
            flights_ls = []
            tickets = self.local_session.query(Ticket).filter(Ticket.customer_id == customer_id).all()
            for ticket in tickets:
                flights_ls.append(ticket.flight)
            return flights_ls
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_airline_by_username(self, _username):
        try:
            stmt = text('select * from sp_get_airline_by_username(:username)').bindparams(username=_username)
            airline_cursor = self.local_session.execute(stmt)
            airline = [air1 for air1 in airline_cursor][0]
            return airline
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_customer_by_username(self, _username):
        try:
            stmt = text('select * from sp_get_customer_by_username(:username)').bindparams(username=_username)
            customer_cursor = self.local_session.execute(stmt)
            customer = [cus1 for cus1 in customer_cursor][0]
            return customer
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_user_by_username(self, _username):
        try:
            stmt = text('select * from sp_get_user_by_username(:username)').bindparams(username=_username)
            user_cursor = self.local_session.execute(stmt)
            user = [us1 for us1 in user_cursor][0]
            return user
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_flights_by_airline_id(self, _airline_id):
        try:
            stmt = text('select * from sp_get_flights_by_airline_id(:airline_id)').bindparams(airline_id=_airline_id)
            flights_cursor = self.local_session.execute(stmt)
            flights = [flight for flight in flights_cursor]
            return flights
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_tickets_by_customer_id(self, _customer_id):
        try:
            stmt = text('select * from sp_get_tickets_by_customer_id(:customer_id)').bindparams(customer_id=_customer_id)
            tickets_cursor = self.local_session.execute(stmt)
            tickets = [ticket for ticket in tickets_cursor]
            return tickets
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_arrival_flights(self, _country_id):
        try:
            stmt = text('select * from sp_get_arrival_flights(:country_id)').bindparams(country_id=_country_id)
            flights_cursor = self.local_session.execute(stmt)
            flights = [flight for flight in flights_cursor]
            return flights
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_departure_flights(self, _country_id):
        try:
            stmt = text('select * from sp_get_departure_flights(:country_id)').bindparams(country_id=_country_id)
            flights_cursor = self.local_session.execute(stmt)
            flights = [flight for flight in flights_cursor]
            return flights
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_flights_by_parameters(self, _origin_country_id, _destination_country_id, _date):
        try:
            stmt = text('select * from sp_get_flights_by_parameters(:origin_country_id, :destination_country_id, :date)')\
                .bindparams(origin_country_id=_origin_country_id, destination_country_id=_destination_country_id, date=_date)
            flights_cursor = self.local_session.execute(stmt)
            flights = [flight for flight in flights_cursor]
            return flights
        except OperationalError as e:
            self.logger.logger.critical(e)

    def create_all_sp(self, file):
        try:
            try:
                with open(file, 'r') as sp_file:
                    queries = sp_file.read().split('|||')
                for query in queries:
                    self.local_session.execute(query)
                self.local_session.commit()
                self.logger.logger.debug(f'all sp from {file} were created.')
            except FileNotFoundError:
                self.logger.logger.critical(f'Tried to create all sp from the the file "{file}" but file was not found')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def drop_all_tables(self):
        try:
            self.local_session.execute('DROP TABLE users CASCADE')
            self.local_session.execute('DROP TABLE user_roles CASCADE')
            self.local_session.execute('DROP TABLE tickets CASCADE')
            self.local_session.execute('DROP TABLE flights CASCADE')
            self.local_session.execute('DROP TABLE customers CASCADE')
            self.local_session.execute('DROP TABLE countries CASCADE')
            self.local_session.execute('DROP TABLE airline_companies CASCADE')
            self.local_session.execute('DROP TABLE administrators CASCADE')
            self.local_session.commit()
            self.logger.logger.debug(f'All tables Dropped.')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def reset_test_db(self):
        try:
            # resetting auto increment for all tables
            self.reset_auto_inc(Country)
            self.reset_auto_inc(User_Role)
            self.reset_auto_inc(User)
            self.reset_auto_inc(Administrator)
            self.reset_auto_inc(Airline_Company)
            self.reset_auto_inc(Customer)
            self.reset_auto_inc(Flight)
            self.reset_auto_inc(Ticket)
            # county
            israel = Country(name='Israel')
            self.add(israel)
            self.add(Country(name='Germany'))
            # user role
            self.add(User_Role(role_name='Customer'))
            self.add(User_Role(role_name='Airline Company'))
            self.add(User_Role(role_name='Administrator'))
            self.add(User_Role(role_name='Not Legal'))
            # user
            self.add(User(username='Dan', password='123', email='dan@gmail.com', user_role=1))
            self.add(User(username='James', password='123', email='james@gmail.com', user_role=1))
            self.add(User(username='Avi', password='123', email='avi@gmail.com', user_role=2))
            self.add(User(username='Benny', password='123', email='benny@gmail.com', user_role=2))
            self.add(User(username='Tonny', password='123', email='tonny@gmail.com', user_role=3))
            self.add(User(username='Felix', password='123', email='felix@gmail.com', user_role=3))
            self.add(User(username='not legal', password='123', email='notlegal@gmail.com', user_role=4))
            # administrator
            self.add(Administrator(first_name='John', last_name='Don', user_id=5))
            self.add(Administrator(first_name='Rami', last_name='Babbi', user_id=6))
            # airline company
            self.add(Airline_Company(name='ELAL', country_id=1, user_id=3))
            self.add(Airline_Company(name='Lufthansa', country_id=2, user_id=4))
            # customer
            self.add(Customer(first_name='Jon', last_name='Doe', address='Bond 11',
                              phone_no='0549549957', credit_card_no='3355', user_id=1))
            self.add(Customer(first_name='Ploni', last_name='Almoni', address='Oxford 16',
                              phone_no='0527688459', credit_card_no='3711', user_id=2))
            # flight
            self.add(Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                            departure_time=datetime(2022, 1, 30, 16, 0, 0),
                            landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=100))
            self.add(Flight(airline_company_id=2, origin_country_id=1, destination_country_id=2,
                            departure_time=datetime(2022, 1, 30, 16, 0, 0),
                            landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=0))
            # ticket
            self.add(Ticket(flight_id=1, customer_id=1))
            self.add(Ticket(flight_id=2, customer_id=2))
            self.logger.logger.debug(f'Reset flights_db_tests')
        except OperationalError as e:
            self.logger.logger.critical(e)


