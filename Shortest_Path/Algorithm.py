import time
import heapq
import pygame
import random
from env import *
from Queue import *
from collections import defaultdict
from abc import ABCMeta, abstractmethod

INF = float('inf')
DELAY = 0.01
DISTANCE = 1

class Search(metaclass=ABCMeta):
    """
    class for search algorithms
    """
    @abstractmethod
    def solver(self):
        """
        Solver to find shortest path between start and target node
        """
        pass
    
    @abstractmethod
    def initialize(self):
        """
        Create information required for solver
        """
        pass

    def output(self):
        # get cells first in case path to be drawn directly
        cells = self.board.draw_board()   

        # derive shortest path starting from target node and reverse it
        node = self.target_node
        while node.parent is not None:
            self.board.path.append(node.state)
            node = node.parent
        self.board.path.reverse()

        # draw shortest path step by step
        color = self.board.colors["p_yellow"]                     
        for i, j in self.board.path:
            time.sleep(1.5*DELAY)
            rect = cells[i][j]
            pygame.draw.rect(self.board.screen, color, rect)
            pygame.display.flip()

class Dijkstra(Search):
    """
    Dijkstra Algorithm
    """
    def __init__(self, board:Board):
        self.board = board
        self.find = False

    def initialize(self):
        """
        Create following information for solver:
        1. adjacent list
        2. node_dict: key is coordinate of node; value is node
        3. distance dict to store distance between nodes and start_node
        """
        self.node_dict = {}
        self.distance = {}

        # create nodes
        for i in range(self.board.v_cells):
            for j in range(self.board.h_cells):
                # if (i,j) is wall, do not create Node
                if (i,j) in self.board.wall:
                    continue

                pos = (i,j)
                node = Node(pos, None, None)
                if pos == self.board.start:
                    self.start_node = node
                elif pos == self.board.target:
                    self.target_node = node

                self.node_dict[pos] = node
                self.distance[node] = INF

        self.distance[self.start_node] = 0

        # add neighbor_nodes to adjacent list with action and distance
        self.adj_list = defaultdict(dict)
        for _, node in self.node_dict.items():
            # get possible neighbor positions of node
            neighbors = self.board.neighbors(node.state)
            for action, (row, col) in neighbors:
                # get neighbor_node from node_dict
                neighbor_node = self.node_dict[(row, col)]
                # update adj_list
                self.adj_list[node][neighbor_node] = [action, DISTANCE]

    def relax(self, node:Node, neighbor: Node):
        """
        Function to update distance dict for each node, and push node into heap by distance
        """
        if self.distance[neighbor] > self.distance[node] + self.adj_list[node][neighbor][1]:

            # update distance
            self.distance[neighbor] = self.distance[node] + self.adj_list[node][neighbor][1]

            # update parent and action take
            neighbor.parent = node
            neighbor.action = self.adj_list[node][neighbor][0]
            
            # push neighbor into heap
            self.entry_count += 1
            heapq.heappush(self.heap, (self.distance[neighbor], self.entry_count, neighbor))

    def solver(self):
        """
        Dijkstra algorithm
        """
        # When pusing node into heap and there exists equal distance values, 
        # then heap will arrange those nodes in order of entry time.
        self.heap = []
        self.entry_count = 1
        heapq.heappush(self.heap, (self.distance[self.start_node], self.entry_count, self.start_node))

        while self.heap and self.find == False:
            time.sleep(DELAY)
            # Extract_Min
            (_, _, node) = heapq.heappop(self.heap)
            
            # If find target node, set self.find == True
            if node.state == self.target_node.state:
                self.find = True

            # Mark node as visited
            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)
            # if there is no outgoing edge, continue while loop
            if not self.adj_list[node]:
                continue

            # if there exists outgoing edges, iteration through all edges
            for neighbor in self.adj_list[node]:
                if neighbor not in self.board.visited:
                    self.relax(node, neighbor)
            pygame.display.flip()


class A_search(Search):
    """
    A* Search algorithm
    """
    def __init__(self, board:Board):
        self.board = board
        self.find = False

    def initialize(self):
        """
        Create following information for solver:
        1. adjacent list
        2. node_dict: key is coordinate of node; value is node
        3. g_scores dictionary
        4. h_scores dictionary
        """
        self.node_dict = {}
        self.g_scores = {}
        self.h_scores = {}

        for i in range(self.board.v_cells):
            for j in range(self.board.h_cells):
                if (i,j) in self.board.wall:
                    continue

                pos = (i,j)
                node = Node(pos, None, None)
                if pos == self.board.start:
                    self.start_node = node
                elif pos == self.board.target:
                    self.target_node = node
                
                self.node_dict[pos] = node
                self.g_scores[node] = INF
                self.h_scores[node] = 0

        self.g_scores[self.start_node] = 0

        self.adj_list = defaultdict(dict)
        for _, node in self.node_dict.items():
            neighbors = self.board.neighbors(node.state)
            for action, (row, col) in neighbors:
                neighbor_node = self.node_dict[(row, col)]
                self.adj_list[node][neighbor_node] = [action, DISTANCE]

    def relax(self, node:Node, neighbor: Node):
        """
        Function to update g_scores dict for each node, and push node into heap by g_scores+h_scores

        node: selected visited node --> Node
        neighbor: neighboring nodes haven't been visited --> Node
        """
        if self.g_scores[neighbor] > self.g_scores[node] + self.adj_list[node][neighbor][1]:

            # update distance
            self.g_scores[neighbor] = self.g_scores[node] + self.adj_list[node][neighbor][1]

            # update parent and action take
            neighbor.parent = node
            neighbor.action = self.adj_list[node][neighbor][0]

            # push neighbor into heap
            self.entry_count += 1
            self.h_scores[neighbor] = A_search.manhattan(neighbor, self.target_node)
            heapq.heappush(self.heap, (self.g_scores[neighbor]+self.h_scores[neighbor], self.entry_count,neighbor))

    @staticmethod
    def manhattan(node_1:Node, node_2:Node)->int:
        """
        Compute manhattan distance between two nodes

        node_1: first node to be computed --> Node
        node_2: second node to be computed --> Node
        """
        start_x, start_y = node_1.state
        target_x, target_y = node_2.state
        return abs(start_x-target_x) + abs(start_y-target_y)
    
    def solver(self):
        """
        A* Search algorithm
        """
        # When pusing node into heap and there exists equal distance values, 
        # then heap will arrange those nodes in order of entry time.
        self.heap = []
        self.entry_count = 1
        h_score_s2t = A_search.manhattan(self.start_node, self.target_node) # h_score from start to target
        heapq.heappush(self.heap, (h_score_s2t, self.entry_count, self.start_node))

        while self.heap and not self.find:
            time.sleep(DELAY)
            # Extract_Min
            _, _, node = heapq.heappop(self.heap)

            # If find target node, set self.find == True
            if node.state == self.target_node.state:
                self.find = True

            # Mark node as visited
            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)

            # if there is no outgoing edge, continue while loop
            if not self.adj_list[node]:
                continue

            # if there exists outgoing edges, iteration through all edges
            for neighbor in self.adj_list[node]:
                if neighbor not in self.board.visited:
                    self.relax(node, neighbor)

            pygame.display.flip()