'''
@author: Jack Charles   https://jackcharlesconsulting.com/
'''

import math
import json
import numpy as np
import matplotlib.pyplot as plt
import util.wellengcalc as wec
import util.unit as uunit
import calcs.abwave as abw

openhole_id = 8.5
openhole_roughness = 0.05
screen_od = 6.25
screen_id = 5.0
screen_roughness = 0.007
centralizer_od = 7.25
washpipe_od = 4
washpipe_id = 3.5
washpipe_roughness = 0.007
solid_diameter = 0.0287
solid_density = 1.60
solid_loading = 0.75
solid_absVol = 0.0443
fluid_density = 8.80
fluid_viscosity = 1.2
dune_height_ratio = [0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675, 0.7, 0.725, 0.75, 0.775, 0.8, 0.825, 0.85, 0.875]

aw_parameters_SGS = abw.ABWaveInputData('SGS case', 'SGS solution', openhole_id, openhole_roughness, screen_od, screen_id, screen_roughness, centralizer_od, washpipe_od, washpipe_id, washpipe_roughness, 
                 solid_diameter, solid_density, solid_loading, solid_absVol, fluid_density, fluid_viscosity, "SGS")
aw_parameters_SGS_alt = abw.ABWaveInputData('SGS alt case', 'SGS alt solution', openhole_id, openhole_roughness, screen_od, screen_id, screen_roughness, centralizer_od, washpipe_od, washpipe_id, washpipe_roughness, 
                 solid_diameter, solid_density, solid_loading, solid_absVol, fluid_density, fluid_viscosity, "SGS alt")
aw_parameters_Oroskar = abw.ABWaveInputData('SGS case', 'SGS solution', openhole_id, openhole_roughness, screen_od, screen_id, screen_roughness, centralizer_od, washpipe_od, washpipe_id, washpipe_roughness, 
                 solid_diameter, solid_density, solid_loading, solid_absVol, fluid_density, fluid_viscosity, "Oroskar")
aw_parameters_Oroskar_mod = abw.ABWaveInputData('SGS case', 'SGS solution', openhole_id, openhole_roughness, screen_od, screen_id, screen_roughness, centralizer_od, washpipe_od, washpipe_id, washpipe_roughness, 
                 solid_diameter, solid_density, solid_loading, solid_absVol, fluid_density, fluid_viscosity, "Oroskar mod")
aw_parameters_Hang = abw.ABWaveInputData('SGS case', 'SGS solution', openhole_id, openhole_roughness, screen_od, screen_id, screen_roughness, centralizer_od, washpipe_od, washpipe_id, washpipe_roughness, 
                 solid_diameter, solid_density, solid_loading, solid_absVol, fluid_density, fluid_viscosity, "Hang")

# results = []
# results0 = []
# results1 = []
# results2 = []
# results3 = []

results = {}
results0 = {}
results1 = {}
results2 = {}
results3 = {}

print("DHR\tDH\tScreenOH\tReturn")
for i in range(len(dune_height_ratio)):
    results[dune_height_ratio[i]] = abw.calc_AlphaBetaWave(aw_parameters_SGS, dune_height_ratio[i])
    results0[dune_height_ratio[i]] = abw.calc_AlphaBetaWave(aw_parameters_SGS_alt, dune_height_ratio[i])
    results1[dune_height_ratio[i]] = abw.calc_AlphaBetaWave(aw_parameters_Oroskar, dune_height_ratio[i])
    results2[dune_height_ratio[i]] = abw.calc_AlphaBetaWave(aw_parameters_Oroskar_mod, dune_height_ratio[i])
    results3[dune_height_ratio[i]] = abw.calc_AlphaBetaWave(aw_parameters_Hang, dune_height_ratio[i])
    #print(f"{results[i].dune_height_ratio: .2f}\t{results[i].dune_height: .2f}\t{results[i].screen_oh_rate: .2f}\t{results[i].return_rate: .2f}\t")
    #print(f"{results[i].dune_height_ratio: .3f}\t{results[i].screen_oh_dp: .2f}\t{results[i].washpipe_screen_dp: .2f} \
    #      \t{results0[i].screen_oh_dp: .2f}\t{results0[i].washpipe_screen_dp: .2f}\t{results1[i].screen_oh_dp: .2f}\t{results1[i].washpipe_screen_dp: .2f} \
    #      \t{results2[i].screen_oh_dp: .2f}\t{results2[i].washpipe_screen_dp: .2f}\t{results3[i].screen_oh_dp: .2f}\t{results3[i].washpipe_screen_dp: .2f}")
abw.show_plots(results, results0, results1, results2, results3)