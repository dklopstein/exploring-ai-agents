from __future__ import print_function
from heapq import * #Hint: Use heappop and heappush
import queue

ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)]

class AI:
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    def set_search(self):
        self.final_cost = 0
        self.grid.reset()
        self.finished = False
        self.failed = False
        self.previous = {}

        # Initialization of algorithms goes here
        if self.type == "dfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = queue.Queue()
            self.frontier.put(self.grid.start)
            self.explored = []
        elif self.type == "ucs":
            self.frontier = [(0, self.grid.start)]
            self.explored = []
            self.dist = {self.grid.start: 0}
        elif self.type == "astar":
            self.frontier = [(0, 0, self.grid.start)]
            self.explored = []
            self.dist = {self.grid.start: 0}

    def get_result(self):
        total_cost = 0
        current = self.grid.goal
        while not current == self.grid.start:
            if self.type == "bfs":
                total_cost += 1
            else:
                total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = True #This turns the color of the node to red
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()

    # TODO: Buggy DFS, fix it first
    def dfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop()

        # Finishes search if we've found the goal.
        if current == self.grid.goal:
            self.finished = True
            return

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.explored.append(current)
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle and not self.grid.nodes[n].color_checked and not self.grid.nodes[n].color_frontier:
                    self.previous[n] = current
                    self.frontier.append(n)
                    self.grid.nodes[n].color_frontier = True
                    if n == self.grid.goal:
                        self.finished = True
                        return

    # TODO: Implement BFS here (Don't forget to implement initialization in set_search function)
    def bfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.get()

        # Finishes search if we've found the goal.
        if current == self.grid.goal:
            self.finished = True
            return

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.explored.append(current)
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle and not self.grid.nodes[n].color_checked and not self.grid.nodes[n].color_frontier:
                    self.previous[n] = current
                    self.frontier.put(n)
                    self.grid.nodes[n].color_frontier = True
                    if n == self.grid.goal:
                        self.finished = True
                        return

    # TODO: Implement UCS here (Don't forget to implement initialization in set_search function)
    #Hint: You can use heappop and heappush from the heapq library (imported for you above)
    def ucs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = heappop(self.frontier)

        # Finishes search if we've found the goal.
        if current[1] == self.grid.goal:
            self.finished = True
            return

        children = [(current[1][0]+a[0], current[1][1]+a[1]) for a in ACTIONS]
        self.explored.append(current[1])
        self.grid.nodes[current[1]].color_checked = True
        self.grid.nodes[current[1]].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                cost = current[0] + self.grid.nodes[n].cost()
                if not self.grid.nodes[n].puddle and not self.grid.nodes[n].color_checked and not self.grid.nodes[n].color_frontier:
                    self.previous[n] = current[1]
                    heappush(self.frontier, (cost, n))
                    self.grid.nodes[n].color_frontier = True
                    self.dist[n] = cost
                elif self.grid.nodes[n].color_frontier and cost < self.dist[n]:
                    # remove same node from frontier and heappush with new distance
                    print('activating')
                    for i in range(len(self.frontier)):
                        if self.frontier[i][1] == n: 
                            self.frontier.pop(i)
                            break

                    heappush(self.frontier, (current[0] + self.grid.nodes[n].cost(), n))
                    self.dist[n] = cost

    
    # TODO: Implement Astar here (Don't forget to implement initialization in set_search function)
    #Hint: You can use heappop and heappush from the heapq library (imported for you above)
    def astar_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = heappop(self.frontier)

        # Finishes search if we've found the goal.
        if current[2] == self.grid.goal:
            self.finished = True
            return

        children = [(current[2][0]+a[0], current[2][1]+a[1]) for a in ACTIONS]
        self.explored.append(current[2])
        self.grid.nodes[current[2]].color_checked = True
        self.grid.nodes[current[2]].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                h = abs(self.grid.goal[0] - n[0]) + abs(self.grid.goal[1] - n[1])
                g = current[1] + self.grid.nodes[n].cost()
                if not self.grid.nodes[n].puddle and not self.grid.nodes[n].color_checked and not self.grid.nodes[n].color_frontier:
                    self.previous[n] = current[2]
                    heappush(self.frontier, (h + g, g, n))
                    self.grid.nodes[n].color_frontier = True
                    self.dist[n] = h + g
                elif self.grid.nodes[n].color_frontier and h + g < self.dist[n]:
                    # remove same node from frontier and heappush with new distance
                    for i in range(len(self.frontier)):
                        if self.frontier[i][2] == n:
                            self.frontier.pop(i)
                            break

                    heappush(self.frontier, (h + g, g, n))
                    self.dist[n] = h + g
