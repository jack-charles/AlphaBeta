'''
@author: Jack Charles   https://jackcharlesconsulting.com/
'''

import math
import json
import numpy as np
import matplotlib.pyplot as plt
import util.wellengcalc as wec
import util.unit as wecu
from util.unit import convert as ucon

class ABWaveInputData():
    def __init__(self, name:str, description:str, 
                 openhole_id:float, openhole_roughness:float, screen_od:float, screen_id:float, screen_roughness:float, 
                 centralizer_od:float, washpipe_od:float, washpipe_id:float, washpipe_roughness:float, 
                 solid_diameter:float, solid_density:float, solid_loading:float, solid_absVol:float, 
                 fluid_density:float, fluid_viscosity:float, model:str):
        self.name = name
        self.description = description
        self.openhole_id = openhole_id
        self.openhole_roughness = openhole_roughness
        self.screen_od = screen_od
        self.screen_id = screen_id
        self.screen_roughness = screen_roughness
        self.centralizer_od = centralizer_od
        self.washpipe_od = washpipe_od
        self.washpipe_id = washpipe_id
        self.washpipe_roughness = washpipe_roughness
        self.solid_diameter = solid_diameter
        self.solid_density = solid_density
        self.solid_loading = solid_loading
        self.solid_absVol = solid_absVol
        self.fluid_density = fluid_density
        self.fluid_viscosity = fluid_viscosity
        self.model= model

class ABWaveResults():
    def __init__(self, name:str, description:str, 
                 dune_height_ratio:float, dune_height:float, hydraulic_diameter:float, equivalent_diameter:float, 
                 area_o, area_i:float, perimeter_o:float, perimeter_i:float, width_o:float, width_i:float,
                 v_crit:float, screen_oh_rate:float, washpipe_screen_rate:float, pump_rate:float, return_rate:float, 
                 screen_oh_dp:float, washpipe_screen_dp:float):
        self.name = name
        self.description = description
        self.dune_height_ratio = dune_height_ratio
        self.dune_height = dune_height
        self.hydraulic_diameter = hydraulic_diameter
        self.equivalent_diameter = equivalent_diameter
        self.area_o = area_o
        self.area_i = area_i
        self.perimeter_o = perimeter_o
        self.perimeter_i = perimeter_i
        self.width_o = width_o
        self.width_i = width_i
        self.v_crit = v_crit
        self.screen_oh_rate = screen_oh_rate
        self.washpipe_screen_rate = washpipe_screen_rate
        self.pump_rate = pump_rate
        self.return_rate = return_rate
        self.screen_oh_dp = screen_oh_dp
        self.washpipe_screen_dp = washpipe_screen_dp

class BetaWave():
    def __init__(self, hydraulic_diameter:float, equivalent_diameter:float, area:float, washpipe_screen_dp:float, dmass_dlength:float):
        self.hydraulic_diameter = hydraulic_diameter
        self.equivalent_diameter = equivalent_diameter
        self.area = area
        self.washpipe_screen_dp = washpipe_screen_dp
        self.dmass_dlength = dmass_dlength

