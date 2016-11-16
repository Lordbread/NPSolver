import NPSolve as NP
import math

constrain_space = []


class DistanceConstrain(NP.Constrain):
    def __init__(self):
        NP.Constrain.__init__(self)
        self.is_hard = False

    def soft_eval(self, solution, m):
        score = 0.0

        for hosptial_index in m.get_element_index_list("H"):
            score += math.fabs(hosptial_index[0] - solution[0]) + math.fabs(hosptial_index[1] - solution[1])
        return score


constrain_space.append(DistanceConstrain())


class FloodPlainConstrain(NP.Constrain):
    def __init__(self):
        NP.Constrain.__init__(self)
        self.is_hard = True

    def hard_eval(self, solution, m):
        return not m.contain_element(solution[0], solution[1], "F")


constrain_space.append(FloodPlainConstrain())
map_ = NP.map_creator_()

engine = NP.LocalMinimum(constrain_space, map_)
