from polar_route.vessel_performance.vessels.abstract_uav import AbstractUAV
from meshiphi.mesh_generation.aggregated_cellbox import AggregatedCellBox
import numpy as np
import logging

class Windracer(AbstractUAV):
    """
        Vessel class with methods specifically designed to model the performance of the Windracers Ultra UAV

        https://windracers.com/drones/

        Cruising Speed - 135 km/hr
        Power Usage - 350w
        Note: This power is actually generated by a set of engines not drawn from a battery, model should be updated in
        the future to account for this.
        Duration - 12+ flight duration
    """
    def __init__(self, params):
        """
            Args:
                params (dict): vessel parameters from the vessel config file
        """

        super().__init__(params)

    def model_speed(self, cellbox):
        """
            Method to determine the maximum speed that the UAV can traverse the given cell

            Args:
                cellbox (AggregatedCellBox): input cell from environmental mesh

            Returns:
                cellbox (AggregatedCellBox): updated cell with speed values
        """

        cellbox.agg_data['speed'] = [self.max_speed for x in range(8)]
        return cellbox

    def model_battery(self, cellbox):
        """
            Method to determine the rate of power usage in a given cell in Watts

            Args:
                cellbox (AggregatedCellBox): input cell from environmental mesh

            Returns:
                cellbox (AggregatedCellBox): updated cell with battery consumption values
        """

        battery = [350 for s in cellbox.agg_data['speed']]

        cellbox.agg_data['battery'] = battery
        return cellbox