def read_saved_file_json(data_filename:str):
    with open(data_filename, 'r',) as file:
        data_dictionary = json.load(file)      
    abinputs:ABWaveInputData
    abresults:dict[str,ABWaveResults] = {}
    #unit_class = UnitSystemClass(**data_dictionary)      #this would work if the class names were identical to the dictionary
    _dd = data_dictionary['Units']
    unit_class = wecu.UnitSystem(_dd['Unit System'], _dd['Angle'], _dd['Area'], _dd['Capacity'], _dd['Concentration'], 
                                 _dd['Density Gas'], _dd['Density Liquid'], _dd['Density Solid'], _dd['Diameter'], _dd['Force'], 
                                 _dd['Length'], _dd['Mass'], _dd['Mass Gradient'], _dd['Mass Rate'], _dd['Permeability'], 
                                 _dd['Power'], _dd['Pressure'], _dd['Pressure Gradient'], _dd['Temperature'], _dd['Velocity'], 
                                 _dd['Viscosity'], _dd['Volume'], _dd['Volumetric Rate'])

    _dd = data_dictionary['AB Inputs']
    abinputs = ABWaveInputData(_dd['Name'], _dd['Description'], 
                                _dd['openhole_id'], _dd['openhole_roughness'], _dd['screen_od'], _dd['screen_id'], _dd['screen_roughness'], 
                                _dd['centralizer_od'], _dd['washpipe_od'], _dd['washpipe_id'], _dd['washpipe_roughness'], 
                                _dd['solid_diameter'], _dd['solid_density'], _dd['solid_loading'], _dd['solid_absVol'],
                                _dd['fluid_density'], _dd['fluid_viscosity'], _dd['model'])
    
    _dd = data_dictionary['AB Results']
    for key in _dd:
        abresults[key] = ABWaveResults(_dd[key]['Name'], _dd[key]['Description'], 
                                    _dd[key]['dune_height_ratio'], _dd[key]['dune_height'], _dd[key]['hydraulic_diameter'], _dd[key]['equivalent_diameter'],
                                    _dd[key]['area_o'], _dd[key]['area_i'], _dd[key]['perimeter_o'], _dd[key]['perimeter_i'], _dd[key]['width_o'], _dd[key]['width_i'],  
                                    _dd[key]['v_crit'], _dd[key]['screen_oh_rate'], _dd[key]['washpipe_screen_rate'], _dd[key]['pump_rate'], _dd[key]['return_rate'], _dd[key]['screen_oh_dp'], _dd[key]['washpipe_screen_dp'])
        
    return abinputs, abresults, unit_class

def write_saved_file_json(abinputs:ABWaveInputData, abresults:dict[str,ABWaveResults], unit_class, data_filename:str):
    data_dictionary = {}
    data_dictionary['Units'] = {'Unit System': unit_class.name_unitsystem, 'Angle': unit_class.angle, 'Area': unit_class.area, 'Capacity': unit_class.capacity,
                 'Concentration': unit_class.concentration, 'Density Gas': unit_class.density_gas, 'Density Liquid': unit_class.density_liquid, 'Density Solid': unit_class.density_solid, 
                 'Diameter': unit_class.diameter, 'Force': unit_class.force, 'Length': unit_class.length, 'Mass': unit_class.mass, 'Mass Gradient': unit_class.mass_gradient, 
                 'Mass Rate': unit_class.mass_rate, 'Permeability': unit_class.permeability, 'Power': unit_class.power, 'Pressure': unit_class.pressure, 'Pressure Gradient': unit_class.pressure_gradient, 
                 'Temperature': unit_class.temperature, 'Velocity': unit_class.velocity, 'Visocisty': unit_class.viscosity, 'Volumetric Rate': unit_class.volumetric_rate}
    data_dictionary['AB Inputs'] = {'Name': abinputs.name, 'Description': abinputs.description}
    for key in abresults:
        data_dictionary['AB Results'][key] = {'dune_height_ratio': abresults[key].dune_height_ratio}
    with open(data_filename, 'w',) as file:
        json.dump(data_dictionary, file)
    return

