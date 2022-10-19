from FacadeBase import FacadeBase
from Flight import Flight
from Customer import Customer
from Ticket import Ticket
from NoRemainingTicketsError import NoRemainingTicketsError


class CustomerFacade(FacadeBase):

    def __init__(self, login_token):
        super().__init__()
        self.login_token = login_token

    def update_customer(self, customer):
        if self.login_token.role != 'Customer':
            self.logger.logger.error(
                 f'You cannot use the token "{self.login_token}" to update a customer because his role is not a customer.')
            return
        if not isinstance(customer, Customer):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update the customer :"{customer}" because its not a Customer object.')
            return
        updated_customer = self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.id == self.login_token.id).all())
        if not updated_customer:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a customer because his customer ID does not exist in the database.')
            return
        if self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.phone_no == customer.phone_no).all()) and \
                self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.phone_no == customer.phone_no).all()) != updated_customer:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a customer because the phone number "{customer.phone_no}" '
                f'already exists in the database.')
            return
        if self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.credit_card_no == customer.credit_card_no).all()) and \
                self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.credit_card_no == customer.credit_card_no).all()) != updated_customer:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to update a customer because the  credit card number "{customer.credit_card_no}" '
                f'already exists in the database.')
            return
        self.logger.logger.debug(
            f'You successfully used login token "{self.login_token}" to update a customer and updated to "{customer}"')
        self.repo.update_by_id(Customer, Customer.id, self.login_token.id, {Customer.first_name: customer.first_name, Customer.last_name: customer.last_name,
                                                                    Customer.address: customer.address, Customer.phone_no: customer.phone_no,
                                                                    Customer.credit_card_no: customer.credit_card_no})
        return True

    def add_ticket(self, ticket):
        if self.login_token.role != 'Customer':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add a ticket because you are not customer.')
            return
        if not isinstance(ticket, Ticket):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add a ticket because the ticket "{ticket}" is not a Ticket object.')
            return
        flight = self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.id == ticket.flight_id).all())
        if not flight:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add a ticket because the flight ID "{ticket.flight_id}" '
                f'does not exist in the database.')
            return
        if flight[0].remaining_tickets <= 0:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add a ticket because the flight has no remaining tickets')
            raise NoRemainingTicketsError
        if self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.customer_id == self.login_token.id,
                                                                         Ticket.flight_id == ticket.flight_id).all()):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to add a ticket because this customer already has a ticket for this flight')
            return
        self.repo.update_by_id(Flight, Flight.id, ticket.flight_id,  # updating the remaining tickets of the flight
                               {Flight.remaining_tickets: flight[0].remaining_tickets - 1})
        ticket.id = None
        ticket.customer_id = self.login_token.id
        self.logger.logger.debug(
            f'You successfully used login token "{self.login_token}" to add a ticket and added the ticket "{ticket}"')
        self.repo.add(ticket)
        return True

    def remove_ticket(self, ticket):
        if self.login_token.role != 'Customer':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove a ticket because you are not customer.')
            return
        if not isinstance(ticket, Ticket):
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove a ticket because the ticket "{ticket}" is not a Ticket object.')
            return
        ticket_ = self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.flight_id == ticket.flight_id,
                                                                               Ticket.customer_id == self.login_token.id).all())
        if not ticket_:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove a ticket because the ticket "{ticket}" does not exist in the database.')
            return
        if ticket_[0].customer_id != self.login_token.id:
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to remove a ticket because the customer ID "{ticket.customer_id}" '
                f'does not belong to the login token.')
            return
        self.repo.update_by_id(Flight, Flight.id, ticket_[0].flight.id,
                               {Flight.remaining_tickets: ticket_[0].flight.remaining_tickets + 1})
        self.logger.logger.debug(
             f'You successfully used login token "{self.login_token}" to remove a ticket and removed the ticket "{ticket}"')
        self.repo.delete_by_id(Ticket, Ticket.id, ticket_[0].id)
        return True

    def get_tickets_by_customer(self):
        if self.login_token.role != 'Customer':
            self.logger.logger.error(
                f'You cannot use the token "{self.login_token}" to get tickets by customer but his role is not customer.')
            return
        return self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.customer_id == self.login_token.id).all())



