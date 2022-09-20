import random
import math

BASE_HEIGHT = 70
MAX_HEIGHT = 87

BASE_TINY = [0,1,2,3]
BASE_REG = [3,4,5,6]
BASE_GIANT = [7,8,9,10]

PG_INC = 0
SG_INC = 2
SF_INC = 4
PF_INC = 6
C_INC = 8

TINY_ODDS = [45,30,20,5]
REG_ODDS = [10,35,40,15]
GIANT_ODDS = [40,40,15,5]
GIANTC_ODDS = [45,40,15]

def calc_height(pos, arch):
    height = -1
    # role base value based on archetype
    if (arch == "tiny"):
        height = random.choices(BASE_TINY, weights=TINY_ODDS, k=1)
    elif (arch == "skilled" or arch == "athletic"):
        height = random.choices(BASE_REG, weights=REG_ODDS, k=1)
    elif (arch == "giant"):
        if (pos == "c"):
            height = random.choices([BASE_GIANT[0],BASE_GIANT[1],BASE_GIANT[2]], weights=GIANTC_ODDS, k=1)
        else:
            height = random.choices(BASE_GIANT, weights=GIANT_ODDS, k=1)

    # add increase based on positional boost
    if (pos == "pg"):
        height[0] = height[0] + PG_INC
    elif (pos == "sg"):
        height[0] = height[0] + SG_INC
    elif (pos == "sf"):
        height[0] = height[0] + SF_INC
    elif (pos == "pf"):
        height[0] = height[0] + PF_INC
    elif (pos == "c"):
        height[0] = height[0] + C_INC

    #prepare final inch amount, then height
    final = BASE_HEIGHT + height[0]
    result = arch.capitalize() + " " + pos.upper() + " " + str(math.floor(final / 12)) + "\'" + str(final % 12)
    return result