def calc_AlphaBetaWave(ABParameters:ABWaveInputData, dune_height_ratio:float):
    #openhole_id,openhole_roughness,screen_od,screen_id,screen_roughness,centralizer_od,washpipe_od,washpipe_id,washpipe_roughness,solid_diameter:in 
    #solid_density,solid_loading,fluid_density:ppg      solid_absVol: fluid_viscosity:cP, dune_height_ratio:dimensionless 
    #solid_density:SG     
    
    nPrime = 1
    kPrime = 0.00002088         #need to include as user variables eventually
    abp = ABParameters
    #calculate geometry of wellbore with dune
    #eccentricity_wp = (screen_id - washpipe_od) / (screen_id - washpipe_od)
    eccentricity_wp = wec.calc_eccentricity(abp.washpipe_od,abp.screen_id, 0)
    dune_height = dune_height_ratio * abp.openhole_id
    hydraulic_diameter, equivalent_diameter, area_o, area_i, perimeter_o, perimeter_i, width_o, width_i = wec.calc_alphawave_dune_height(abp.openhole_id, abp.screen_od, abp.centralizer_od, dune_height_ratio)
    flow_area = area_o - area_i
    bed_width = width_o - width_i
    wetted_perimeter = perimeter_o + perimeter_i 

    #calculate slurry properties
    full_open_annulus = wec.calc_area(abp.openhole_id, abp.screen_od)
    solid_loading_oh = abp.solid_loading / (flow_area / full_open_annulus)    #first assumption is flow is evenly split based on area
    c = solid_loading_oh / (abp.solid_density * 8.34 + solid_loading_oh)
    slurry_viscosity = abp.fluid_viscosity * wec.calc_slurry_viscosity(solid_loading_oh, abp.solid_density * 8.34, abp.fluid_density)
    slurry_density = wec.calc_slurry_density(abp.fluid_density, abp.solid_absVol, solid_loading_oh)
    
    #calculate transport rate
    if abp.model == 'Oroskar':
        transport_velocity = wec.calc_horizontal_transport_Oroskar(equivalent_diameter, abp.solid_diameter, abp.solid_density * 8.34, abp.fluid_density, abp.fluid_viscosity, c)
    elif abp.model == 'Oroskar mod':
        transport_velocity = wec.calc_horizontal_transport_OroskarMod(equivalent_diameter, abp.solid_diameter, abp.solid_density * 8.34, abp.fluid_density, abp.fluid_viscosity, c)
    elif abp.model == 'Hang':
        transport_velocity = wec.calc_horizontal_transport_Hang(hydraulic_diameter, abp.solid_diameter, abp.solid_density * 8.34, abp.fluid_density, slurry_density, abp.fluid_viscosity)
    
    #calculate pressure drop at given rate above dune
    screen_oh_rate = ucon(transport_velocity * flow_area / 144, 'ft\u00b3', 'bbl') * 60
    NRe = wec.calc_NRe_newton(transport_velocity, hydraulic_diameter, slurry_density, slurry_viscosity)
    alpha_ff = wec.calc_friction_colebrook(hydraulic_diameter, NRe, abp.openhole_roughness)     #friction factor above dune
    screen_oh_dp = wec.calc_DPf(alpha_ff, slurry_density, transport_velocity, hydraulic_diameter, 1)
    
    #inner loop finds rates to satisfy dPscr_oh = dPwp_scr with Newton-Raphson method
    #outer loop verifies that change in sand concentration is low once fluid rates are solved
    exit_converged_c = 1      #exits if converged
    loop_counter_c = 1        #limits number of loops to prevent lockup
    while abs(exit_converged_c) > 0.001 and loop_counter_c < 100:    #final check if sand concentration change is small
        exit_converged_dP = 1      #exits if converged
        loop_counter = 1        #limits number of loops to prevent lockup
        q1 = screen_oh_rate     #bpm
        dq = 0.001              #bpm
        while abs(exit_converged_dP) > 0.01 and loop_counter < 100:     #dPscr_oh = dPwp_scr(q)
            #first estimate, q = q_wp_scr
            q = q1

            wp_screen_vel = wec.calc_fluid_velocity(q, abp.screen_id,abp. washpipe_od)
            NRe = wec.calc_NRe_newton(wp_screen_vel, abp.screen_id - abp.washpipe_od, abp.fluid_density, abp.fluid_viscosity)
            wp_screen_ff = wec.calc_friction_colebrook(abp.screen_id - abp.washpipe_od, NRe, abp.screen_roughness)
            wp_screen_dp1 = wec.calc_DPf(wp_screen_ff, abp.fluid_density, wp_screen_vel, abp.screen_id - abp.washpipe_od, 1) * wec.calc_eccentricity_factor_powerlaw(nPrime, NRe, abp.screen_id, abp.washpipe_od, eccentricity_wp)

            #NRe = wec.calc_NRe_newton(wec.calc_fluid_velocity(q, washpipe_od, screen_id), screen_id - washpipe_od, fluid_density, fluid_viscosity)
            #wp_screen_ff = wec.calc_friction_colebrook(screen_id - washpipe_od, NRe, screen_roughness)
            #wp_screen_dp1 = wec.calc_DPf(wp_screen_ff, fluid_density, wec.calc_fluid_velocity(q, washpipe_od, screen_id), screen_id - washpipe_od, 1) * wec.calc_eccentricity_factor_powerlaw(nPrime, NRe, screen_id, washpipe_od, eccentricity_wp)
            
            #second calc, q2
            q = q1 + dq
            
            wp_screen_vel = wec.calc_fluid_velocity(q, abp.screen_id, abp.washpipe_od)
            NRe = wec.calc_NRe_newton(wp_screen_vel, abp.screen_id - abp.washpipe_od, abp.fluid_density, abp.fluid_viscosity)
            wp_screen_ff = wec.calc_friction_colebrook(abp.screen_id - abp.washpipe_od, NRe, abp.screen_roughness)
            wp_screen_dp2 = wec.calc_DPf(wp_screen_ff, abp.fluid_density, wp_screen_vel, abp.screen_id - abp.washpipe_od, 1) * wec.calc_eccentricity_factor_powerlaw(nPrime, NRe, abp.screen_id, abp.washpipe_od, eccentricity_wp)

            #NRe = wec.calc_NRe_newton(wec.calc_fluid_velocity(q, washpipe_od, screen_id), screen_id - washpipe_od, fluid_density, fluid_viscosity)
            #wp_screen_ff = wec.calc_friction_colebrook(screen_id - washpipe_od, NRe, screen_roughness)
            #wp_screen_dp2 = wec.calc_DPf(wp_screen_ff, fluid_density, wec.calc_fluid_velocity(q, washpipe_od, screen_id), screen_id - washpipe_od, 1) * wec.calc_eccentricity_factor_powerlaw(nPrime, NRe, screen_id, washpipe_od, eccentricity_wp)

            y1 = screen_oh_dp - wp_screen_dp1
            y2 = screen_oh_dp - wp_screen_dp2
            q2 = q1 - y1 / ((y2 - y1) / dq)
            exit_converged_dP = q2 - q1
            loop_counter = loop_counter + 1
            q1 = q2

            #calculate new proppant loading based on fluid rates from dP, and update calculations above dune
            solid_loading_oh = abp.solid_loading * (screen_oh_rate + q1) / screen_oh_rate
            c1 = solid_loading_oh / (abp.solid_density * 8.34 + solid_loading_oh)
            slurry_viscosity = abp.fluid_viscosity * wec.calc_slurry_viscosity(solid_loading_oh, abp.solid_density * 8.34, abp.fluid_density)
            slurry_density = wec.calc_slurry_density(abp.fluid_density, abp.solid_absVol, solid_loading_oh)

            if abp.model == 'SGS':
                transport_velocity = wec.calc_horizontal_transport_SGS(equivalent_diameter, abp.solid_diameter, abp.solid_density * 8.34, abp.fluid_density, abp.fluid_viscosity, c1, dune_height, abp.openhole_id)
            elif abp.model == 'SGS alt':
                transport_velocity = wec.calc_horizontal_transport_SGS_alt(equivalent_diameter, abp.solid_diameter, abp.solid_density * 8.34, abp.fluid_density, abp.fluid_viscosity, c1, width_o - width_i, perimeter_o + perimeter_i)
            elif abp.model == 'Oroskar':
                transport_velocity = wec.calc_horizontal_transport_Oroskar(equivalent_diameter, abp.solid_diameter, abp.solid_density * 8.34, abp.fluid_density, abp.fluid_viscosity, c)
            elif abp.model == 'Oroskar mod':
                transport_velocity = wec.calc_horizontal_transport_OroskarMod(equivalent_diameter, abp.solid_diameter, abp.solid_density * 8.34, abp.fluid_density, abp.fluid_viscosity, c1)
            elif abp.model == 'Hang':
                transport_velocity = wec.calc_horizontal_transport_Hang(hydraulic_diameter, abp.solid_diameter, abp.solid_density * 8.34, abp.fluid_density, slurry_density, abp.fluid_viscosity)
            
            screen_oh_rate = ucon(transport_velocity * flow_area / 144, 'ft\u00b3', 'bbl') * 60
            NRe = wec.calc_NRe_newton(transport_velocity, hydraulic_diameter, slurry_density, slurry_viscosity)
            alpha_ff = wec.calc_friction_colebrook(hydraulic_diameter, NRe, abp.openhole_roughness)
            screen_oh_dp = wec.calc_DPf(alpha_ff, slurry_density, transport_velocity, hydraulic_diameter, 1)
            
        loop_counter_c = loop_counter_c + 1
        exit_converged_c = c1 - c
        c = c1

    #calculate final washpipe-screen dP
    wp_screen_rate = q1
    wp_screen_velocity = wec.calc_fluid_velocity(wp_screen_rate, abp.screen_id, abp.washpipe_od)
    NRe = wec.calc_NRe_newton(wp_screen_velocity, abp.screen_id - abp.washpipe_od, abp.fluid_density, abp.fluid_viscosity)
    wp_screen_ff = wec.calc_friction_colebrook(abp.screen_id - abp.washpipe_od, NRe, abp.screen_roughness)
    washpipe_screen_dp = wec.calc_DPf(wp_screen_ff, abp.fluid_density, wp_screen_velocity, abp.screen_id - abp.washpipe_od, 1) * wec.calc_eccentricity_factor_powerlaw(nPrime, NRe, abp.screen_id, abp.washpipe_od, eccentricity_wp)
    
    #with rates solved, allow for losses in reported input rate
    leakoff_rate = 0
    return_rate = screen_oh_rate + wp_screen_rate
    pump_rate = screen_oh_rate + wp_screen_rate + leakoff_rate

    #solve for beta wave with pump rate
    wp_screen_velocity_beta = wec.calc_fluid_velocity(pump_rate, abp.screen_id, abp.washpipe_od)
    NRe = wec.calc_NRe_newton(wp_screen_velocity, abp.screen_id - abp.washpipe_od, abp.fluid_density, abp.fluid_viscosity)
    wp_screen_ff_beta = wec.calc_friction_colebrook(abp.screen_id - abp.washpipe_od, NRe, abp.screen_roughness)
    washpipe_screen_dp_beta = wec.calc_DPf(wp_screen_ff_beta, abp.fluid_density, wp_screen_velocity_beta, abp.screen_id - abp.washpipe_od, 1) * wec.calc_eccentricity_factor_powerlaw(nPrime, NRe, abp.screen_id, abp.washpipe_od, eccentricity_wp)

    #solve for washpipe dP with return rate
    washpipe_velocity = wec.calc_fluid_velocity(return_rate, abp.washpipe_id)
    NRe = wec.calc_NRe_newton(washpipe_velocity, abp.washpipe_id, abp.fluid_density, abp.fluid_viscosity)
    washpipe_ff = wec.calc_friction_colebrook(abp.washpipe_id, NRe, abp.washpipe_roughness)
    washpipe_dp = wec.calc_DPf(washpipe_ff, abp.fluid_density, washpipe_velocity, abp.washpipe_id, 1)

    #with overall pump rate, calculate full open dP with clean fluid
    
    output = ABWaveResults(abp.name, abp.description, dune_height_ratio, dune_height, hydraulic_diameter, equivalent_diameter, area_o, area_i, perimeter_o, perimeter_i, width_o, width_i, 
                            transport_velocity, screen_oh_rate, wp_screen_rate, pump_rate, return_rate, screen_oh_dp, washpipe_screen_dp)
    return output

