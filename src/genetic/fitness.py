from typing import List, Tuple

import numpy as np


def fitness(positions: List[float], setpoints: List[float], weight_factor: float = 1) -> float:
    """
    Calculates the Fitness Value of the Simulated Data. The smaller the Fitness-Value the better
    :param positions: The actual Positions of the simulated Ball
    :param setpoints: The desired Positions for the ball
    :param weight_factor: The Factor which decides how much weight gets applied to the error of the approaching areas
    :return: Fitness Value of the PID-Controller
    """
    assert weight_factor >= 0
    positions, setpoints = prepare_data(positions, setpoints)
    setpoint_changes = get_setpoint_changing_points(setpoints)
    positions_diff, positions_abs_diff = get_differentiated_positions(positions)
    intersection_points = get_intersection_points(positions, setpoints, positions_abs_diff, threshold=0.02)
    approaching_areas = get_approaching_areas(setpoints, setpoint_changes, intersection_points)
    fitness_value = calculate_fitness(positions, setpoints, approaching_areas, weight_factor)

    return fitness_value


def prepare_data(positions: List[float], setpoints: List[float]) -> Tuple[np.ndarray, np.ndarray]:
    positions.insert(0, 0)
    setpoints.insert(0, 0)

    return np.array(positions), np.array(setpoints)


def get_setpoint_changing_points(setpoints: np.ndarray) -> np.ndarray:
    setpoint_changes = np.where(np.subtract((setpoints[:-1]), setpoints[1:]) != 0)[0]

    return setpoint_changes


def get_differentiated_positions(positions: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    positions_diff = np.diff(positions)
    positions_abs_diff = np.abs(positions_diff)

    return positions_diff, positions_abs_diff


def get_intersection_points(positions: np.ndarray, setpoints: np.ndarray, positions_abs_diff: np.ndarray, threshold: float) -> np.ndarray:
    setpoint_position_difference = setpoints - positions
    intersection_points = np.where(
        (np.multiply(
            setpoint_position_difference[1:],
            setpoint_position_difference[:-1]
        ) <= 0) & (positions_abs_diff > threshold)
    )[0]

    return intersection_points


def get_approaching_areas(setpoints: np.ndarray, setpoint_changes: np.ndarray, intersection_points: np.ndarray) -> List[Tuple[int, int]]:
    approaching_areas = []
    for idx, setpoint_change in enumerate(setpoint_changes):
        next_intersection = next((x for x in intersection_points if x > setpoint_change), None)
        next_setpoint_change = next((x for x in setpoint_changes if x > setpoint_change), None)
        # If there is an intersection following the setpoint change
        if next_intersection is not None:
            # If also a next setpoint change exists take the value which is closer to the current setpoint change
            if next_setpoint_change is not None:
                approaching_areas.append((setpoint_change, next_intersection if next_intersection < next_setpoint_change else next_setpoint_change))
            # Just take the next intersection, if there is no next setpoint change
            else:
                approaching_areas.append((setpoint_change, next_intersection))
        else:
            # If there is no intersection following the setpoint change
            if next_setpoint_change is not None:
                approaching_areas.append((setpoint_change, next_setpoint_change))
            # If there is neither an intersection nor a setpoint change following the setpoint change
            else:
                approaching_areas.append((setpoint_change, len(setpoints) - 1))

    return approaching_areas


def calculate_fitness(positions: np.ndarray, setpoints: np.ndarray, approaching_areas: List[Tuple[int, int]], weight_factor: float) -> float:
    error_weights = np.ones(len(setpoints))
    for area in approaching_areas:
        error_weights[area[0]:area[1] + 1] = weight_factor

    error_values = error_weights * np.abs(setpoints - positions)
    fitness_value = np.sum(error_values)

    return fitness_value
