"""
A Map related NP Hard problem solver
@author : Weicheng Huang
"""
import random, math


class GeoPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "("+ str(self.x) + "," + str(self.y) + ")"


def map_creator_():
    size = int(raw_input("Tell me how detail you want:"))
    lt = GeoPoint(0, 0)
    lt.x = float(raw_input("Tell me your map top left corner geo x:"))
    lt.y = float(raw_input("Tell me your map top left corner geo y:"))
    rb = GeoPoint(0, 0)
    rb.x = float(raw_input("Tell me your map right bottom corner geo x:"))
    rb.y = float(raw_input("Tell me your map right bottom corner geo y:"))
    map_ = Map(size, lt, rb)
    print "import map element:"
    print "1,each line contains one element"
    print "2,line format: [geo.x]:[geo.y]:[map element name]"
    print "3,H for hospital, F for floodplain, S for school, U for utilities, E for existing structure, R for ohio medical waste regulation, C for central ohio"

    ff = raw_input("Tell me the file name contains the map element:")
    with open(ff) as f:
        for line in f.readlines():
            try:
                data = line.split(":")
                ge = GeoPoint(0, 0)
                ge.x = float(data[0])
                ge.y = float(data[1])
                ele = data[2].strip()
                map_.add_element_by_geo(ge, ele)
                print "Add element:", ele,"at", ge
            except:
                print "Broken Data Line,skipped:", line

    print "Done importing data"
    return map_


import collections


class Map:
    def __init__(self, size, left_top_geo, right_bot_geo):
        print "Initilizing map..."
        self.data_grid = [0] * size
        for i in range(size):
            self.data_grid[i] = [0] * size
            for j in range(size):
                self.data_grid[i][j] = []

        self.lt = left_top_geo
        self.rb = right_bot_geo
        self.size = size
        self.element_list = collections.defaultdict(set)

    def get_element(self, x, y):
        return self.data_grid[x][y]

    def add_element_by_xy(self, x, y, ele):
        self.data_grid[x][y].append(ele)
        self.element_list[ele].add((x, y))

    def get_element_index_list(self, ele):
        return list(self.element_list[ele])

    def contain_element(self, x, y, ele):
        return ele in self.data_grid[x][y]

    def print_map(self):
        for row in self.data_grid:
            for col in row:
                print col,
            print ""
        print ""

    def to_geo(self, x, y):
        x_total = self.rb.x - self.lt.x
        y_total = self.rb.y - self.lt.y

        _res_x = self.lt.x + (float(x) / self.size) * x_total
        _res_y = self.lt.y + (float(y) / self.size) * y_total
        res = GeoPoint(_res_x, _res_y)
        return res

    def from_geo(self,geo):
        if geo.x < self.lt.x or geo.x > self.rb.x or geo.y < self.lt.y or geo.y > self.rb.y:
            print "Wrong Geo location,skipped!"
            return

        x_total = self.rb.x - self.lt.x
        y_total = self.rb.y - self.lt.y

        x = int(math.floor((float(geo.x - self.lt.x) / x_total) * self.size))
        y = int(math.floor((float(geo.y - self.lt.y) / y_total) * self.size))

        return (x,y)
    def add_element_by_geo(self, geo, element):
        x,y = self.from_geo(geo)

        self.add_element_by_xy(x, y, element)


class Constrain:
    def __init__(self):
        self.is_hard = True

        self.important = 1.0

    def eval_solution(self, solution, m):
        if self.is_hard:
            return self.hard_eval(solution, m) * float(self.important)
        else:
            return self.soft_eval(solution, m) * float(self.important)

    def hard_eval(self, solution, m):
        raise NotImplementedError

    def soft_eval(self, solution, m):
        raise NotImplementedError


class Algorithm:
    def __init__(self, constrain_space, map_):
        '''
        :param constrain_space: a list of constrain class object
        :param map_: the map
        '''
        self.constrain_space = constrain_space
        self.solution_space = []
        self.solution_score = []
        self.map = map_
        print "Calculating Solution Space..."
        self.find_solution_space()
        print "Solution Space founded!"
        print "Find Best Optimal Solution..."
        res = self.run()
        print "Best Solution Founded, the solution is:" + str(self.map.to_geo(res[0], res[1]))
        print "In this grid:", self.map.get_element(res[0],res[1])

    def run(self):
        raise NotImplementedError

    def find_solution_space(self):
        for i in range(self.map.size):
            for j in range(self.map.size):
                if self.is_solution((i, j)):
                    self.solution_space.append((i, j))
        self.solution_score = [-1] * len(self.solution_space)

    def is_solution(self, solution):
        pass_hard_constrain = True
        for constrain in self.constrain_space:
            if constrain.is_hard:
                pass_hard_constrain = pass_hard_constrain and constrain.eval_solution(solution, self.map)
            if not pass_hard_constrain:
                return False
        return True

    def evaluate_solution(self, solution):
        score = 0
        for constrain in self.constrain_space:
            if not constrain.is_hard:
                score += constrain.eval_solution(solution, self.map)
        return score

    def get_score(self, index):
        if self.solution_score[index] != -1:
            return self.solution_score[index]
        else:
            score = self.evaluate_solution(self.solution_space[index])
            self.solution_score[index] = score
            return score


import sys


class LocalMinimum(Algorithm):
    LOOP_TIME = 100

    def run(self):
        res_point = -1
        res_score = sys.maxint
        for i in range(LocalMinimum.LOOP_TIME):
            this_solution_point = self.single_run()
            this_solution_score = self.get_score(this_solution_point)

            if res_point == -1 or res_score > this_solution_score:
                res_point = this_solution_point
                res_score = this_solution_score

        return self.solution_space[res_point]

    def single_run(self):
        current_point = random.randint(1, len(self.solution_space) - 2)
        current_score = self.get_score(current_point)

        while (current_point > 0) and (current_point < (len(self.solution_space) - 1)):
            left = self.get_score(current_point - 1)
            right = self.get_score(current_point + 1)

            if current_score <= min(left, right):
                return current_point

            elif left > right:
                current_point += 1
                current_score = right
            else:
                current_point -= 1
                current_score = left

        return current_point