def show_plots(alphawave_curve, alphawave_curve0, alphawave_curve1, alphawave_curve2, alphawave_curve3):
    #plots
    #plt.plot(alphawave_curve.dune_height_ratio, alphawave_curve.pump_rate)
    plt.title('Pump Rate vs Dune Height Ratio')
    plt.xlabel('Pump Rate', fontsize=8)
    plt.ylabel('Dune Height Ratio', fontsize=8)
    plt.tick_params(axis='both', which='major', labelsize=6)
    plt.grid()
    
    cases = list(alphawave_curve.keys())
    plt.plot([alphawave_curve[dhr].pump_rate for dhr in list(alphawave_curve.keys())], [alphawave_curve[dhr].dune_height_ratio for dhr in list(alphawave_curve.keys())], label=alphawave_curve[0.7].name)
    plt.plot([alphawave_curve0[dhr].pump_rate for dhr in cases], [alphawave_curve0[dhr].dune_height_ratio for dhr in cases], label=alphawave_curve0[0.7].name)
    plt.plot([alphawave_curve1[dhr].pump_rate for dhr in cases], [alphawave_curve1[dhr].dune_height_ratio for dhr in cases], label=alphawave_curve1[0.7].name)
    plt.plot([alphawave_curve2[dhr].pump_rate for dhr in cases], [alphawave_curve2[dhr].dune_height_ratio for dhr in cases], label=alphawave_curve2[0.7].name)
    plt.plot([alphawave_curve3[dhr].pump_rate for dhr in cases], [alphawave_curve3[dhr].dune_height_ratio for dhr in cases], label=alphawave_curve3[0.7].name)  
    plt.legend(['SGS', 'SGS alt', 'Oroskar', 'Oroskar mod', 'Hang'], loc='best')

    plt.show()




