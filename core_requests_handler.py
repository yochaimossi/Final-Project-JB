import threading

from RabbitConsumerObject import RabbitConsumerObject
from RabbitProducerObject import RabbitProducerObject
from facades.AnonymousFacade import AnonymousFacade
from facades.CustomerFacade import CustomerFacade
from facades.AirlineFacade import Airline_Company
from facades.AdministratorFacade import AdministratorFacade
from data_access_objects.DbRepoPool import DbRepoPool
from custom_errors.NoRemainingTicketsError import NoRemainingTicketsError
from custom_errors.NotLegalFlightTimesError import NotLegalFlightTimesError
from custom_errors.UserRoleTableError import UserRoleTableError
from custom_errors.NotValidDataError import NotValidDataError
from custom_errors.WrongLoginDataError import WrongLoginDataError
from custom_errors.WrongLoginTokenError import WrongLoginTokenError
from login_token.LoginToken import LoginToken
from ThreadLockManager import ThreadLockManager
from tables.User import User
from tables.Customer import Customer

from datetime import datetime
import time
import json


rabbit_producer = RabbitProducerObject('db_responses')
repool = DbRepoPool.get_instance()


def main():
    rabbit = RabbitConsumerObject(q_name='db_requests', callback=callback)
    rabbit.consume()


