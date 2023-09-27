import random
import math

BASE_HEIGHT = 70
MAX_HEIGHT = 87

POS = ['pg','sg','sf','pf','c']
POS_ODDS = [1,1,1,1,1]
ARCH = ['tiny','athletic','skilled','giant']
ARCH_ODDS = [1,1,1,1]

BASE_TINY = [1,2,3]
BASE_REG = [4,5,6]
BASE_GIANT = [7,8,9]

PG_INC = 0
SG_INC = 2
SF_INC = 4
PF_INC = 6
C_INC = 8

TINY_ODDS = [5,45,50]
REG_ODDS = [25,50,25]
GIANT_ODDS = [50,45,5]

def calc_height(pos, arch):
    height = -1
    rand_pos = ""
    rand_arch = ""

    if (pos == "random"):
        pos = str(random.choices(POS, weights=POS_ODDS, k=1)[0])
        rand_pos = "Random:"

    if (arch == "random"):
        arch = str(random.choices(ARCH, weights=ARCH_ODDS, k=1)[0])
        rand_arch = "Random:"

    # roll base value based on archetype
    if (arch == "tiny"):
        height = random.choices(BASE_TINY, weights=TINY_ODDS, k=1)
    elif (arch == "skilled" or arch == "athletic"):
        height = random.choices(BASE_REG, weights=REG_ODDS, k=1)
    elif (arch == "giant"):
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

    # prepare final inch amount, then height
    final = BASE_HEIGHT + height[0]
    result = rand_arch + arch.capitalize() + " " + rand_pos + pos.upper() + " - " + str(math.floor(final / 12)) + "\'" + str(final % 12)
    return result