#SAVE THIS IN CASE OF REVERSION
# def calc_AlphaWave(openhole_id, openhole_roughness, screen_od, screen_id, screen_roughness, centralizer_od, washpipe_od, washpipe_id, washpipe_roughness, 
#                   solid_diameter, solid_density, solid_loading, solid_absVol, fluid_density, fluid_viscosity, dune_height_ratio, model: str):
#     #openhole_id,openhole_roughness,screen_od,screen_id,screen_roughness,centralizer_od,washpipe_od,washpipe_id,washpipe_roughness,solid_diameter:in 
#     #solid_density,solid_loading,fluid_density:ppg      solid_absVol: fluid_viscosity:cP, dune_height_ratio:dimensionless 
#     #solid_density:SG     
    
#     nPrime = 1
#     kPrime = 0.00002088         #need to include as user variables eventually
    
#     #calculate geometry of wellbore with dune
#     #eccentricity_wp = (screen_id - washpipe_od) / (screen_id - washpipe_od)
#     eccentricity_wp = wec.calc_eccentricity(washpipe_od,screen_id, 0)
#     dune_height = dune_height_ratio * openhole_id
#     hydraulic_diameter, equivalent_diameter, area_o, area_i, perimeter_o, perimeter_i, width_o, width_i = wec.calc_alphawave_dune_height(openhole_id, screen_od, centralizer_od, dune_height_ratio)
#     flow_area = area_o - area_i
#     bed_width = width_o - width_i
#     wetted_perimeter = perimeter_o + perimeter_i 

