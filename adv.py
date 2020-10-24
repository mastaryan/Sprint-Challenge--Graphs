from room import Room
from player import Player
from world import World

from collections import deque
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# Tracks each step while exploring
traversal_path = []
graph = dict()
# false id allows while loop to start
cur_room = -1
#need to be able to move backwards
inverse_moves = {'n': 's', 'w': 'e', 's': 'n', 'e': 'w'}

queue = deque([[]])


# Grab a first direction to go into.
while len(graph) < len(room_graph) and cur_room != player.current_room.id:
    next_dir = None
    adj_unvisited = 0
    cur_room = player.current_room

    if cur_room.id not in graph:
        graph[cur_room.id] = {'n': '?', 'w': '?', 's': '?', 'e': '?'}

        for direction in 'news':
            adj = cur_room.get_room_in_direction(direction)

            if adj:
                graph[cur_room.id][direction] = adj.id
                if adj.id not in graph:
                    adj_unvisited += 1
                    next_dir = direction

    else:
        for k, v in graph[cur_room.id].items():
            if v != '?' and v not in graph:
                adj_unvisited += 1
                next_dir = k

    if next_dir:
        if adj_unvisited > 1:
            queue.append([inverse_moves[next_dir]])
        else:
            queue[-1].append(inverse_moves[next_dir])
        traversal_path.append(next_dir)
        player.travel(next_dir)
        continue
    else:
        path_back = queue.pop()
        for move in range(len(path_back) - 1, -1, -1):
            traversal_path.append(path_back[move])
            player.travel(path_back[move])

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")