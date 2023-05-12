import numpy as np
from matplotlib import pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl



temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'temperature')
wind = ctrl.Antecedent(np.arange(0, 5, 1), 'wind')
melt = ctrl.Consequent(np.arange(0, 1.5, 0.5), 'melt')

temperature.automf(5)
wind.automf(3)

melt['no melt'] = fuzz.trimf(melt.universe, [0, 0, 0.4])   # generate a triangular memebership function
melt['partially melted'] = fuzz.trimf(melt.universe, [0, 0.5, 1])
melt['fully melted'] = fuzz.trimf(melt.universe, [0.6, 1, 1])

temperature['average'].view()
wind.view()
melt.view()
plt.show()

#THIS RULE SET IS FOR ALL TEMPERATURES WHEN THERES LOW ('poor) WIND

rule1 = ctrl.Rule(temperature['poor'] & wind['poor'], melt['no melt']) #low wind, low temp
rule2 = ctrl.Rule(temperature['mediocre'] & wind['poor'], melt['no melt'])
rule3 = ctrl.Rule(temperature['average'] & wind['poor'], melt['no melt']) # 12-25
rule4 = ctrl.Rule(temperature['decent'] & wind['poor'], melt['partially melted']) # 23-40
rule5 = ctrl.Rule(temperature['good'] & wind['poor'], melt['fully melted']) # 38-50

#THIS RULE SET IS FOR ALL TEMPERATURES WHEN THERES AVERAGE WIND

rule6 = ctrl.Rule(temperature['poor'] & wind['average'], melt['no melt']) #low wind, low temp
rule7 = ctrl.Rule(temperature['mediocre'] & wind['average'], melt['no melt'])
rule8 = ctrl.Rule(temperature['average'] & wind['average'], melt['no melt']) # 12-25
rule9 = ctrl.Rule(temperature['decent'] & wind['average'], melt['partially melted']) # 23-40
rule10 = ctrl.Rule(temperature['good'] & wind['average'], melt['fully melted']) # 38-50

#THIS RULE SET IS FOR ALL TEMPERATURES WHEN THERES HIGH ('good) WIND

rule11 = ctrl.Rule(temperature['poor'] & wind['good'], melt['no melt']) #low wind, low temp
rule12 = ctrl.Rule(temperature['mediocre'] & wind['good'], melt['no melt'])
rule13 = ctrl.Rule(temperature['average'] & wind['good'], melt['partially melted']) # 12-25
rule14 = ctrl.Rule(temperature['decent'] & wind['good'], melt['fully melted']) # 23-40
rule15 = ctrl.Rule(temperature['good'] & wind['good'], melt['fully melted']) # 38-50

#'poor'; 'mediocre'; 'average'; 'decent' 'good': I HAD AN ERROR FOR USING DIFFERENT VARIABLE TYPES THAT AREN'T IN THE FUZZY FILE

#RULE APPLICATION AND INPUTS

melting_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11,rule12,rule13,rule14,rule15])
melting = ctrl.ControlSystemSimulation(melting_ctrl)

#INPUT OF TEMPERATURE AND WIND SPEED
melting.input['temperature'] = 38
melting.input['wind'] = 6

melting.compute()

print(melting.output['melt'])
melt.view(sim=melting)

plt.show()