#     #calculate slurry properties
#     full_open_annulus = wec.calc_area(openhole_id, screen_od)
#     solid_loading_oh = solid_loading / (flow_area / full_open_annulus)    #first assumption is flow is evenly split based on area
#     c = solid_loading_oh / (solid_density * 8.34 + solid_loading_oh)
#     slurry_viscosity = fluid_viscosity * wec.calc_slurry_viscosity(solid_loading_oh, solid_density * 8.34, fluid_density)
#     slurry_density = wec.calc_slurry_density(fluid_density, solid_absVol, solid_loading_oh)
    
#     #calculate transport rate
#     if model == 'SGS':
#         transport_velocity = wec.calc_horizontal_transport_SGS(equivalent_diameter, solid_diameter, solid_density * 8.34, fluid_density, fluid_viscosity, c, dune_height, openhole_id)
#     elif model == 'SGS alt':
#         transport_velocity = wec.calc_horizontal_transport_SGS_alt(equivalent_diameter, solid_diameter, solid_density * 8.34, fluid_density, fluid_viscosity, c, bed_width, wetted_perimeter)
#     elif model == 'Oroskar':
#         transport_velocity = wec.calc_horizontal_transport_Oroskar(equivalent_diameter, solid_diameter, solid_density * 8.34, fluid_density, fluid_viscosity, c)
#     elif model == 'Oroskar mod':
#         transport_velocity = wec.calc_horizontal_transport_OroskarMod(equivalent_diameter, solid_diameter, solid_density * 8.34, fluid_density, fluid_viscosity, c)
#     elif model == 'Hang':
#         transport_velocity = wec.calc_horizontal_transport_Hang(hydraulic_diameter, solid_diameter, solid_density * 8.34, fluid_density, slurry_density, fluid_viscosity)
    
#     #calculate pressure drop at given rate above dune
#     screen_oh_rate = ucon(transport_velocity * flow_area / 144, 'ft\u00b3', 'bbl') * 60
#     NRe = wec.calc_NRe_newton(transport_velocity, hydraulic_diameter, slurry_density, slurry_viscosity)
#     alpha_ff = wec.calc_friction_colebrook(hydraulic_diameter, NRe, openhole_roughness)     #friction factor above dune
#     screen_oh_dp = wec.calc_DPf(alpha_ff, slurry_density, transport_velocity, hydraulic_diameter, 1)
    
