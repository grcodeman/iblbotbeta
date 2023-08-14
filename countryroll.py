import random
import math

AMERICA = ["United States", "Canada", "Mexico", "Argentina", "Brazil", "Colombia", "Jamaica", "Cuba", "Puerto Rico", "Venezuela", "Dominican Republic", "Uruguay", "Haiti"]
EUROPE = ["France", "Germany", "Spain", "Portugal", "UK", "Ireland", "Serbia", "Slovenia", "Lithuania", "Greece", "Turkey", "Ukraine", "Italy", "Finland", "Croatia", "Poland", "Czech Republic"]
AFRICA = ["Angola", "Ivory Coast", "Senegal", "Egypt", "Nigeria", "DR Congo", "Ethiopia", "South Africa", "Cote D'Ivoire", "Sudan", "Cameroon", "Kenya"]
ASIA = ["India", "Japan", "Iran", "China", "Philippines", "Korea", "Lebanon", "Tunisia", "Jordan", "UAE", "Israel", "Russia"]
OCEANIA = ["Australia", "New Zealand", "Papua New Guinea", "Fiji", "Solomon Islands", "Samoa"]

REGIONS = {'america':AMERICA, 'europe':EUROPE, 'africa':AFRICA, 'asia':ASIA, 'oceania':OCEANIA}

def roll_country(region):
    rolled = random.choice(REGIONS[region])
    return rolled