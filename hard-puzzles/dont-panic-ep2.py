import sys
import math
from bisect import bisect

input_data = [int(i) for i in input().split()]
nb_floors = input_data[0]
width = input_data[1]
nb_rounds = input_data[2]
exit_floor = input_data[3]
exit_pos = input_data[4]
nb_total_clones = input_data[5]
nb_additional_elevators = input_data[6]
nb_elevators = input_data[7]

# Read elevator positions
elevator_positions = {}
for i in range(nb_elevators):
    elevator_floor, elevator_pos = [int(j) for j in input().split()]
    elevator_positions[elevator_floor] = elevator_positions.get(
        elevator_floor, []) + [elevator_pos]


def dynamic_programming_shortest_path(start_pos, start_dir, additional_elevators):
    # Save distance to exit for each possible state
    distance_matrix = {
        "LEFT": [[[0] * width for _ in range(exit_floor + 1)] for _ in range(additional_elevators + 1)],
        "RIGHT": [[[0] * width for _ in range(exit_floor + 1)] for _ in range(additional_elevators + 1)]
    }
    elevators_on_floor = sorted(elevator_positions.get(exit_floor, []))

    # Fill last floor
    for current_pos in range(width):
        # Current pos is on elevator which means exit cannot be reached
        if current_pos in elevators_on_floor:
            for available_elevators in range(additional_elevators + 1):
                distance_matrix["LEFT"][available_elevators][exit_floor][current_pos] = distance_matrix[
                    "RIGHT"][available_elevators][exit_floor][current_pos] = (100000, 'take', current_pos)
        # Current pos is on exit
        elif current_pos == exit_pos:
            for available_elevators in range(additional_elevators + 1):
                distance_matrix["LEFT"][available_elevators][exit_floor][current_pos] = distance_matrix[
                    "RIGHT"][available_elevators][exit_floor][current_pos] = (0, 'take', exit_pos)
        # Move to exit
        else:
            i = bisect(elevators_on_floor, current_pos)
            j = bisect(elevators_on_floor, exit_pos)
            # Check if exit can be reached
            if i == j:
                for available_elevators in range(additional_elevators + 1):
                    distance_matrix["LEFT"][available_elevators][exit_floor][current_pos] = (abs(
                        current_pos - exit_pos) + (3 if current_pos < exit_pos else 0), 'take', exit_pos)
                    distance_matrix["RIGHT"][available_elevators][exit_floor][current_pos] = (abs(
                        current_pos - exit_pos) + (3 if current_pos > exit_pos else 0), 'take', exit_pos)
            else:
                for available_elevators in range(additional_elevators + 1):
                    distance_matrix["LEFT"][available_elevators][exit_floor][current_pos] = distance_matrix[
                        "RIGHT"][available_elevators][exit_floor][current_pos] = (100000, 'take', current_pos)

    # Fill other floor top down
    for floor in reversed(range(0, exit_floor)):
        elevators_on_floor = sorted(elevator_positions.get(floor, []))
        for current_pos in range(width):
            # Elevator on current position means the elevator has to be taken to the next floor
            if current_pos in elevators_on_floor:
                possible_paths_facing_left = [[(distance_matrix["LEFT"][available_elevators][floor+1][current_pos]
                                                [0] + 1, 'take', current_pos)] for available_elevators in range(additional_elevators + 1)]
                possible_paths_facing_right = [[(distance_matrix["RIGHT"][available_elevators][floor+1][current_pos]
                                                 [0] + 1, 'take', current_pos)] for available_elevators in range(additional_elevators + 1)]
            else:
                possible_paths_facing_left = [[]
                                              for _ in range(additional_elevators + 1)]
                possible_paths_facing_right = [
                    [] for _ in range(additional_elevators + 1)]
                # Handle building on current position
                for available_elevators in range(1, additional_elevators + 1):
                    possible_paths_facing_left[available_elevators].append(
                        (distance_matrix["LEFT"][available_elevators - 1][floor+1][current_pos][0] + 4, 'build', current_pos))
                    possible_paths_facing_right[available_elevators].append(
                        (distance_matrix["RIGHT"][available_elevators - 1][floor+1][current_pos][0] + 4, 'build', current_pos))
                left_pos = current_pos - 1
                # Check left options till elevator is reached
                while left_pos >= 0:
                    if left_pos in elevators_on_floor:
                        for available_elevators in range(additional_elevators + 1):
                            dist = (current_pos - left_pos) + \
                                distance_matrix["LEFT"][available_elevators][floor + 1][left_pos][0] + 1
                            possible_paths_facing_left[available_elevators].append(
                                (dist, 'take', left_pos))
                            possible_paths_facing_right[available_elevators].append(
                                (dist + 3, 'take', left_pos))
                        break
                    for available_elevators in range(1, additional_elevators + 1):
                        dist = (current_pos - left_pos) + \
                            distance_matrix["LEFT"][available_elevators - 1][floor+1][left_pos][0] + 4
                        possible_paths_facing_left[available_elevators].append(
                            (dist, 'build', left_pos))
                        possible_paths_facing_right[available_elevators].append(
                            (dist + 3, 'build', left_pos))
                    left_pos -= 1

                right_pos = current_pos + 1
                # Check right operions till elevator is reached
                while right_pos < width:
                    if right_pos in elevators_on_floor:
                        for available_elevators in range(additional_elevators + 1):
                            dist = (right_pos - current_pos) + \
                                distance_matrix["RIGHT"][available_elevators][floor +
                                                                              1][right_pos][0] + 1
                            possible_paths_facing_right[available_elevators].append(
                                (dist, 'take', right_pos))
                            possible_paths_facing_left[available_elevators].append(
                                (dist + 3, 'take', right_pos))
                        break
                    for available_elevators in range(1, additional_elevators + 1):
                        dist = (right_pos - current_pos) + \
                            distance_matrix["RIGHT"][available_elevators -
                                                     1][floor+1][right_pos][0] + 4
                        possible_paths_facing_right[available_elevators].append(
                            (dist, 'build', right_pos))
                        possible_paths_facing_left[available_elevators].append(
                            (dist + 3, 'build', right_pos))
                    right_pos += 1
            # Take fastest option
            for available_elevators in range(additional_elevators + 1):
                distance_matrix["LEFT"][available_elevators][floor][current_pos] = min(
                    possible_paths_facing_left[available_elevators], default=(100000, None, None))
                distance_matrix["RIGHT"][available_elevators][floor][current_pos] = min(
                    possible_paths_facing_right[available_elevators], default=(100000, None, None))

    # Assemble final path
    final_path = []
    current_pos = start_pos
    current_dir = start_dir
    current_available_elevators = additional_elevators
    for floor in range(exit_floor+1):
        dist, action, pos = distance_matrix[current_dir][current_available_elevators][floor][current_pos]
        if current_pos < pos:
            current_dir = "RIGHT"
        elif current_pos > pos:
            current_dir = "LEFT"
        current_pos = pos
        if action == 'build':
            current_available_elevators -= 1
        final_path.append((action, pos))
    return final_path


def clone_looks_at(clone_pos, direction, object_pos):
    return (clone_pos >= object_pos and direction == "LEFT") or \
        (clone_pos <= object_pos and direction == "RIGHT")


# Execute shortest path
shortest_path = None
while True:
    clone_floor, clone_pos, direction = input().split()
    clone_floor = int(clone_floor)
    clone_pos = int(clone_pos)

    if shortest_path is None:
        shortest_path = dynamic_programming_shortest_path(
            clone_pos, direction, nb_additional_elevators)
        print(shortest_path, file=sys.stderr)

    if direction == "NONE":
        print("WAIT")
    else:
        next_elevator_pos = shortest_path[clone_floor]
        if next_elevator_pos[0] == 'build' and clone_pos == next_elevator_pos[1]:
            print("ELEVATOR")
            shortest_path[clone_floor] = ('take', clone_pos)
        elif not clone_looks_at(clone_pos, direction, next_elevator_pos[1]):
            print("BLOCK")
        else:
            print("WAIT")