#     #inner loop finds rates to satisfy dPscr_oh = dPwp_scr with Newton-Raphson method
#     #outer loop verifies that change in sand concentration is low once fluid rates are solved
#     exit_converged_c = 1      #exits if converged
#     loop_counter_c = 1        #limits number of loops to prevent lockup
#     while abs(exit_converged_c) > 0.001 and loop_counter_c < 100:    #final check if sand concentration change is small
#         exit_converged_dP = 1      #exits if converged
#         loop_counter = 1        #limits number of loops to prevent lockup
#         q1 = screen_oh_rate     #bpm
#         dq = 0.001              #bpm
#         while abs(exit_converged_dP) > 0.01 and loop_counter < 100:     #dPscr_oh = dPwp_scr(q)
#             #first estimate, q = q_wp_scr
#             q = q1

#             wp_screen_vel = wec.calc_fluid_velocity(q, screen_id, washpipe_od)
#             NRe = wec.calc_NRe_newton(wp_screen_vel, screen_id - washpipe_od, fluid_density, fluid_viscosity)
#             wp_screen_ff = wec.calc_friction_colebrook(screen_id - washpipe_od, NRe, screen_roughness)
#             wp_screen_dp1 = wec.calc_DPf(wp_screen_ff, fluid_density, wp_screen_vel, screen_id - washpipe_od, 1) * wec.calc_eccentricity_factor_powerlaw(nPrime, NRe, screen_id, washpipe_od, eccentricity_wp)

#             #NRe = wec.calc_NRe_newton(wec.calc_fluid_velocity(q, washpipe_od, screen_id), screen_id - washpipe_od, fluid_density, fluid_viscosity)
#             #wp_screen_ff = wec.calc_friction_colebrook(screen_id - washpipe_od, NRe, screen_roughness)
#             #wp_screen_dp1 = wec.calc_DPf(wp_screen_ff, fluid_density, wec.calc_fluid_velocity(q, washpipe_od, screen_id), screen_id - washpipe_od, 1) * wec.calc_eccentricity_factor_powerlaw(nPrime, NRe, screen_id, washpipe_od, eccentricity_wp)
            
#             #second calc, q2
#             q = q1 + dq
            
#             wp_screen_vel = wec.calc_fluid_velocity(q, screen_id, washpipe_od)
#             NRe = wec.calc_NRe_newton(wp_screen_vel, screen_id - washpipe_od, fluid_density, fluid_viscosity)
#             wp_screen_ff = wec.calc_friction_colebrook(screen_id - washpipe_od, NRe, screen_roughness)
#             wp_screen_dp2 = wec.calc_DPf(wp_screen_ff, fluid_density, wp_screen_vel, screen_id - washpipe_od, 1) * wec.calc_eccentricity_factor_powerlaw(nPrime, NRe, screen_id, washpipe_od, eccentricity_wp)

#             #NRe = wec.calc_NRe_newton(wec.calc_fluid_velocity(q, washpipe_od, screen_id), screen_id - washpipe_od, fluid_density, fluid_viscosity)
#             #wp_screen_ff = wec.calc_friction_colebrook(screen_id - washpipe_od, NRe, screen_roughness)
#             #wp_screen_dp2 = wec.calc_DPf(wp_screen_ff, fluid_density, wec.calc_fluid_velocity(q, washpipe_od, screen_id), screen_id - washpipe_od, 1) * wec.calc_eccentricity_factor_powerlaw(nPrime, NRe, screen_id, washpipe_od, eccentricity_wp)

#             y1 = screen_oh_dp - wp_screen_dp1
#             y2 = screen_oh_dp - wp_screen_dp2
#             q2 = q1 - y1 / ((y2 - y1) / dq)
#             exit_converged_dP = q2 - q1
#             loop_counter = loop_counter + 1
#             q1 = q2

#             #calculate new proppant loading based on fluid rates from dP, and update calculations above dune
#             solid_loading_oh = solid_loading * (screen_oh_rate + q1) / screen_oh_rate
#             c1 = solid_loading_oh / (solid_density * 8.34 + solid_loading_oh)
#             slurry_viscosity = fluid_viscosity * wec.calc_slurry_viscosity(solid_loading_oh, solid_density * 8.34, fluid_density)
#             slurry_density = wec.calc_slurry_density(fluid_density, solid_absVol, solid_loading_oh)

