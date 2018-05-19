# -*- coding: utf-8 -*-
"""
Created on Wed May 16 17:45 2018

@author: GoldHawk
"""


import operator as op
import random as rd

''' i = infantary
    h = cavalry
    a = archery
    
    [attack, i_def, h_def, ar_def, type, farm, time]'''''

i = 1
h = 2
a = 3

sp = [10, 15, 45, 20, i, 1, 129] #0
sw = [25, 50, 15, 40, i, 1, 189] #1
b = [40, 10, 5, 10, i, 1, 166] #2
ar = [15, 50, 40, 5, a, 1, 227] #3
cl = [130, 30, 40, 30, h, 4, 303] #4
ac = [120, 40, 30, 50, a, 5, 455] #5
cp = [150, 200, 80, 180, h, 6, 606] #6
ram = [2, 20, 50, 20, i, 5, 1081] #7
cata = [100, 100, 50, 100, i, 8, 1621] #8

params = [sp, sw, b, ar, cl, ac, cp, ram, cata]

# attack_set = [7760,4000,0,0,0,0] #bbs, cls, acs, cps, rams, catas
# defense_set = [3550, 3550, 3550, 0] #lanca, espada, archer, cp
attack_set = [6500,3000,0,0,350,0] #bbs, cls, acs, cps, rams, catas
defense_set = [10000, 10000, 5000, 1000] #lanca, espada, archer, cp

wall_lvl = 20
integridade = 0


def time_to_recruit(sp, sw, b, ar, cl, ac, cp, ram, cata, params):
    quartel_time = ((sp * params[0][6]) + (sw * params[1][6]) + (b * params[2][6]) + (ar * params[3][6]))/3600
    estabulo_time = ((cl * params[4][6]) + (ac * params[5][6]) + (cp * params[6][6]))/3600
    oficina_time = ((ram * params[7][6]) + (cata * params[8][6]))/3600
    time = []
    time.append(quartel_time)
    time.append(estabulo_time)
    time.append(oficina_time)

    return time

def attack(attack, params):
    b_att = params[2][0] * attack[0]
    cl_att = params[4][0] * attack[1]
    ac_att = params[5][0] * attack[2]
    cp_att = params[6][0] * attack[3]
    cata_att = params[8][0] * attack[5]

    total = b_att+cl_att+ac_att+cp_att+cata_att

    if total == 0:
        row = [0,0,0,0,0,0,0,0,0,0]
        return row

    b_percent = b_att/total
    cl_percent = cl_att/total
    ac_percent = ac_att/total
    cp_percent = cp_att/total
    cata_percent = cata_att/total

    row = [b_att, cl_att, cp_att, ac_att, b_percent, cl_percent, cp_percent, ac_percent, cata_att, cata_percent]
    return row

def rams_necessary(wall_lvl, lvls_lowered):
    rams_necessary = 2* (1.09**wall_lvl) + (4* (1.09**wall_lvl)*(lvls_lowered-1))+0.5
    rams_necessary2 = (2 * (1.09 ** wall_lvl) + (4 * (1.09 ** wall_lvl) * (lvls_lowered - 1)) + 0.5)*(1+integridade)

    ramsm = [rams_necessary, rams_necessary2]
    return ramsm

def wall_after_b(wall_lvl):
    return wall_lvl

def levels_lowered(wall_lvl, rams):
    levels_lowered = int((((-0.5 - (2*1.09**wall_lvl)+rams)/(4*1.09**wall_lvl)) + 1)*(1/(1+integridade)))

    if levels_lowered > 10:
        levels_lowered = 10
    return levels_lowered

def defense(attack, defense, params, wall_lvl):
    def_inf = params[0][1] * defense[0] + params[1][1] * defense[1] + params[3][1] * defense[2] + params[6][1] * defense[3]
    def_calv = params[0][2] * defense[0] + params[1][2] * defense[1] + params[3][2] * defense[2] + params[6][2] * defense[3]
    def_archer = params[0][3] * defense[0] + params[1][3] * defense[1] + params[3][3] * defense[2]  + params[6][3] * defense[3]
    row = [def_inf,def_calv,def_archer]

    return row

def winner_loss(attack_power, defense_power, params):
    winner_power = defense_power
    loser_power = attack_power

    if attack_power > defense_power:
        winner_power = attack_power
        loser_power = defense_power

    ratio = ((loser_power/winner_power)**(0.5))/(winner_power/loser_power)
    rate = [ratio, 1]
    return rate