def callback(ch, method, properties, body):
    request = json.loads(body)  # reading the data
    request_id = request['id_']  # getting the request id


    method = request['method']  # getting the method
    resource = request['resource']  # getting the resource

    if resource == 'country':
        repo = repool.get_connection()
        anonymous_facade = AnonymousFacade(repo)
        if method == 'get':
            if 'resource_id' in request:  # get country by id
                try:
                    country = anonymous_facade.get_country_by_id(request['resource_id'])
                    country = [country.get_dictionary() for country in country]
                    rabbit_producer.publish(json.dumps({'id_': request_id, 'error': None, 'data': country}))
                except NotValidDataError:
                    rabbit_producer.publish(json.dumps({'id_': request_id, 'error': 'NotValidDataError'}))
                finally:
                    repool.return_connection(repo)
                    return

            else:
                countries = anonymous_facade.get_all_countries()
                countries = [country.get_dictionary() for country in countries]
                repool.return_connection(repo)
                rabbit_producer.publish(json.dumps({'id_': request_id, 'error': None, 'data': countries}))
                return

    elif resource == 'ticket':
        pass

    elif resource == 'flight':
        if 'login_token' in request:
            pass

        else:
            if method == 'get':
                repo = repool.get_connection()
                anonymous_facade = AnonymousFacade(repo)
                if 'resource_id' in request:
                    try:
                        flight = anonymous_facade.get_flight_by_id(request['resource_id'])
                        flight = [flight.get_dictionary() for flight in flight]
                        print(flight)
                        rabbit_producer.publish(json.dumps({'id_': request_id, 'error': None, 'data': flight}))
                    except NotValidDataError:
                        rabbit_producer.publish(json.dumps({'id_': request_id, 'error': 'NotValidDataError'}))
                    finally:
                        repool.return_connection(repo)
                        return
                if 'filter' in request:
                    if request['filter'] == 'arrivals_delta_t':
                        try:
                            flights = anonymous_facade.get_arrival_flights_by_delta_t(request['arrivals_delta_t'])
                            flights = [flight.get_dictionary() for flight in flights]
                            rabbit_producer.publish(json.dumps({'id_': request_id, 'error': None, 'data': flights}))
                        except NotValidDataError:
                            rabbit_producer.publish(json.dumps({'id_': request_id, 'error': 'NotValidDataError'}))
                        finally:
                            repool.return_connection(repo)
                            return
                    elif request['filter'] == 'departures_delta_t':
                        try:
                            flights = anonymous_facade.get_departure_flights_by_delta_t(request['departures_delta_t'])
                            flights = [flight.get_dictionary() for flight in flights]
                            rabbit_producer.publish(json.dumps({'id_': request_id, 'error': None, 'data': flights}))
                        except NotValidDataError:
                            rabbit_producer.publish(json.dumps({'id_': request_id, 'error': 'NotValidDataError'}))
                        finally:
                            repool.return_connection(repo)
                            return
                    elif request['filter'] == 'airline_id':
                        try:
                            flights = anonymous_facade.get_flights_by_airline_id(request['airline_id'])
                            flights = [flight.get_dictionary() for flight in flights]
                            rabbit_producer.publish(json.dumps({'id_': request_id, 'error': None, 'data': flights}))
                        except NotValidDataError:
                            rabbit_producer.publish(json.dumps({'id_': request_id, 'error': 'NotValidDataError'}))
                        finally:
                            repool.return_connection(repo)
                            return
                    elif request['filter'] == 'params':
                        try:
                            date_ls = request['date'].split('-')
                            date = datetime(int(date_ls[0]), int(date_ls[1]), int(date_ls[2]))
                        except:
                            date = request['date']
                        try:
                            flights = anonymous_facade.get_flights_by_parameters(
                                origin_country_id=request['origin_country_id'],
                                destination_country_id=request['destination_country_id'], date=date)
                            flights = [flight.get_dictionary() for flight in flights]
                            rabbit_producer.publish(json.dumps({'id_': request_id, 'error': None, 'data': flights}))
                        except NotValidDataError:
                            rabbit_producer.publish(json.dumps({'id_': request_id, 'error': 'NotValidDataError'}))
                        finally:
                            repool.return_connection(repo)
                            return
                else:
                    flights = anonymous_facade.get_all_flights()
                    flights = [flight.get_dictionary() for flight in flights]
                    rabbit_producer.publish(json.dumps({'id_': request_id, 'error': None, 'data': flights}))
                    repool.return_connection(repo)
                    return

    elif resource == 'customer':
        print('trying to create the customer')
        if request['method'] == 'post':
            if 'login_token' in request:
                pass
            else:
                repo = repool.get_connection()
                anonymous_facade = AnonymousFacade(repo)
                try:
                    user_dict: dict = request['data']['user']
                    print(user_dict)
                    customer_dict: dict = request['data']['customer']
                    print(customer_dict)
                    new_user = User(username=user_dict['username'],
                                    password=user_dict['password'],
                                    email=user_dict['email'],
                                    user_role=user_dict['user_role'])
                    new_customer = Customer(first_name=customer_dict['first_name'],
                                            last_name=customer_dict['last_name'],
                                            address=customer_dict['address'],
                                            phone_no=customer_dict['phone_no'],
                                            credit_card_no=customer_dict['credit_card_no'],
                                            user_id=customer_dict['user_id'])
                    anonymous_facade.add_customer(user=new_user, customer=new_customer)
                    rabbit_producer.publish(json.dumps({'id_': request_id, 'error': None}))
                except NotValidDataError:
                    rabbit_producer.publish(json.dumps({'id_': request_id, 'error': 'NotValidDataError'}))
                finally:
                    repool.return_connection(repo)
                    return

    elif resource == 'airline':
        if method == 'get':
            repo = repool.get_connection()
            anonymous_facade = AnonymousFacade(repo)
            if 'resource_id' in request:  # get airline by id
                try:
                    airline = anonymous_facade.get_airline_by_id(request['resource_id'])
                    airline = [airline.get_dictionary() for airline in airline]
                    print(airline)
                    rabbit_producer.publish(json.dumps({'id_': request_id, 'error': None, 'data': airline}))
                except NotValidDataError:
                    rabbit_producer.publish(json.dumps({'id_': request_id, 'error': 'NotValidDataError'}))
                finally:
                    repool.return_connection(repo)
                    return

            else:
                airlines = anonymous_facade.get_all_airlines()
                airlines = [airline.get_dictionary() for airline in airlines]
                repool.return_connection(repo)
                rabbit_producer.publish(json.dumps({'id_': request_id, 'error': None, 'data': airlines}))
                return

        elif method == 'post':
            pass

        elif method == 'delete':
            pass

        elif method == 'patch':
            pass

    elif resource == 'admin':

        repo = repool.get_connection()
        login_token = get_login_token(request['login_token'])
        admin_facade = AdministratorFacade(login_token=login_token, repo=repo)
        if method == 'post':
            try:
                admin_facade.add_administrator(user=request['data']['user'],
                                               administrator=request['data']['admin'])
                rabbit_producer.publish({'id_': request_id, 'error': None})
            except WrongLoginTokenError:
                rabbit_producer.publish({'id_': request_id, 'error': 'WrongLoginTokenError'})
            except NotValidDataError:
                rabbit_producer.publish({'id_': request_id, 'error': 'NotValidDataError'})
            finally:
                repool.return_connection(repo)
                return

        elif method == 'delete':
            resource_id = request['resource_id']
            try:
                admin_facade.remove_administrator(resource_id)
                rabbit_producer.publish({'id_': request_id, 'error': None})
            except WrongLoginTokenError:
                rabbit_producer.publish({'id_': request_id, 'error': 'WrongLoginTokenError'})
            except NotValidDataError:
                rabbit_producer.publish({'id_': request_id, 'error': 'NotValidDataError'})
            finally:
                repool.return_connection(repo)
                return


def get_login_token(login_token_json):
    return LoginToken(id_=login_token_json['id_'], name=login_token_json['name'],
                      role=login_token_json['role'])


if __name__ == '__main__':
    main()