#             if model == 'SGS':
#                 transport_velocity = wec.calc_horizontal_transport_SGS(equivalent_diameter, solid_diameter, solid_density * 8.34, fluid_density, fluid_viscosity, c1, dune_height, openhole_id)
#             elif model == 'SGS alt':
#                 transport_velocity = wec.calc_horizontal_transport_SGS_alt(equivalent_diameter, solid_diameter, solid_density * 8.34, fluid_density, fluid_viscosity, c1, width_o - width_i, perimeter_o + perimeter_i)
#             elif model == 'Oroskar':
#                 transport_velocity = wec.calc_horizontal_transport_Oroskar(equivalent_diameter, solid_diameter, solid_density * 8.34, fluid_density, fluid_viscosity, c)
#             elif model == 'Oroskar mod':
#                 transport_velocity = wec.calc_horizontal_transport_OroskarMod(equivalent_diameter, solid_diameter, solid_density * 8.34, fluid_density, fluid_viscosity, c1)
#             elif model == 'Hang':
#                 transport_velocity = wec.calc_horizontal_transport_Hang(hydraulic_diameter, solid_diameter, solid_density * 8.34, fluid_density, slurry_density, fluid_viscosity)
            
#             screen_oh_rate = ucon(transport_velocity * flow_area / 144, 'ft\u00b3', 'bbl') * 60
#             NRe = wec.calc_NRe_newton(transport_velocity, hydraulic_diameter, slurry_density, slurry_viscosity)
#             alpha_ff = wec.calc_friction_colebrook(hydraulic_diameter, NRe, openhole_roughness)
#             screen_oh_dp = wec.calc_DPf(alpha_ff, slurry_density, transport_velocity, hydraulic_diameter, 1)
            
#         loop_counter_c = loop_counter_c + 1
#         exit_converged_c = c1 - c
#         c = c1

#     #calculate final washpipe-screen dP
#     wp_screen_rate = q1
#     wp_screen_velocity = wec.calc_fluid_velocity(wp_screen_rate, screen_id, washpipe_od)
#     NRe = wec.calc_NRe_newton(wp_screen_velocity, screen_id - washpipe_od, fluid_density, fluid_viscosity)
#     wp_screen_ff = wec.calc_friction_colebrook(screen_id - washpipe_od, NRe, screen_roughness)
#     washpipe_screen_dp = wec.calc_DPf(wp_screen_ff, fluid_density, wp_screen_velocity, screen_id - washpipe_od, 1) * wec.calc_eccentricity_factor_powerlaw(nPrime, NRe, screen_id, washpipe_od, eccentricity_wp)
    
#     #with rates solved, allow for losses in reported input rate
#     leakoff_rate = 0
#     return_rate = screen_oh_rate + wp_screen_rate
#     pump_rate = screen_oh_rate + wp_screen_rate + leakoff_rate

#     #solve for beta wave with pump rate
#     wp_screen_velocity_beta = wec.calc_fluid_velocity(pump_rate, screen_id, washpipe_od)
#     NRe = wec.calc_NRe_newton(wp_screen_velocity, screen_id - washpipe_od, fluid_density, fluid_viscosity)
#     wp_screen_ff_beta = wec.calc_friction_colebrook(screen_id - washpipe_od, NRe, screen_roughness)
#     washpipe_screen_dp_beta = wec.calc_DPf(wp_screen_ff_beta, fluid_density, wp_screen_velocity_beta, screen_id - washpipe_od, 1) * wec.calc_eccentricity_factor_powerlaw(nPrime, NRe, screen_id, washpipe_od, eccentricity_wp)

#     #solve for washpipe dP with return rate
#     washpipe_velocity = wec.calc_fluid_velocity(return_rate, washpipe_id)
#     NRe = wec.calc_NRe_newton(washpipe_velocity, washpipe_id, fluid_density, fluid_viscosity)
#     washpipe_ff = wec.calc_friction_colebrook(washpipe_id, NRe, washpipe_roughness)
#     washpipe_dp = wec.calc_DPf(washpipe_ff, fluid_density, washpipe_velocity, washpipe_id, 1)

#     #with overall pump rate, calculate full open dP with clean fluid
    
#     output = AlphaWave(dune_height_ratio, dune_height, hydraulic_diameter, equivalent_diameter, area_o, area_i, perimeter_o, perimeter_i, width_o, width_i, 
#                             transport_velocity, screen_oh_rate, wp_screen_rate, pump_rate, return_rate, screen_oh_dp, washpipe_screen_dp)
#     return output