def battle(attack_row, defense_row, params, wall_b_lvl, attack_set, defense_set):
    wall_lvl = wall_b_lvl #CHECK THIS
    init_attack_set = attack_set
    after_def_set = defense_set
    loser_ratio_i = [0, 0]
    loser_ratio_h = [0, 0]
    loser_ratio_arc = [0, 0]
    attack_won = ['i', 'h', 'a']

    wall_b_lvl -= levels_lowered(wall_b_lvl, attack_set[4])

    if attack_row[0] > 0 or attack_row[8] > 0:
        def_to_f_i = (attack_row[4] + attack_row[9]) * defense_row[0]* (1.037**wall_b_lvl)
        attack_won[0] = True if def_to_f_i < attack_row[0] else False
        loser_ratio_i = winner_loss((attack_row[0]+attack_row[8]), def_to_f_i, params)

    if attack_row[1] > 0 or attack_row[2] > 0:
        def_to_f_h = (attack_row[5]+attack_row[6]) * defense_row[1]* (1.037**wall_b_lvl)
        attack_won[1] = True if def_to_f_h < attack_row[1] else False
        loser_ratio_h = winner_loss((attack_row[1]+attack_row[2]), def_to_f_h, params)

    if attack_row[3] > 0:
        def_to_f_arc = attack_row[7] * defense_row[2]* (1.037**wall_b_lvl)
        attack_won[2] = True if def_to_f_arc < attack_row[3] else False
        loser_ratio_arc = winner_loss(attack_row[3], def_to_f_arc, params)


    if attack_won[0] == True:
        units_to_f_i = [defense_set[0]* (attack_row[4]+attack_row[9]), defense_set[1]*(attack_row[4]+attack_row[9]), defense_set[2]*(attack_row[4]+attack_row[9]), defense_set[3]*(attack_row[4]+attack_row[9])]
        after_def_set = [int(after_def_set[0] - units_to_f_i[0]), int(after_def_set[1] - units_to_f_i[1]), int(after_def_set[2] - units_to_f_i[2]), int(after_def_set[3] - units_to_f_i[3])]
        attack_set[0] -= int(attack_set[0] * loser_ratio_i[0])
        attack_set[5] -= int(attack_set[5] * loser_ratio_i[0])
        attack_set[4] -= int(attack_set[4] * loser_ratio_i[0])

    if attack_won[0] == False:
        attack_set[0] = 0
        attack_set[5] = 0
        attack_set[4] = 0
        units_to_f_i = [defense_set[0]* (attack_row[4]+attack_row[9]), defense_set[1]*(attack_row[4]+attack_row[9]), defense_set[2]*(attack_row[4]+attack_row[9]), defense_set[3]*(attack_row[4]+attack_row[9])]
        def_lost = [units_to_f_i[0] * loser_ratio_i[0], units_to_f_i[1] * loser_ratio_i[0], units_to_f_i[2] * loser_ratio_i[0], units_to_f_i[3] * loser_ratio_i[0]]
        after_def_set = [int(after_def_set[0] - def_lost[0]), int(after_def_set[1] - def_lost[1]), int(after_def_set[2] - def_lost[2]), int(after_def_set[3] - def_lost[3])]


    if attack_won[1] == True:
        units_to_f_h = [defense_set[0] * (attack_row[5]+attack_row[6]), defense_set[1] * (attack_row[5]+attack_row[6]), defense_set[2] * (attack_row[5]+attack_row[6]), defense_set[3] * (attack_row[5]+attack_row[6])]
        after_def_set = [int(after_def_set[0] - units_to_f_h[0]), int(after_def_set[1] - units_to_f_h[1]),int(after_def_set[2] - units_to_f_h[2]), int(after_def_set[3] - units_to_f_h[3])]
        attack_set[1] -= int(attack_set[1] * loser_ratio_h[0])
        attack_set[3] -= int(attack_set[3] * loser_ratio_h[0])

    if attack_won[1] == False:
        attack_set[1] = 0
        attack_set[3] = 0
        units_to_f_h = [defense_set[0] * (attack_row[5]+attack_row[6]), defense_set[1] * (attack_row[5]+attack_row[6]), defense_set[2] * (attack_row[5]+attack_row[6]), defense_set[3] * (attack_row[5]+attack_row[6])]
        def_lost = [units_to_f_h[0] * loser_ratio_h[0], units_to_f_h[1] * loser_ratio_h[0], units_to_f_h[2] * loser_ratio_h[0], units_to_f_h[3] * loser_ratio_h[0]]
        after_def_set = [int(after_def_set[0] - def_lost[0]), int(after_def_set[1] - def_lost[1]), int(after_def_set[2] - def_lost[2]), int(after_def_set[3] - def_lost[3])]

    if attack_won[2] == True:
        units_to_f_arc = [defense_set[0] * attack_row[7], defense_set[1] * attack_row[7], defense_set[2] * attack_row[7], defense_set[3] * attack_row[7]]
        after_def_set = [int(after_def_set[0] - units_to_f_arc[0]), int(after_def_set[1] - units_to_f_arc[1]), int(after_def_set[2] - units_to_f_arc[2]), int(after_def_set[3] - units_to_f_arc[3])]
        attack_set[2] -= int(attack_set[2] * loser_ratio_arc[0])

    if attack_won[2] == False:
        attack_set[2] = 0
        units_to_f_arc = [defense_set[0] * attack_row[7], defense_set[1] * attack_row[7], defense_set[2] * attack_row[7], defense_set[3] * attack_row[7]]
        def_lost = [units_to_f_arc[0] * loser_ratio_arc[0], units_to_f_arc[1] * loser_ratio_arc[0], units_to_f_arc[2] * loser_ratio_arc[0], units_to_f_arc[3] * loser_ratio_arc[0]]
        after_def_set = [int(after_def_set[0] - def_lost[0]), int(after_def_set[1] - def_lost[1]), int(after_def_set[2] - def_lost[2]), int(after_def_set[3] - def_lost[3])]

    if not (attack_set == [0, 0, 0, 0, 0, 0] or after_def_set == [0, 0, 0, 0]):
            defense_set = after_def_set
            y = battle(attack(attack_set, params), defense(attack_set, defense_set, params, wall_lvl), params, wall_lvl, attack_set, defense_set)

            return y


    ##CHECK THIS###
    after_att_set = attack_set
    wall_lvl = wall_after_b(wall_lvl, after_att_set, init_attack_set)
    # print(wall_lvl)

    return [after_att_set, after_def_set, wall_lvl]

