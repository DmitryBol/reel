
# xi - random variable, equals payment for combination
# eta - random variable, equals the number of freespins given for combination
# zeta - random variable, equals payment for freespin


def Exi2(self, width, lines):
    s = 0
    for str_with_count in self.simple_num_comb:
        string = str_with_count[0]
        #payment = self.get_simple_payment(string)
        payment = str_with_count[2]
        s += str_with_count[1] / self.all_combinations() * (payment ** 2)
    for scatter_comb in self.scatter_num_comb:
        scat = scatter_comb[0]
        counts = scatter_comb[1]
        for cnt in range(width + 1):
            s += ((self.symbol[scat].payment[cnt] * len(lines)) ** 2) * counts[cnt] / self.all_combinations()
    return s


def Exieta(self, width, lines):
    s = 0
    for scatter_comb in self.scatter_num_comb:
        scat = scatter_comb[0]
        counts = scatter_comb[1]
        for cnt in range(width + 1):
            s += (self.symbol[scat].payment[cnt] * len(lines)) * self.symbol[scat].scatter[cnt] * \
                      counts[cnt] / self.all_combinations()
    return s


def Eeta(self, width):
    s = 0
    for scatter_comb in self.scatter_num_comb:
        scat = scatter_comb[0]
        counts = scatter_comb[1]
        for cnt in range(width + 1):
            s += self.symbol[scat].scatter[cnt] * counts[cnt] / self.all_combinations()
    return s


def Eeta2(self, width):
    s = 0
    for scatter_comb in self.scatter_num_comb:
        scat = scatter_comb[0]
        counts = scatter_comb[1]
        for cnt in range(width + 1):
            s += (self.symbol[scat].scatter[cnt] ** 2) * counts[cnt] / self.all_combinations()
    return s
