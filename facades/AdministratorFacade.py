from FacadeBase import FacadeBase
from Customer import Customer
from User import User
from Flight import Flight
from Ticket import Ticket
from Airline_Company import Airline_Company
from Administrator import Administrator
from Country import Country


class AdministratorFacade(FacadeBase):

    def __init__(self, login_token):
        super().__init__()
        self.login_token = login_token

    def get_all_customers(self):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get the customer list because you are not an administartor.')
            return
        return self.repo.get_all(Customer)

    def add_administrator(self, user, administrator):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add an administrator because you are not an administartor.')
            return
        if not isinstance(user, User):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add an administrator because you are not a registered user.')
            return
        if user.user_role != 3:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add an administrator because "{user.user_role}" is not not an administartor.')
            return
        if not isinstance(administrator, Administrator):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add an administrator because the administrator "{administrator}" '
                f'that was sent is not an Administrator object.')
            return
        if self.create_user(user):
            administrator.id = None
            administrator.user_id = user.id
            self.logger.logger.debug(
                f'You successfully used login token "{self.login_token}" to add "{user}" as an "{administrator}".')
            self.repo.add(administrator)
            return True
        else:
            self.logger.logger.error(
                 f'You cannot use the token "{self.login_token}" to add an administrator because user "{user}" '
                f'that was sent is not a valid user.')
            return

    def remove_administrator(self, administrator_id):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove an administrator because you are not an administartor.')
            return


        if not isinstance(administrator_id, int):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove an administrator because the administrator ID "{administrator_id}" '
                f'that was sent is not in the correct format.')
            return

        admin = self.repo.get_by_condition(Administrator, lambda query: query.filter(Administrator.id == administrator_id).all())
        if not admin:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove an administrator because the administrator ID "{administrator_id}" '
                f'does not exist in the database.')
            return
        self.logger.logger.debug(
            f'You successfully used login token "{self.login_token}" to remove "{admin}" as an administrator.')
        self.repo.delete_by_id(User, User.id, admin[0].user.id)
        return True

    def remove_airline(self, airline_id):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove an airline because you are not an administrator.')
            return
        if not isinstance(airline_id, int):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove an airline because the airline ID "{airline_id}" '
                f'that was sent is not in the correct format.')
            return


        airline = self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.id == airline_id).all())
        if not airline:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove an airline because the airline ID "{airline_id}" '
                f'does not exist in the database.')
            return
        self.logger.logger.debug(
            f'You successfully used login token "{self.login_token}" to remove the airline "{airline}" from the database')
        self.repo.delete_by_id(User, User.id, airline[0].user.id)
        return True

    def remove_customer(self, customer_id):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove a customer because you are not an administrator.')
            return
        if not isinstance(customer_id, int):
            self.logger.logger.error(
                         f'You cannot use the token "{self.login_token}" to remove an administrator because the airline ID "{customer_id}" '
                f'that was sent is not in the correct format.')
            return

        customer = self.repo.get_by_condition(Customer,
                                           lambda query: query.filter(Customer.id == customer_id).all())
        if not customer:
            self.logger.logger.error(
                 f'You cannot use the token "{self.login_token}" to remove a customer because the customer ID "{customer_id}" '
                f'does not exist in the database.')
            return
        tickets = self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.customer_id == customer_id).all())
        for ticket in tickets:
            self.repo.update_by_id(Flight, Flight.id, ticket.flight_id,  # updating the remaining tickets of the flight
                                   {Flight.remaining_tickets: ticket.flight.remaining_tickets + 1})
        self.logger.logger.debug(
            f'You successfully used login token "{self.login_token}" to remove the customer "{customer}" from the database')
        self.repo.delete_by_id(User, User.id, customer[0].user.id)
        return True

    def add_customer(self, user, customer):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add a customer because you are not an administrator.')
        if not isinstance(user, User):
            self.logger.logger.error(
                 f'You cannot use the token "{self.login_token}" to add an administrator because the user "{user}" '
                f'that was sent is not a User instance.')
            return
        if user.user_role != 1:
            self.logger.logger.error(
                  f'You cannot use the token "{self.login_token}" to add a customer because your user role "{user.user_role}" '
                f'is not customer.')
            return
        if not isinstance(customer, Customer):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add a customer because customer "{customer}" '
                f'that was sent is not a Customer object.')
            return
        if self.repo.get_by_condition(Customer,
                                      lambda query: query.filter(Customer.phone_no == customer.phone_no).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add a customer because the customer phone number "{customer.phone_no}" '
                f'already exists in the database.')
            return
        if self.repo.get_by_condition(Customer,
                                      lambda query: query.filter(
                                          Customer.credit_card_no == customer.credit_card_no).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add a customer because the customer credit card number "{customer.credit_card_no}" '
                f'already exists in the database.')
            return
        if self.create_user(user):
            customer.id = None
            customer.user_id = user.id
            self.logger.logger.debug(
                f'You successfully used login token "{self.login_token}" to add user "{user}" to the customer "{customer}"')
            self.repo.add(customer)
            return True
        else:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add a customer because the user "{user}" is not valid user.')
            return

    def add_airline(self, user, airline):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                 f'You cannot use the token "{self.login_token}" to add an airline because you are not an administrator.')
            return
        if not isinstance(user, User):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add an airline because the user "{user}" '
                f'that was sent is not a User instance.')
            return
        if user.user_role != 2:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add an airline because your user role "{user.user_role}" '
                f'is not airline.')
            return
        if not isinstance(airline, Airline_Company):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add an airline because airline "{airline}" '
                f'is not an Airline Company object.')
            return
        if self.repo.get_by_condition(Airline_Company,
                                      lambda query: query.filter(Airline_Company.name == airline.name).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add an airline because the  airline name "{airline.name}" '
                f'already exists in the database.')
            return
        if not self.repo.get_by_condition(Country,
                                          lambda query: query.filter(Country.id == airline.country_id).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add an airline because airline country ID "{airline.country_id}" '
                f'does not exist in the database.')
            return
        if self.create_user(user):
            airline.id = None
            airline.user_id = user.id
            self.logger.logger.debug(
                f'You successfully used login token "{self.login_token}" to add airline "{airline}" to the user "{user}".')
            self.repo.add(airline)
            return True
        else:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add an airline because the user "{user}" is not valid.')
            return