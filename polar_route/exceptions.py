"""
    This module contains the custom exceptions for the polar_route package.
"""

class WayPointOutOfBounds(Exception):
    "Raised when the waypoint is out of bounds of the mesh"

    def __init__(self, waypoint, message="Waypoint is out of bounds of the mesh"):
        self.message = "Waypoint at " + str(waypoint) + " is out of bounds of the mesh"
        super().__init__(self.message)

class NoRouteFound(Exception):
    "Raised when a route cannot be found between two waypoints"

    def __init__(self, message="No route found"):
        self.message = message
        super().__init__(self.message)

class InaccessibleWaypoint(Exception):
    "Raised when a waypoint is inaccessible"

    def __init__(self, waypoint, message="Waypoint is inaccessible"):
        self.message = "Waypoint at " + str(waypoint) + " is inaccessible"
        super().__init__(self.message)

class RouteCouldNotSmooth(Exception):
    "Raised when a route cannot be smoothed"

    def __init__(self, message="Route could not be smoothed"):
        self.message = message
        super().__init__(self.message)

class InvalidMesh(Exception):
    "Raised when the mesh is invalid"

    def __init__(self, message="Invalid mesh"):
        self.message = message
        super().__init__(self.message)