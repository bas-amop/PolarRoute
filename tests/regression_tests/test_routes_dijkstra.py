import json
import pytest
import time

from polar_route import __version__ as pr_version
from polar_route.route_planner.route_planner import RoutePlanner

from .route_test_functions import extract_waypoints
from .route_test_functions import extract_route_info

# Import tests, which are automatically run
from .route_test_functions import test_route_coordinates
from .route_test_functions import test_waypoint_names
from .route_test_functions import test_time
from .route_test_functions import test_fuel_battery
from .route_test_functions import test_cell_indices
from .route_test_functions import test_cases

import logging
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# location of test files to be recalculated for regression testing
TEST_ROUTES = [
    './example_routes/dijkstra/fuel/gaussian_random_field.json',
    './example_routes/dijkstra/fuel/gaussian_random_field_waypointsplitting.json',
    './example_routes/dijkstra/fuel/checkerboard.json',
    './example_routes/dijkstra/fuel/great_circle_forward.json',
    './example_routes/dijkstra/fuel/great_circle_reverse.json',
    './example_routes/dijkstra/time/gaussian_random_field.json',
    './example_routes/dijkstra/time/gaussian_random_field_waypointsplitting.json',
    './example_routes/dijkstra/time/checkerboard.json',
    './example_routes/dijkstra/time/great_circle_forward.json',
    './example_routes/dijkstra/time/great_circle_reverse.json',
    './example_routes/dijkstra/time/multi_waypoint_blocked.json',
    './example_routes/dijkstra/time/single_cell.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_20lat_s.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_20lat_n.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_40lat_s.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_40lat_n.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_60lat_s.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_60lat_n.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_80lat_s.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_80lat_n.json',
    './example_routes/dijkstra/crossing_point/diagonal/diagonal_0lat.json',
    './example_routes/dijkstra/crossing_point/diagonal/diagonal_0lat_split.json',
    './example_routes/dijkstra/crossing_point/diagonal/diagonal_0lat_split4.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_20lat_s.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_20lat_n.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_40lat_s.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_40lat_n.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_60lat_s.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_60lat_n.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_80lat_s.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_80lat_n.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_split.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_split.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_scalar.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_scalar_split.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_scalar.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_scalar_split.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_offset_source.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_offset_destination.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_scalar_offset_source.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_scalar_offset_destination.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_offset_source.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_offset_destination.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_scalar_offset_source.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_scalar_offset_destination.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_split4.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_split4.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_vector_same_dir.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_vector_opp_dir.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_vector_same_dir.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_vector_opp_dir.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_antimeridian.json',
    './example_routes/dijkstra/crossing_point/diagonal/diagonal_0lat_scalar.json',
    './example_routes/dijkstra/crossing_point/diagonal/diagonal_0lat_split_scalar.json',
    './example_routes/dijkstra/crossing_point/diagonal/diagonal_0lat_vector_opp_dir.json',
    './example_routes/dijkstra/crossing_point/diagonal/diagonal_0lat_vector_same_dir.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_wind_opp_dir.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_wind_opp_dir_offset.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_wind_opp_dir.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_wind_opp_dir_offset.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_80latn_reverse.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_80lats_reverse.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_antimeridian_reverse.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_reverse.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_reverse.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_80latn_reverse.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_80lats_reverse.json',
    './example_routes/dijkstra/crossing_point/diagonal/diagonal_0lat_reverse.json',
    './example_routes/dijkstra/crossing_point/diagonal/diagonal_0lat_vector_reverse.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_scalar_reverse.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_vector_reverse.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_scalar_reverse.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_vector_reverse.json',
    './example_routes/dijkstra/crossing_point/diagonal/diagonal_0lat_scalar_reverse.json',
    './example_routes/dijkstra/crossing_point/horizontal/horizontal_0lat_wind_same_dir.json',
    './example_routes/dijkstra/crossing_point/vertical/vertical_0lat_wind_same_dir.json',
    './example_routes/dijkstra/fuel/twin_otter_f_route_dijkstra.json',
    './example_routes/dijkstra/battery/slocum_b_route_dijkstra.json',
    './example_routes/dijkstra/battery/alr_b_route_dijkstra.json',
    './example_routes/dijkstra/time/slocum_tt_route_dijkstra.json',
    './example_routes/dijkstra/time/alr_tt_route_dijkstra.json',
    './example_routes/dijkstra/time/twin_otter_tt_route_dijkstra.json'
]

def setup_module():
    LOGGER.info(f'PolarRoute version: {pr_version}')

# Pairing old and new outputs
@pytest.fixture(scope='session', autouse=False, params=TEST_ROUTES)
def route_pair(request):
    """
    Creates a pair of JSON objects, one newly generated, one as old reference
    Args:
        request (fixture): 
            fixture object including list of jsons of optimised routes

    Returns:
        list: [reference json, new json]
    """

    LOGGER.info(f'Test File: {request.param}')

    # Load reference JSON
    with open(request.param, 'r') as fp:
        old_route = json.load(fp)
    route_info = extract_route_info(old_route)
    # Create new json (cast old to dict to create copy to avoid modifying)
    new_route = calculate_dijkstra_route(route_info, dict(old_route))

    return [old_route, new_route]

# Generating new outputs
def calculate_dijkstra_route(config, mesh):
    """
    Calculates the optimised route, with dijkstra but no smoothing

    Args:
        config (dict): the route config
        mesh (dict): the reference mesh (including routes and waypoints)

    Returns:
        new_route (dict): new route output
    """
    start = time.perf_counter()

    # Initial set up
    waypoints   = extract_waypoints(mesh)

    # Calculate dijkstra route
    rp = RoutePlanner(mesh, config)
    routes = rp.compute_routes(waypoints)
    
    # Generate json to compare to old output
    new_route = mesh
    new_route['paths'] = {"type": "FeatureCollection", "features": []}
    new_route['paths']['features'] = [r.to_json() for r in routes]

    end = time.perf_counter()
    LOGGER.info(f'Route calculated in {end - start} seconds')

    return new_route