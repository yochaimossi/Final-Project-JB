CREATE or replace function sp_get_airline_by_username
(_username text)
returns TABLE(id bigint, name text, country_id bigint,
			 user_id bigint)
language plpgsql AS
	$$
		BEGIN
			return QUERY
			select a.id, a.name, a.country_id,
			a.user_id from airline_companies a
			join users u on a.user_id = u.id
			where u.username = _username;
		end;
	$$;
|||
CREATE or replace function sp_get_customer_by_username
(_username text)
returns TABLE(id bigint, first_name text, last_name text,
			 address text, phone_no text,
			 credit_card_no text, user_id bigint)
language plpgsql AS
	$$
		BEGIN
			return QUERY
			select c.id, c.first_name, c.last_name,
			c.address, c.phone_no, c.credit_card_no,
			c.user_id from customers c
			join users u on c.user_id = u.id
			where u.username = _username;
		end;
	$$;
|||
CREATE or replace function sp_get_user_by_username
(_username text)
returns TABLE(id bigint, username text, password text,
			  email text, user_role int)
language plpgsql AS
	$$
		BEGIN
			return QUERY
			select u.id, u.username, u.password,
			u.email, u.user_role from users u
			where u.username = _username;
		end;
	$$;
|||
CREATE or replace function sp_get_flights_by_airline_id
(_airline_id bigint)
returns TABLE(id bigint, airline_company_id bigint,
			  origin_country_id bigint,
			  destination_country_id bigint,
			  departure_time timestamp,
			  landing_time timestamp,
			  remaining_tickets int)
language plpgsql AS
	$$
		BEGIN
			return QUERY
			select f.id, f.airline_company_id,
			f.origin_country_id, f.destination_country_id,
			f.departure_time, f.landing_time,
			f.remaining_tickets from flights f
			where f.airline_company_id = _airline_id;
		end;
	$$;
|||
CREATE or replace function sp_get_tickets_by_customer_id
(_customer_id bigint)
returns TABLE(id bigint, flight_id bigint,
			  customer_id bigint)
language plpgsql AS
	$$
		BEGIN
			return QUERY
			select t.id, t.flight_id, t.customer_id
			from tickets t where t.customer_id = _customer_id;
		end;
	$$;
|||
CREATE or replace function sp_get_arrival_flights
(_country_id int)
returns TABLE(id bigint, airline_company_id bigint, origin_country_id bigint, destination_country_id bigint, departure_time timestamp,
			 landing_time timestamp, remaining_tickets int)
language plpgsql AS
	$$
		BEGIN
			return QUERY
			select * from flights where (now() AT TIME ZONE 'UTC' + interval '12 hours') > flights.landing_time and flights.destination_country_id = _country_id;
		end;
	$$;
|||
CREATE or replace function sp_get_departure_flights
(_country_id int)
returns TABLE(id bigint, airline_company_id bigint, origin_country_id bigint, destination_country_id bigint, departure_time timestamp,
			 landing_time timestamp, remaining_tickets int)
language plpgsql AS
	$$
		BEGIN
			return QUERY
			select * from flights where (now() AT TIME ZONE 'UTC' + interval '12 hours') > flights.departure_time and flights.origin_country_id = _country_id;
		end;
	$$;
|||
CREATE or replace function sp_get_flights_by_parameters
(_origin_country_id int, _destination_country_id int, _date date)
returns TABLE(id bigint, airline_company_id bigint, origin_country_id bigint, destination_country_id bigint, departure_time timestamp,
			 landing_time timestamp, remaining_tickets int)
language plpgsql AS
	$$
		BEGIN
			return QUERY
			select * from flights where date(flights.departure_time) = _date and flights.origin_country_id = _origin_country_id
			and flights.destination_country_id = _destination_country_id;
		end;
	$$;