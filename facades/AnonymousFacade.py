from FacadeBase import FacadeBase
from CustomerFacade import CustomerFacade
from AirlineFacade import AirlineFacade
from AdministratorFacade import AdministratorFacade
from User import User
from Customer import Customer
from LoginToken import LoginToken
from UserRoleTableError import UserRoleTableError


class AnonymousFacade(FacadeBase):

    facade_dict = {1: lambda login_token: CustomerFacade(login_token), 2: lambda login_token: AirlineFacade(login_token),
                   3: lambda login_token: AdministratorFacade(login_token)}

    def __init__(self):
        super().__init__()

    def login(self, username, password):
        user = self.repo.get_by_condition(User, lambda query: query.filter(User.username == username, User.password == pw).all())
        if not user:
            self.logger.logger.info(
                f'Wrong username {username} or password {password},please check again.')
            return
        else:
            if user[0].user_role == 1:
                token_dict = {1: {'id': user[0].customers.id, 'name': user[0].customers.first_name, 'role': 'Customer'}}
            elif user[0].user_role == 2:
                token_dict = {2: {'id': user[0].airline_companies.id, 'name': user[0].airline_companies.name, 'role': 'Airline Company'}}
            elif user[0].user_role == 3:
                token_dict = {3: {'id': user[0].administrators.id, 'name': user[0].administrators.first_name, 'role': 'Administrator'}}
            else:
                self.logger.logger.error(
                    f'This uer is not a customer,airline or administrator-please check again.')
                raise UserRoleTableError

            login_token = LoginToken(token_dict[user[0].user_role]['id'], token_dict[user[0].user_role]['name'],
                                     token_dict[user[0].user_role]['role'])

            self.logger.logger.debug(f'{login_token} logged into the system.')
            return AnonymousFacade.facade_dict[user[0].user_role](login_token)

    def add_customer(self, user, customer):
        if not isinstance(user, User):
            self.logger.logger.error(f'The user "{user}" cannot be added as a customer because it is not a User instance.')
            return
        if user.user_role != 1:
            self.logger.logger.error(f'The user "{user.user_role}" is not a customer.')
            return
        if not isinstance(customer, Customer):
            self.logger.logger.error(
                f'The customer "{customer}" that was sent  is not a Customer instance.')
            return
        if self.repo.get_by_condition(Customer,
                                      lambda query: query.filter(Customer.phone_no == customer.phone_no).all()):
            self.logger.logger.error(
                f'The customer phone number "{customer.phone_no}" already exists in the database.')
            return
        if self.repo.get_by_condition(Customer,
                                      lambda query: query.filter(
                                          Customer.credit_card_no == customer.credit_card_no).all()):
            self.logger.logger.error(
                f'The customer credit card number "{customer.credit_card_no}" already exists in the database.')
            return
        if self.create_user(user):
            customer.id = None
            customer.user_id = user.id
            self.logger.logger.debug(f'Customer "{customer}" connected by the User "{user}" has been added to the database.')
            self.repo.add(customer)
            return True
        else:
            self.logger.logger.error(f'The function failed - User "{user} " is not a valid user.')
            return