def wall_after_b(wall_lvl, after_att, init_att):
    att_lost = after_att[4] - init_att[4]
    wall_lvl -= int((((after_att[4]) + 1 - (att_lost/ 2)) - 1.09**(wall_lvl))/(2 * 1.09**(wall_lvl)) + 1)
    return wall_lvl

z = battle(attack(attack_set, params), defense(attack_set, defense_set, params, wall_lvl), params, wall_lvl, attack_set, defense_set)




print(attack(attack_set, params))

print(defense(attack_set, defense_set, params, 20))

print(z)


# print(time_to_recruit(0,0,6500,0,3000,0,0,300,0,params))

# print(levels_lowered(20, 324))

# for i in range(1,11):
#     print(rams_necessary(20,i))



def random_attack_set():
    pop = 0
    attack_set = [0, 0, 0, 0, 0, 0]
    random_2 = rd.randint(0, 2)

    while pop<20600:
        random = rd.randint(0,100)
        if random_2 ==1:
            random = rd.randint(0,95)
        if random_2 ==2:
            random = rd.randint(0,79)


        if -1<random<28:
            attack_set[0] = attack_set[0] + 50
            pop = pop +50

        if 43<random< 80:
            attack_set[1] = attack_set[1] + 20
            pop = pop + 80

        if 28<=random<=43:
            attack_set[4] = attack_set[4] + 5
            pop = pop + 25

        if 80<=random<=95:
            attack_set[2] = attack_set[2] + 20
            pop = pop + 100

        if random>95:
            attack_set[5] = attack_set[5] + 5
            pop = pop + 40

    return attack_set

# for i in range(1,100000):
#     x = random_attack_set()
#     if x[0] > 8000:
#          print(x)


def best_attack(gen_numb):
    best_effectiveness = [0,0]
    for i in range (1,gen_numb):
        attack_set = random_attack_set()
        x = battle() #10x batalha - retorn [units killed, attack set]
        x.append(time_to_recruit(attack_set)) # x = [units killed, attack set, time to recruit]

        effectiveness = [x[0]/x[2], attack_set]
        if effectiveness[0] > best_effectiveness[0]:
            best_effectiveness = effectiveness

    return best_effectiveness