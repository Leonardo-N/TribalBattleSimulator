

import operator as op
import random as rd

''' i = infantary
    h = cavalry
    a = archery

    [attack, i_def, h_def, ar_def, type, farm, time]'''''


class Simulate:


    def __init__(self):
        i = 1
        h = 2
        a = 3

        sp = [10, 15, 45, 20, i, 1, 129]  # 0
        sw = [25, 50, 15, 40, i, 1, 189]  # 1
        b = [40, 10, 5, 10, i, 1, 166]  # 2
        ar = [15, 50, 40, 5, a, 1, 227]  # 3
        cl = [130, 30, 40, 30, h, 4, 303]  # 4
        ac = [120, 40, 30, 50, a, 5, 455]  # 5
        cp = [150, 200, 80, 180, h, 6, 606]  # 6
        ram = [2, 20, 50, 20, i, 5, 1081]  # 7
        cata = [100, 100, 50, 100, i, 8, 1621]  # 8

        params = [sp, sw, b, ar, cl, ac, cp, ram, cata]
        self.params = params

        attack_set = [7760,3000,0,0,0,0] #bbs, cls, acs, cps, rams, catas
        defense_set = [3550, 3550, 3550, 0] #lanca, espada, archer, cp
        self.attack_set = attack_set #[7760, 4000, 0, 0, 0, 0]  # bbs, cls, acs, cps, rams, catas
        self.defense_set = defense_set #[4458, 3550, 3550, 0]  # lanca, espada, archer, cp
        wall_lvl = 20
        integridade = 0.5
        self.wall_lvl = wall_lvl
        self.wall_b_lvl = wall_lvl
        self.integridade = integridade
        self.troops = [defense_set[0],  defense_set[1], attack_set[0], defense_set[2], attack_set[1], attack_set[2], defense_set[3], attack_set[4], attack_set[5]]

        return

    def reset(self):
        self.wall_b_lvl = self.wall_lvl
        self.defense_set = self.after_def_set
        self.after_def_set = []
        self.units_lost = []

    def time_to_recruit(self, att=True):
        if not att:
            quartel_time = ((self.troops[0] * self.params[0][6]) + (self.troops[1] * self.params[1][6]) + (self.troops[3] * self.params[3][6])) / 3600
            estabulo_time = (self.troops[6] * self.params[6][6]) / 3600
            oficina_time = 0
        if att:
            quartel_time = (self.troops[2] * self.params[2][6]) / 3600
            estabulo_time = ((self.troops[4] * self.params[4][6]) + (self.troops[5] * self.params[5][6])) / 3600
            oficina_time = ((self.troops[7] * self.params[7][6]) + (self.troops[8] * self.params[8][6])) / 3600

        time = []
        time.append(quartel_time)
        time.append(estabulo_time)
        time.append(oficina_time)
        self.time = time

        return self.time #usar self?


    def attack(self, attack, params):
        b_att = self.params[2][0] * attack[0]
        cl_att = self.params[4][0] * attack[1]
        ac_att = self.params[5][0] * attack[2]
        cp_att = self.params[6][0] * attack[3]
        cata_att = self.params[8][0] * attack[5]

        self.total = b_att + cl_att + ac_att + cp_att + cata_att

        if self.total == 0:
            row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            return row

        self.b_percent = b_att / total
        self.cl_percent = cl_att / total
        self.ac_percent = ac_att / total
        self.cp_percent = cp_att / total
        self.cata_percent = cata_att / total

        self.row = [b_att, cl_att, cp_att, ac_att, self.b_percent, self.cl_percent, self.cp_percent, self.ac_percent, cata_att, self.cata_percent]



    def rams_necessary(self, wall_lvl, lvls_lowered):
        rams_necessary = 2 * (1.09 ** wall_lvl) + (4 * (1.09 ** wall_lvl) * (lvls_lowered - 1)) + 0.5
        rams_necessary2 = (2 * (1.09 ** wall_lvl) + (4 * (1.09 ** wall_lvl) * (lvls_lowered - 1)) + 0.5) * (1 + integridade)

        ramsm = [rams_necessary, rams_necessary2]
        self.ramsm = ramsm

        return self.ramsm


    def levels_lowered(self, wall_lvl, rams):
        levels_lowered = int(
            (((-0.5 - (2 * 1.09 ** wall_lvl) + rams) / (4 * 1.09 ** wall_lvl)) + 1) * (1 / (1 + integridade)))

        if levels_lowered > 10:
            levels_lowered = 10
        return levels_lowered


    def defense(self, attack, defense, params, wall_lvl):
        def_inf = params[0][1] * defense[0] + params[1][1] * defense[1] + params[3][1] * defense[2] + params[6][1] * \
                  defense[3]
        def_calv = params[0][2] * defense[0] + params[1][2] * defense[1] + params[3][2] * defense[2] + params[6][2] * \
                   defense[3]
        def_archer = params[0][3] * defense[0] + params[1][3] * defense[1] + params[3][3] * defense[2] + params[6][3] * \
                     defense[3]
        row = [def_inf, def_calv, def_archer]
        self.row = row

        return self.row


    def winner_loss(attack_power, defense_power, params):
        winner_power = defense_power
        loser_power = attack_power

        if attack_power > defense_power:
            winner_power = attack_power
            loser_power = defense_power

        ratio = ((loser_power / winner_power) ** (0.5)) / (winner_power / loser_power)
        rate = [ratio, 1]
        return rate


    def battle(self, attack_row, defense_row, defense_set):
        self.after_def_set = self.defense_set
        loser_ratio_i = [0, 0]
        loser_ratio_h = [0, 0]
        loser_ratio_arc = [0, 0]
        attack_won = ['i', 'h', 'a']

        self.wall_b_lvl -= levels_lowered(self.wall_b_lvl, self.attack_set[4])

        if attack_row[0] > 0 or attack_row[8] > 0:
            def_to_f_i = (attack_row[4] + attack_row[9]) * defense_row[0] * (1.037 ** self.wall_b_lvl)
            attack_won[0] = True if def_to_f_i < attack_row[0] else False
            loser_ratio_i = winner_loss((attack_row[0] + attack_row[8]), def_to_f_i, params)

        if attack_row[1] > 0 or attack_row[2] > 0:
            def_to_f_h = (attack_row[5] + attack_row[6]) * defense_row[1] * (1.037 ** wall_b_lvl)
            attack_won[1] = True if def_to_f_h < attack_row[1] else False
            loser_ratio_h = winner_loss((attack_row[1] + attack_row[2]), def_to_f_h, params)

        if attack_row[3] > 0:
            def_to_f_arc = attack_row[7] * defense_row[2] * (1.037 ** wall_b_lvl)
            attack_won[2] = True if def_to_f_arc < attack_row[3] else False
            loser_ratio_arc = winner_loss(attack_row[3], def_to_f_arc, params)

        if attack_won[0] == True:
            units_to_f_i = [defense_set[0] * (attack_row[4] + attack_row[9]),
                            defense_set[1] * (attack_row[4] + attack_row[9]),
                            defense_set[2] * (attack_row[4] + attack_row[9]),
                            defense_set[3] * (attack_row[4] + attack_row[9])]
            after_def_set = [int(after_def_set[0] - units_to_f_i[0]), int(after_def_set[1] - units_to_f_i[1]),
                             int(after_def_set[2] - units_to_f_i[2]), int(after_def_set[3] - units_to_f_i[3])]
            attack_set[0] -= int(attack_set[0] * loser_ratio_i[0])
            attack_set[5] -= int(attack_set[5] * loser_ratio_i[0])
            attack_set[4] -= int(attack_set[4] * loser_ratio_i[0])

        if attack_won[0] == False:
            attack_set[0] = 0
            attack_set[5] = 0
            attack_set[4] = attack_set[4]
            units_to_f_i = [defense_set[0] * (attack_row[4] + attack_row[9]),
                            defense_set[1] * (attack_row[4] + attack_row[9]),
                            defense_set[2] * (attack_row[4] + attack_row[9]),
                            defense_set[3] * (attack_row[4] + attack_row[9])]
            def_lost = [units_to_f_i[0] * loser_ratio_i[0], units_to_f_i[1] * loser_ratio_i[0],
                        units_to_f_i[2] * loser_ratio_i[0], units_to_f_i[3] * loser_ratio_i[0]]
            after_def_set = [int(after_def_set[0] - def_lost[0]), int(after_def_set[1] - def_lost[1]),
                             int(after_def_set[2] - def_lost[2]), int(after_def_set[3] - def_lost[3])]

        if attack_won[1] == True:
            units_to_f_h = [defense_set[0] * (attack_row[5] + attack_row[6]),
                            defense_set[1] * (attack_row[5] + attack_row[6]),
                            defense_set[2] * (attack_row[5] + attack_row[6]),
                            defense_set[3] * (attack_row[5] + attack_row[6])]
            after_def_set = [int(after_def_set[0] - units_to_f_h[0]), int(after_def_set[1] - units_to_f_h[1]),
                             int(after_def_set[2] - units_to_f_h[2]), int(after_def_set[3] - units_to_f_h[3])]
            attack_set[1] -= int(attack_set[1] * loser_ratio_h[0])
            attack_set[3] -= int(attack_set[3] * loser_ratio_h[0])

        if attack_won[1] == False:
            attack_set[1] = 0
            attack_set[3] = 0
            units_to_f_h = [defense_set[0] * (attack_row[5] + attack_row[6]),
                            defense_set[1] * (attack_row[5] + attack_row[6]),
                            defense_set[2] * (attack_row[5] + attack_row[6]),
                            defense_set[3] * (attack_row[5] + attack_row[6])]
            def_lost = [units_to_f_h[0] * loser_ratio_h[0], units_to_f_h[1] * loser_ratio_h[0],
                        units_to_f_h[2] * loser_ratio_h[0], units_to_f_h[3] * loser_ratio_h[0]]
            after_def_set = [int(after_def_set[0] - def_lost[0]), int(after_def_set[1] - def_lost[1]),
                             int(after_def_set[2] - def_lost[2]), int(after_def_set[3] - def_lost[3])]

        if attack_won[2] == True:
            units_to_f_arc = [defense_set[0] * attack_row[7], defense_set[1] * attack_row[7],
                              defense_set[2] * attack_row[7], defense_set[3] * attack_row[7]]
            after_def_set = [int(after_def_set[0] - units_to_f_arc[0]), int(after_def_set[1] - units_to_f_arc[1]),
                             int(after_def_set[2] - units_to_f_arc[2]), int(after_def_set[3] - units_to_f_arc[3])]
            attack_set[2] -= int(attack_set[2] * loser_ratio_arc[0])

        if attack_won[2] == False:
            attack_set[2] = 0
            units_to_f_arc = [defense_set[0] * attack_row[7], defense_set[1] * attack_row[7],
                              defense_set[2] * attack_row[7], defense_set[3] * attack_row[7]]
            def_lost = [units_to_f_arc[0] * loser_ratio_arc[0], units_to_f_arc[1] * loser_ratio_arc[0],
                        units_to_f_arc[2] * loser_ratio_arc[0], units_to_f_arc[3] * loser_ratio_arc[0]]
            self.after_def_set = [int(after_def_set[0] - def_lost[0]), int(after_def_set[1] - def_lost[1]),
                             int(after_def_set[2] - def_lost[2]), int(after_def_set[3] - def_lost[3])]

        if not (attack_set == [0, 0, 0, 0, 0, 0] or after_def_set == [0, 0, 0, 0]):
            defense_set = after_def_set
            self.y = battle(attack(attack_set, params), defense(attack_set, defense_set, params, wall_lvl), params, wall_lvl,
                       attack_set, defense_set)

            return self.y

        after_def_set = self.after_def_set
        return self.after_def_set

    def wall_destroyed(self):
        self.wall_lvl -= (((rams remaining after losses) + 1 - (rams lost / 2)) * (
                    (strength of a ram, at the level of the sending village) / (strength of level 1 ram)) - 1 * 1.09 ^ (
                          wall lvl)) / (2 * 1.09 ^ (wall lvl)) + 1
        return

    def random_attack_set(self):
        pop = 0
        attack_set = [0, 0, 0, 0, 0, 0]
        random_2 = rd.randint(0, 2)

        while pop < 20600:
            random = rd.randint(0, 100)
            if random_2 == 1:
                random = rd.randint(0, 95)
            if random_2 == 2:
                random = rd.randint(0, 79)

            if -1 < random < 28:
                attack_set[0] = attack_set[0] + 50
                pop = pop + 50

            if 43 < random < 80:
                attack_set[1] = attack_set[1] + 20
                pop = pop + 80

            if 28 <= random <= 43:
                attack_set[4] = attack_set[4] + 5
                pop = pop + 25

            if 80 <= random <= 95:
                attack_set[2] = attack_set[2] + 20
                pop = pop + 100

            if random > 95:
                attack_set[5] = attack_set[5] + 5
                pop = pop + 40

        attack_set = self.attack_set

        return self.attack_set

def best_attack(gen_numb):
    best_effectiveness = [0, 0]
    for i in range(1, gen_numb):
        attack_set = random_attack_set()
        x = battle()  # 10x batalha - retorn [units killed, attack set]
        x.append(time_to_recruit(attack_set))  # x = [units killed, attack set, time to recruit]

        effectiveness = [x[0] / x[2], attack_set]
        if effectiveness[0] > best_effectiveness[0]:
            best_effectiveness = effectiveness

    return best_effectiveness

simulate= Simulate()

y= simulate.time_to_recruit()

print(y)