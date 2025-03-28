import numpy as np
import pandas as pd

from polar_route.utils import round_to_sigfig

SIG_FIG_TOLERANCE = 4

# Testing route outputs
def test_route_coordinates(route_pair):
    compare_route_coordinates(route_pair[0], route_pair[1])

def test_waypoint_names(route_pair):
    compare_waypoint_names(route_pair[0], route_pair[1])
    
def test_time(route_pair):
    compare_time(route_pair[0], route_pair[1])

def test_fuel_battery(route_pair):
    path_variables = extract_route_info(route_pair[0])['path_variables']
    if 'fuel' in path_variables:
        compare_fuel(route_pair[0], route_pair[1])
    if 'battery' in path_variables:
        compare_battery(route_pair[0], route_pair[1])

def test_cell_indices(route_pair):
    compare_cell_indices(route_pair[0], route_pair[1])

def test_cases(route_pair):
    compare_cases(route_pair[0], route_pair[1])
    
def test_distance(route_pair):
    compare_distance(route_pair[0], route_pair[1])
    
def test_speed(route_pair):
    compare_speed(route_pair[0], route_pair[1])
    

# Comparison between old and new
def compare_route_coordinates(route_a, route_b):
    """
    Tests if coordinates of each node are the same between both routes.
    
    Args:
        route_a (json)
        route_b (json)
        
    Raises:
        AssertionError:
            Fails if length of coord arrays is different,
            which implies different nodes along route
        AssertionError:
            Fails if coords of each node are different at any point 
            (beyond sig fig limit)
    """
    coords_a = extract_path(route_a)['geometry']['coordinates']
    coords_b = extract_path(route_b)['geometry']['coordinates']

    len_a = len(coords_a)
    len_b = len(coords_b)
    
    assert(len_a == len_b), \
        f"Number of nodes different! Expected {len_a}, got {len_b}"
    
    rounded_x_a = round_to_sigfig(coords_a[:][0], sigfig=SIG_FIG_TOLERANCE)
    rounded_x_b = round_to_sigfig(coords_b[:][0], sigfig=SIG_FIG_TOLERANCE)

    rounded_y_a = round_to_sigfig(coords_a[:][1], sigfig=SIG_FIG_TOLERANCE)
    rounded_y_b = round_to_sigfig(coords_b[:][1], sigfig=SIG_FIG_TOLERANCE)
    
    np.testing.assert_array_equal(rounded_x_a, rounded_x_b, 
                                  err_msg='Difference in "route_coordinates"')
    np.testing.assert_array_equal(rounded_y_a, rounded_y_b, 
                                  err_msg='Difference in "route_coordinates"')

def compare_waypoint_names(route_a, route_b):
    """
    Tests if waypoint names are the same between both routes.
    
    Args:
        route_a (json)
        route_b (json)
        
    Raises:
        AssertionError:
            Fails if source or destination names don't match 
    """
    from_a = extract_path(route_a)['properties']['from']
    from_b = extract_path(route_b)['properties']['from']
    assert(from_a == from_b), \
        f"Waypoint source names don't match! Expected {from_a}, got {from_b}"
    
    to_a = extract_path(route_a)['properties']['to']
    to_b = extract_path(route_b)['properties']['to']
    assert(to_a == to_b), \
        f"Waypoint destination names don't match! Expected {to_a}, got {to_b}"

def compare_time(route_a, route_b):
    """
    Tests if times to each node are the same between both routes.
    
    Args:
        route_a (json)
        route_b (json)
        
    Raises:
        AssertionError:
            Fails if time to each node is different at any point 
            (beyond sig fig limit)
    """
    times_a = extract_path(route_a)['properties']['traveltime']
    times_b = extract_path(route_b)['properties']['traveltime']

    rounded_a = round_to_sigfig(times_a, sigfig=SIG_FIG_TOLERANCE)
    rounded_b = round_to_sigfig(times_b, sigfig=SIG_FIG_TOLERANCE)

    np.testing.assert_array_equal(rounded_a, rounded_b, 
                                  err_msg='Difference in "traveltime"')

def compare_fuel(route_a, route_b):
    """
    Tests if fuel to each node are the same between both routes.
    
    Args:
        route_a (json)
        route_b (json)
        
    Raises:
        AssertionError:
            Fails if fuel to each node is different at any point 
            (beyond sig fig limit)
    """
    fuel_a = extract_path(route_a)['properties']['fuel']
    fuel_b = extract_path(route_b)['properties']['fuel']

    rounded_a = round_to_sigfig(fuel_a, sigfig=SIG_FIG_TOLERANCE)
    rounded_b = round_to_sigfig(fuel_b, sigfig=SIG_FIG_TOLERANCE)

    np.testing.assert_array_equal(rounded_a, rounded_b, 
                                  err_msg='Difference in "fuel"')

