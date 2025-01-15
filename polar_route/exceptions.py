"""
    This module contains the custom exceptions for the polar_route package.
"""

class WayPointOutOfBounds(Exception):
    "Raised when the waypoint is out of bounds of the mesh"

    def __init__(self, message="Waypoint is out of bounds of the mesh"):
        self.message = message
        super().__init__(self.message)

class NoRouteFound(Exception):
    "Raised when the route is not found"

    def __init__(self, message="No route found"):
        self.message = message
        super().__init__(self.message)