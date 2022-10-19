from flask import Blueprint, render_template, jsonify, request, current_app, make_response
from functools import wraps
import jwt
import uuid

from logger.Logger import Logger
from RabbitProducerObject import RabbitProducerObject
from ThreadLockManager import ThreadLockManager


airline = Blueprint("airline", __name__, template_folder="templates")


logger = Logger.get_instance()
rabbit_producer = RabbitProducerObject('db_requests')
lock_manager = ThreadLockManager.get_instance()


def airline_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.removeprefix('Bearer ')

        if not token:
            logger.logger.info('A user tried to used a function that requires token but token is missing.')
            return jsonify({'message': 'Token is missing'}), 401

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'])
            if payload['role'] == 'Airline Company':
                return f(payload, *args, **kwargs)
            else:
                jsonify({'message': 'Token is not valid'}), 401

        except (jwt.InvalidTokenError, jwt.ExpiredSignature, jwt.DecodeError, KeyError):
            logger.logger.warning('A user tried to used a function that requires token but token is not valid.')
            return jsonify({'message': 'Token is not valid'}), 401

    return decorated


@airline.route('/')
@airline_token_required
def home(login_token):
    return render_template('airline/home.html')


@airline.route('/flights', methods=['GET', 'POST'])
@airline_token_required
def flights(login_token):
    request_id: str = str(uuid.uuid4())

    if request.method == 'GET':
        rabbit_producer.publish({'id_': request_id, 'login_token': login_token, 'method': 'get',
                                 'resource': 'flight'})
        lock_manager.lock_thread(request_id)
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        pass

    else:
        new_flight: dict = request.get_json()
        rabbit_producer.publish({'id_': request_id, 'login_token': login_token, 'method': 'post',
                                 'resource': 'flight', 'data': new_flight})
        lock_manager.lock_thread(request_id)
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        pass


@airline.route('/flights/<int:id_>', methods=['PATCH', 'DELETE'])  # update and delete flight
@airline_token_required
def flight_by_id(login_token, id_):
    request_id: str = str(uuid.uuid4())

    if request.method == 'PATCH':
        patched_flight: dict = request.get_json()
        rabbit_producer.publish({'id_': request_id, 'login_token': login_token, 'method': 'patch',
                                 'resource': 'flight', 'data': patched_flight})
        lock_manager.lock_thread(request_id)
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        pass

    else:
        rabbit_producer.publish({'id_': request_id, 'login_token': login_token, 'method': 'delete',
                                 'resource': 'flight', 'resource_id': id_})
        lock_manager.lock_thread(request_id)
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        pass


@airline.route('/airlines/<int:id_>', methods=['PATCH'])  # update airline
@airline_token_required
def airline_by_id(login_token, id_):
    request_id: str = str(uuid.uuid4())

    patched_airline: dict = request.get_json()
    rabbit_producer.publish({'id_': request_id, 'login_token': login_token, 'method': 'patch',
                             'resource': 'airline', 'data': patched_airline})
    lock_manager.lock_thread(request_id)
    answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
    pass