def compare_battery(route_a, route_b):
    """
    Tests if battery consumption is the same between both routes.

    Args:
        route_a (json)
        route_b (json)

    Raises:
        AssertionError:
            Fails if battery consumption to each node is different at any point
            (beyond sig fig limit)
    """
    battery_a = extract_path(route_a)['properties']['battery']
    battery_b = extract_path(route_b)['properties']['battery']

    rounded_a = round_to_sigfig(battery_a, sigfig=SIG_FIG_TOLERANCE)
    rounded_b = round_to_sigfig(battery_b, sigfig=SIG_FIG_TOLERANCE)

    np.testing.assert_array_equal(rounded_a, rounded_b,
                                  err_msg='Difference in "battery"')

def compare_cell_indices(route_a, route_b):
    """
    Tests if cell indices are the same between both routes.
    
    Args:
        route_a (json)
        route_b (json)
        
    Raises:
        AssertionError:
            Fails if cell indices are different at any point
    """
    cid_a = extract_path(route_a)['properties']['CellIndices']
    cid_b = extract_path(route_b)['properties']['CellIndices']

    cid_a = [int(a) for a in cid_a]
    cid_b = [int(b) for b in cid_b]

    np.testing.assert_array_equal(cid_a, cid_b,
                                  err_msg='Difference in "cell_indices"')

def compare_cases(route_a, route_b):
    """
    Tests if dijkstra route direction cases are the same between both routes.
    
    Args:
        route_a (json)
        route_b (json)
        
    Raises:
        AssertionError:
            Fails if dijkstra route direction cases are different at any point
    """
    cases_a = extract_path(route_a)['properties']['cases']
    cases_b = extract_path(route_b)['properties']['cases']
    
    np.testing.assert_array_equal(cases_a, cases_b, 
                                  err_msg='Difference in "cases"')

def compare_distance(route_a, route_b):
    """
    Tests if distance between cells are the same between both routes.
    
    Args:
        route_a (json)
        route_b (json)
        
    Raises:
        AssertionError:
            Fails if distances are different at any point
    """
    distance_a = extract_path(route_a)['properties']['distance']
    distance_b = extract_path(route_b)['properties']['distance']

    rounded_a = round_to_sigfig(distance_a, sigfig=SIG_FIG_TOLERANCE)
    rounded_b = round_to_sigfig(distance_b, sigfig=SIG_FIG_TOLERANCE)

    np.testing.assert_array_equal(rounded_a, rounded_b, 
                                  err_msg='Difference in "distance"')
    
def compare_speed(route_a, route_b):
    """
    Tests if speed between cells are the same between both routes.
    
    Args:
        route_a (json)
        route_b (json)
        
    Raises:
        AssertionError:
            Fails if speeds are different at any point
    """
    speed_a = extract_path(route_a)['properties']['speed']
    speed_b = extract_path(route_b)['properties']['speed']

    rounded_a = round_to_sigfig(speed_a, sigfig=SIG_FIG_TOLERANCE)
    rounded_b = round_to_sigfig(speed_b, sigfig=SIG_FIG_TOLERANCE)

    np.testing.assert_array_equal(rounded_a, rounded_b, 
                                  err_msg='Difference in "speed"')

# Utility functions
def extract_waypoints(mesh):
    """
    Extracts waypoints from mesh and returns as a pd.Dataframe for 
    routeplanner to work with
    
    Args:
        mesh (json): JSON object with waypoints key

    Returns:
        pd.DataFrame: Dataframe constructed from waypoints
    """
    return pd.DataFrame.from_dict(mesh['waypoints'])

def extract_path(mesh):
    """
    Extracts path information from mesh and returns as a json for 
    tests to work with
    
    Args:
        mesh (json): JSON object with paths key

    Returns:
        json: Dictionary with path information
    """
    return mesh['paths']['features'][0]

def extract_route_info(mesh):
    """
    Extracts route info from mesh and returns as JSON to read
    
    Args:
        mesh (json): JSON object with route_info key

    Returns:
        json: Dictionary with route information
    """
    return mesh['config']['route_info']