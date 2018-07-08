import numpy as np
import itertools
import re
import copy

# xi - random variable, equals payment for combination
# eta - random variable, equals the number of freespins given for combination
# zeta - random variable, equals payment for freespin


def Exi2(self, width, lines):
    Exi2 = 0
    for str_with_count in self.simple_num_comb:
        string = str_with_count[0]
        payment = self.get_simple_payment(string)
        Exi2 += str_with_count[1] / self.all_combinations() * (payment ** 2)
    for scatter_comb in self.scatter_num_comb:
        scat = scatter_comb[0]
        counts = scatter_comb[1]
        for cnt in range(width + 1):
            Exi2 += ((self.symbol[scat].payment[cnt] * len(lines)) ** 2) * counts[cnt] / self.all_combinations()
    return Exi2 / len(lines)


def Exieta(self, width, lines):
    Exieta = 0
    for scatter_comb in self.scatter_num_comb:
        scat = scatter_comb[0]
        counts = scatter_comb[1]
        for cnt in range(width + 1):
            Exieta += (self.symbol[scat].payment[cnt] * len(lines)) * self.symbol[scat].scatter[cnt] * \
                      counts[cnt] / self.all_combinations()
    return Exieta / len(lines)


def Eeta(self, width):
    Eeta = 0
    for scatter_comb in self.scatter_num_comb:
        scat = scatter_comb[0]
        counts = scatter_comb[1]
        for cnt in range(width + 1):
            Eeta += self.symbol[scat].scatter[cnt] * counts[cnt] / self.all_combinations()
    return Eeta


def Eeta2(self, width):
    Eeta2 = 0
    for scatter_comb in self.scatter_num_comb:
        scat = scatter_comb[0]
        counts = scatter_comb[1]
        for cnt in range(width + 1):
            Eeta2 += (self.symbol[scat].scatter[cnt] ** 2) * counts[cnt] / self.all_combinations()
    return Eeta2