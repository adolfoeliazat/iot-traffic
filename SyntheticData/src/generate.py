import random
import sys
from time import strftime
import datetime
import uuid
import geolib as geo

EARTH_RADIUS = 6378.1						# Radius of earth
SEED_COORDINATE = (40.12009,-88.247681)		# Coordinate
SEED_VELOCITY = 50							# 50 miles/hour
SEED_TIME = 0.0167						    # 1 minute(s) converted to hour
SEED_DIRECTION = 90							# 90 degrees
SEED_VELOCITY_CRASHED = 5					# 5 miles/hour

vehicle_set = {}

def randomize_conditions(max_range):
	random_error = random.random()
	random_range = random.randint(0, max_range)
	velocity_change = random_range*random_error
	random_direction = random.randint(0, 11)
	random_dict = {}
	random_dict['velocity_change'] = velocity_change
	if random_direction < 6:
		random_dict['direction'] = 90
	elif random_direction < 8:
		random_dict['direction'] = 180
	elif random_direction < 10:
		random_dict['direction'] = 270
	else:
		random_dict['direction'] = 360
	return random_dict
#end_def

def difference(a, b):
	if a > b:
		return 1
	else:
		return 0
	#endif

# Based on Vaishali's Data
def get_speed_change(current_velocity, weather, previous_condition):
	temperature = difference(weather['tmin'], previous_condition['tmin'])
	snow = difference(weather['snow'], previous_condition['snow'])
	windspeed = difference(weather['wind'], previous_condition['windspeed'])
	final_velocity = current_velocity
	if windspeed == 1:
		final_velocity = final_velocity - (0.1*current_velocity)

	if snow == 1:
		final_velocity = final_velocity - (0.2*current_velocity)
	return final_velocity


def get_motion_for_vehicles(num_vehicles, num_coordinates):
	result = {}
	# Initialization
	for i in range(num_vehicles):
		unique_id = uuid.uuid4()
		result[unique_id] = []
	current_velocity = SEED_VELOCITY
	current_coordinate = SEED_COORDINATE
	time_stamp = datetime.datetime.now()
	first_stamp = time_stamp

	# Working
	for i in range(num_coordinates):
		current_key = "temporary"
		changes = {}
		for key in result.keys():
			current_key = key
			random_conditions = randomize_conditions(5)
			if current_velocity + random_conditions['velocity_change'] < 55:
				current_velocity = current_velocity - random_conditions['velocity_change']
			distance_travelled = current_velocity * SEED_TIME
			next_coordinate = geo.predict_next_coordinate(current_coordinate, distance_travelled, SEED_DIRECTION)
			current_coordinate = next_coordinate
			changes['car_id'] = str(key)
			changes['latitude'] = current_coordinate[0]
			changes['longitude'] = current_coordinate[1]
			changes['time_stamp'] = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
		#endfor
		time_stamp = time_stamp + datetime.timedelta(0, 60)
		result[current_key].append(changes)
		pass
	#endfor
	return result
#enddef'

def get_weather_dependent_motion_for_vehicles(num_vehicles, num_coordinates):
	result = {}
	# Initialization
	for i in range(num_vehicles):
		unique_id = uuid.uuid4()
		result[unique_id] = []
	current_velocity = SEED_VELOCITY
	current_coordinate = SEED_COORDINATE
	time_stamp = datetime.datetime.now()
	first_stamp = time_stamp

	# Working
	for i in range(num_coordinates):
		current_key = "temporary"
		changes = {}
		for key in result.keys():
			current_key = key
			random_conditions = randomize_conditions(5)
			weather = weather_conditions(current_coordinate, datetime.now())
			current_velocity = get_speed_change(current_velocity, weather, result[key][-1])
			distance_travelled = current_velocity * SEED_TIME
			next_coordinate = geo.predict_next_coordinate(current_coordinate, distance_travelled, SEED_DIRECTION)
			current_coordinate = next_coordinate
			changes['car_id'] = str(key)
			changes['latitude'] = current_coordinate[0]
			changes['longitude'] = current_coordinate[1]
			changes['time_stamp'] = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
			changes['windspeed'] = weather['wind']
			changes['snow'] = weather['snow']
			changes['tmin'] = weather['tmin']
			vehicle_set[key] = (changes['latitude'], changes['longitude'])
			accident_vehicle = check_accident(key)
 		#endfor
		time_stamp = time_stamp + datetime.timedelta(0, 60)
		result[current_key].append(changes)
		pass
	#endfor
	return result
#enddef

def check_accident(vehicle_id):
	list_cars = []
	for key in vehicle_set:
		if isAccidentProne(vehicle_set[key], vehicle_set[vehicle_id])
			list_cars.append(key)
		pass
	pass
	return list_cars

# Currently supports exact same coordinates but should get a 1 m radius
def isAccidentProne(vehicle1_coord, vehicle2_coord):
	return (vehicle1_coord == vehicle2_coord)