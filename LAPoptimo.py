from opentrons import protocol_api
from opentrons.protocol_api import SINGLE

# Metadatos del protocolo
metadata = {
    'protocolName': 'Sintesis Automatizada de Hidrogeles PEGDA-LAP optimizado (LHS Design)',
    'author': 'NicoPeña',
    'description': 'Preparacion de 96 muestras con gradientes de PEGDA y LAP usando Latin Hypercube Sampling.',
}

requirements = {"robotType": "Flex", "apiLevel": "2.21"}

def run(protocol: protocol_api.ProtocolContext):
    muestras = [
        ("A1", 90.14, 20.09, 89.77), ("A2", 38.82, 20.92, 140.27), ("A3", 78.98, 21.65, 99.36),
        ("A4", 62.43, 22.31, 115.26), ("A5", 55.08, 22.81, 122.11), ("A6", 49.29, 23.61, 127.10),
        ("A7", 99.08, 23.80, 77.12), ("A8", 71.25, 24.66, 104.09), ("A9", 66.80, 25.48, 107.72),
        ("A10", 83.63, 25.79, 90.58), ("A11", 43.57, 26.66, 129.76), ("A12", 36.18, 27.27, 136.55),
        ("B1", 80.80, 27.95, 91.25), ("B2", 60.16, 28.15, 111.69), ("B3", 86.52, 29.12, 84.35),
        ("B4", 49.90, 29.38, 120.72), ("B5", 93.55, 30.21, 76.24), ("B6", 73.33, 31.04, 95.63),
        ("B7", 45.79, 31.84, 122.38), ("B8", 97.83, 32.36, 69.81), ("B9", 42.17, 32.93, 124.90),
        ("B10", 76.30, 33.70, 90.00), ("B11", 64.71, 34.34, 100.96), ("B12", 54.30, 34.48, 111.22),
        ("C1", 58.35, 35.58, 106.07), ("C2", 35.32, 36.18, 128.50), ("C3", 88.98, 36.32, 74.70),
        ("C4", 70.08, 37.24, 92.68), ("C5", 91.15, 38.06, 70.79), ("C6", 57.08, 38.54, 104.38),
        ("C7", 75.59, 38.88, 85.54), ("C8", 39.64, 39.63, 120.73), ("C9", 96.08, 40.33, 63.59),
        ("C10", 47.17, 40.90, 111.93), ("C11", 65.65, 41.48, 92.88), ("C12", 84.42, 42.47, 73.11),
        ("D1", 78.03, 42.95, 79.02), ("D2", 34.01, 43.40, 122.59), ("D3", 52.07, 43.91, 104.02),
        ("D4", 93.85, 44.78, 61.37), ("D5", 63.85, 45.16, 90.99), ("D6", 87.84, 45.73, 66.43),
        ("D7", 42.74, 46.76, 110.50), ("D8", 80.34, 47.39, 72.27), ("D9", 68.09, 48.12, 83.78),
        ("D10", 54.00, 48.41, 97.59), ("D11", 51.33, 49.29, 99.38), ("D12", 85.52, 49.61, 64.87),
        ("E1", 73.85, 50.52, 75.63), ("E2", 39.30, 51.14, 109.56), ("E3", 98.12, 51.83, 50.05),
        ("E4", 70.29, 52.21, 77.50), ("E5", 61.41, 52.56, 86.03), ("E6", 40.53, 53.61, 105.86),
        ("E7", 60.47, 54.30, 85.23), ("E8", 92.78, 54.53, 52.69), ("E9", 82.40, 55.47, 62.12),
        ("E10", 48.09, 55.95, 95.95), ("E11", 85.08, 56.60, 58.33), ("E12", 46.40, 57.22, 96.38),
        ("F1", 76.84, 57.92, 65.24), ("F2", 35.78, 58.35, 105.87), ("F3", 94.49, 59.35, 46.16),
        ("F4", 58.26, 59.38, 82.36), ("F5", 69.19, 60.48, 70.33), ("F6", 53.19, 61.08, 85.73),
        ("F7", 72.80, 61.56, 65.64), ("F8", 99.75, 62.43, 37.82), ("F9", 44.60, 62.84, 92.56),
        ("F10", 63.89, 63.70, 72.40), ("F11", 81.54, 64.15, 54.31), ("F12", 38.11, 64.59, 97.30),
        ("G1", 88.80, 65.58, 45.62), ("G2", 66.46, 65.98, 67.56), ("G3", 47.63, 66.63, 85.74),
        ("G4", 79.83, 67.19, 52.98), ("G5", 56.30, 67.58, 76.12), ("G6", 74.69, 68.47, 56.84),
        ("G7", 95.18, 69.01, 35.81), ("G8", 34.57, 69.51, 95.92), ("G9", 52.62, 70.23, 77.15),
        ("G10", 86.92, 70.82, 42.27), ("G11", 67.38, 71.80, 60.82), ("G12", 59.45, 71.98, 68.57),
        ("H1", 92.11, 72.83, 35.05), ("H2", 50.11, 73.30, 76.60), ("H3", 44.10, 74.10, 81.80),
        ("H4", 96.95, 74.50, 28.55), ("H5", 62.92, 75.15, 61.93), ("H6", 77.19, 76.03, 46.78),
        ("H7", 71.73, 76.67, 51.60), ("H8", 36.93, 76.93, 86.14), ("H9", 90.86, 77.94, 31.20),
        ("H10", 41.32, 78.58, 80.10), ("H11", 55.58, 79.18, 65.24), ("H12", 82.78, 79.40, 37.82)
    ]

    # --- 1. CARGA DE LABWARE ---
    trash = protocol.load_trash_bin("A3")
    tipracks = protocol.load_labware("opentrons_flex_96_tiprack_200ul", "D3")
    res = protocol.load_labware("custom_4_reservoir_90000ul", "D2")
    res_lapeg = protocol.load_labware("19mlglass_15_tuberack_19000ul", "C2")
    h_s = protocol.load_module('heaterShakerModuleV1', 'C1') 
    plate = h_s.load_labware("corning_96_wellplate_360ul_flat")

    # --- 2. PIPETTE ---
    pipette = protocol.load_instrument("flex_8channel_1000", mount="left", tip_racks=[tipracks])
    pipette.configure_nozzle_layout(style=SINGLE, start="H1")

    # --- 3. SEGURIDAD: CERRAR LATCH ---
    # Esto habilita el movimiento sobre el módulo Heater-Shaker
    h_s.close_labware_latch()

    # --- 4. REACTIVOS ---
    pegda_60 = res_lapeg['B3']
    agua = res['A1']
    lap_05 = res_lapeg['A1']

    vol_max_p200 = 190

    # --- LOGICA DE EJECUCION ---

    # PASO 1: AGUA
    protocol.comment("Distribuyendo Agua...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 40
    pipette.flow_rate.blow_out = 50
    
    pipette.pick_up_tip(tipracks['A1'])
    for well, v_peg, v_lap, v_agua in muestras:
        pipette.aspirate(v_agua, agua.bottom(z=3))
        pipette.dispense(v_agua, plate[well].top(z=2))
        pipette.blow_out(plate[well].top(z=-2))
        protocol.delay(seconds=2)
    pipette.drop_tip(trash)

    # PASO 2: PEGDA
    protocol.comment("Distribuyendo Pegda...")
    pipette.flow_rate.aspirate = 30
    pipette.flow_rate.dispense = 30
    pipette.flow_rate.blow_out = 40
    
    pipette.pick_up_tip(tipracks['A2'])
    for well, v_peg, v_lap, v_agua in muestras:
        pipette.aspirate(v_peg, pegda_60.bottom(z=15))
        protocol.delay(seconds=3) 
        pipette.move_to(pegda_60.top(z=5),speed=10)
        pipette.dispense(v_peg, plate[well].top(z=2))
        pipette.blow_out(plate[well].top(z=-2))
        protocol.delay(seconds=2)
    pipette.drop_tip(trash)

    # PASO 3: LAP
    protocol.comment("Distribuyendo LAP...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 40
    
    pipette.pick_up_tip(tipracks['A3'])
    liquido_en_punta = 0
    for well, v_peg, v_lap, v_agua in muestras:
        if liquido_en_punta < (v_lap + 10):
            espacio_libre = vol_max_p200 - liquido_en_punta
            pipette.aspirate(espacio_libre, lap_05.bottom(z=15))
            liquido_en_punta = vol_max_p200
        pipette.dispense(v_lap, plate[well].top(z=2))
        pipette.touch_tip(v_offset=-3, speed=5)#demasiado fuerte lol cambiar
        protocol.delay(seconds=2)
        liquido_en_punta -= v_lap
    pipette.drop_tip(trash)

     # --- 7. FINALIZACIÓN ---
    protocol.comment("Iniciando agitación...")
    h_s.set_and_wait_for_shake_speed(1000)
    protocol.delay(minutes=2)
    h_s.deactivate_shaker()
    h_s.open_labware_latch()
    protocol.comment("Protocolo terminado.")
