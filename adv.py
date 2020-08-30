from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# class Stack():
#     def __init__(self):
#         self.stack = []

#     def push(self, value):
#         self.stack.append(value)

#     def pop(self):
#         if self.size() > 0:
#             return self.stack.pop()
#         else:
#             return None

#     def size(self):
#         return len(self.stack)


# class Queue():
#     def __init__(self):
#         self.queue = []

#     def enqueue(self, value):
#         self.queue.append(value)

#     def dequeue(self):
#         if self.size() > 0:
#             return self.queue.pop(0)
#         else:
#             return None

#     def size(self):
#         return len(self.queue)


# def bfs(starting_vertex, visited):
#     q = Queue()
#     q.enqueue([starting_vertex])

#     while q.size() > 0:
#         current_path = q.dequeue()
#         current_vertex = current_path[-1]

#         if current_vertex not in visited:
#             exits = current_vertex.get_exits()
#             if "?" in visited[current_vertex.id].values():
#                 for ex in visited[current_vertex.id].values():
#                     if ex == "?":
#                         return current_path
#         else:
#             visited.append(current_vertex)
#             for ex in exits:
#                 q.enqueue(ex)


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
opposite = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

# Find the path


def find_path(path, full=True):
    backtrack = []

    for i in reversed(range(len(path))):
        backtrack.append(opposite[path[i]])

    path.extend(backtrack)
    if full:
        return path

    return backtrack

# Traverse the graph


def traverse(starting_node, path=None, visited=None):
    if visited is None:
        visited = set()
    if path is None:
        path = list()

    visited.add(starting_node.name)
    exits = starting_node.get_exits()
    random.shuffle(exits)

    for direction in exits:
        next_room = starting_node.get_room_in_direction(direction)

        if len(exits) > 2:
            path = []
        if len(exits) == 2 and starting_node.get_room_in_direction(exits[0]).name in visited and len(exits) == 2 and starting_node.get_room_in_direction(exits[1]).name in visited:
            traversal_path.extend(find_path(path))
            return
        elif len(exits) == 1 and starting_node.get_room_in_direction(direction).name in visited:
            traversal_path.extend(find_path(path))
            return
        elif next_room.name not in visited:
            path.append(direction)
            new_exits = next_room.get_exits()

            if len(new_exits) == 2:
                path_clone = path.copy()
                traverse(next_room, path_clone, visited)
            elif len(new_exits) > 2:
                path_clone = path.copy()
                traversal_path.extend(path)
                traverse(next_room, visited=visited)
                traversal_path.extend(find_path(path_clone, False))
            else:
                path_clone = path.copy()
                traverse(next_room, path_clone, visited)


traverse(world.starting_room)

# print(world.room_grid[4][5])

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
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


# def traverse_grid():
#     curr = player.current_room
#     directions = curr.get_exits()
#     visited = {}
#     visited[curr.id] = {direction: "?" for direction in directions}

#     random.shuffle(directions)

#     s = Stack()
#     for el in directions:
#         s.push(el)

#     while s.size() > 0:
#         unvisited = []
#         next_direction = s.pop()

#         prev_room = curr
#         player.travel(next_direction)
#         # Add movement to traversal path
#         traversal_path.append(next_direction)
#         curr = player.current_room
#         # Get all exits for current room
#         exits = curr.get_exits()

#         visited[prev_room.id][next_direction] = curr.id

#         if curr.id not in visited:
#             visited[curr.id] = {
#                 exit: "?" for exit in exits}

#         for (ex, room_id) in visited[curr.id].items():
#             if room_id == "?":
#                 unvisited.append(ex)

#         opposite_direction = opposite[next_direction]

#         if opposite_direction in exits:
#             visited[curr.id][opposite_direction] = prev_room.id

#         if len(unvisited) > 0:
#             s.push(unvisited[-1])

#         else:
#             path_back = bfs(curr, visited)
#             if path_back is not None:
#                 for direction in path_back:
#                     player.travel(direction)
#                     traversal_path.append(direction)
#             curr = player.current_room
#             for (ex, room_id) in visited[curr.id].items():
#                 if room_id == "?":
#                     unvisited.append(ex)

#             if len(unvisited) > 0:
#                 s.push(unvisited[0])
