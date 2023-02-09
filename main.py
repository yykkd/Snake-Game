from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import Scoreboard
from queue import PriorityQueue

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("AI Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()


class Node:
    def __init__(self, current_state, parent, g_value, h_value, head_orientation):
        self.current_state = current_state
        self.parent = parent
        self.g_value = g_value
        self.h_value = h_value
        self.orientation = head_orientation

    def __hash__(self):
        return self.current_state.__hash__()

    def f_value(self):
        return self.g_value + self.h_value

    def __lt__(self, other):
        return self.f_value() < other.f_value()


# gets the estimated cost of a state
def heuristic_cost(state):
    xcor, ycor = state
    return abs(xcor - food.xcor()) + abs(ycor - food.ycor())


# definition of a test for what the goal state is
def goal_test(node_state):
    node_x = node_state[0]
    node_y = node_state[1]
    return food.distance(node_x, node_y) < 10


def solution_path(n):
    movements_list = []

    while n.parent is not None:
        movements_list.append(n.orientation)
        n = n.parent
    movements_list.reverse()  # shows states in ascending order
    return movements_list


def get_neighbouring_states(current_node):
    list_of_nodes = []
    curr_x = current_node.current_state[0]
    curr_y = current_node.current_state[1]

    if current_node.orientation != "up":
        new_state = (curr_x, curr_y - 20)
        if -300 <= new_state[0] <= 280 or -280 <= new_state[1] <= 250:
            list_of_nodes.append(Node(new_state, current_node, food.distance((new_state[0],
                                                                              new_state[1])),
                                 heuristic_cost(new_state), "down"))

    if current_node.orientation != "down":
        new_state = (curr_x, curr_y + 20)
        if -300 < new_state[0] < 280 or -280 < new_state[1] < 250:
            list_of_nodes.append(Node(new_state, current_node, food.distance((new_state[0], new_state[1])),
                                      heuristic_cost(new_state), "up"))

    if current_node.orientation != "left":
        new_state = (curr_x + 20, curr_y)
        if -300 < new_state[0] < 280 or -280 < new_state[1] < 250:
            list_of_nodes.append(Node(new_state, current_node, food.distance((new_state[0], new_state[1])),
                                      heuristic_cost(new_state), "right"))

    if current_node.orientation != "right":
        new_state = (curr_x - 20, curr_y)
        if -300 < new_state[0] < 280 or -280 < new_state[1] < 250:
            list_of_nodes.append(Node(new_state, current_node, food.distance((new_state[0], new_state[1])),
                                      heuristic_cost(new_state), "left"))

    return list_of_nodes


def a_star_search(start_node):
    # create corresponding map to compare positions
    open_list = PriorityQueue()
    closed_list = set()

    positions_map_open_list = dict()
    positions_map_closed_list = dict()

    open_list.put(start_node, start_node.f_value())
    positions_map_open_list[start_node.current_state] = start_node

    while open_list.qsize() != 0:
        min_node = open_list.get()
        positions_map_open_list.pop(min_node.current_state)

        if goal_test(min_node.current_state):
            return solution_path(min_node)

        successor_nodes = get_neighbouring_states(min_node)

        for successor_node in successor_nodes:
            if goal_test(successor_node.current_state):
                return solution_path(successor_node)

            if successor_node.current_state in positions_map_closed_list:
                continue

            if successor_node.current_state not in positions_map_open_list and successor_node.current_state not in positions_map_closed_list:
                open_list.put(successor_node, successor_node.f_value())
                positions_map_open_list[successor_node.current_state] = successor_node

            elif successor_node.current_state in positions_map_open_list:
                holder_node = positions_map_open_list.get(successor_node.current_state)
                holder_node_fvalue = holder_node.f_value()
                successor_node_fvalue = successor_node.f_value()

                if successor_node_fvalue < holder_node_fvalue:
                    print("\t open + 1 comp")
                    open_list.put(successor_node, successor_node.f_value())
                    open_list.queue.remove(holder_node)
                    positions_map_open_list.pop(holder_node.current_state)
                    positions_map_open_list[successor_node.current_state] = successor_node

        closed_list.add(min_node)
        positions_map_closed_list[min_node.current_state] = min_node

    return None  # this is returned when there is failure


game_is_on = True

node = Node((0, 0), None, food.distance(0, 0), heuristic_cost((0, 0)), "right")
orientation_path = a_star_search(node)
length = len(orientation_path)
print(f"Start: {snake.head.pos()}")
print(f"Goal: {food.pos()}")
print(f"A* Path: {orientation_path}\n")

for turn in range(10):

    for move in range(length):
        screen.update()
        time.sleep(0.1)

        if orientation_path[move] == "up":
            snake.move_up()
        elif orientation_path[move] == "down":
            snake.move_down()
        elif orientation_path[move] == "left":
            snake.move_left()
        elif orientation_path[move] == "right":
            snake.move_right()

        snake.move_snake()

        if snake.head.xcor() > 280 or snake.head.xcor() < -300 or snake.head.ycor() > 250 or snake.head.ycor() < -280:
            scoreboard.reset()
            scoreboard.game_over()
            game_is_on = False
            exit(0)

    food.refresh()
    snake.extend()
    scoreboard.update_score()
    screen.update()
    time.sleep(0.1)

    x = snake.head.xcor()
    y = snake.head.ycor()

    orientation = ""

    if snake.head.heading() == 90:
        orientation = "up"
    elif snake.head.heading() == 270:
        orientation = "down"
    elif snake.head.heading() == 180:
        orientation = "left"
    elif snake.head.heading() == 0:
        orientation = "right"

    node = Node((x, y), None, food.distance(x, y), heuristic_cost((x, y)), orientation)
    orientation_path = a_star_search(node)
    length = len(orientation_path)

    print(f"Start: {snake.head.pos()}")
    print(f"Goal: {food.pos()}")
    print(f"A* Path: {orientation_path}\n")

screen.exitonclick()
