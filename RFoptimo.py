from opentrons import protocol_api
from opentrons.protocol_api import SINGLE

metadata = {
    "protocolName": "Protocolo PEGDA-RIBOFLAVINA-TEA Optimizado Final",
    "author": "NicolasPeña",
    "description": "Dispensación con control de stocks y seguridad de Shaker",
}

requirements = {"robotType": "Flex", "apiLevel": "2.21"}

def run(protocol: protocol_api.ProtocolContext):

    # --- 1. CARGA DE LABWARE ---
    trash = protocol.load_trash_bin("A3")
    tipracks = protocol.load_labware("opentrons_flex_96_tiprack_200ul", "B1")
    res = protocol.load_labware("custom_4_reservoir_90000ul", "D2")
    res_tea = protocol.load_labware("custom_24_tuberack_6000ul", "D1")
    
    # Definimos el módulo como h_s
    h_s = protocol.load_module('heaterShakerModuleV1', 'D3') 
    plate = h_s.load_labware("corning_96_wellplate_360ul_flat")

    # --- 2. CARGA DE INSTRUMENTOS ---
    pipette = protocol.load_instrument("flex_8channel_1000", mount="left", tip_racks=[tipracks])
    pipette.configure_nozzle_layout(style=SINGLE, start="H1")

    # --- 3. SEGURIDAD: CERRAR LATCH (Soluciona error PipetteMovementRestricted) ---
    h_s.close_labware_latch()

    # --- 4. DEFINICIÓN DE REACTIVOS ---
    rf_04 = res['A1']
    rf_01 = res['A2']
    pegda_60 = res['A3']
    agua = res['A4']
    tea_5 = res_tea['A1']
    tea_10 = res_tea['A2']

    # --- 5. DATOS DE VOLÚMENES ---
    vol_agua_peg_rf = [
        ("A1", 38.56, 90.36, 21.45), ("A2", 48.13, 85.49, 22.61), ("A3", 103.57, 46.07, 23.95),
        ("A4", 89.15, 49.73, 25.83), ("A5", 43.45, 97.93, 28.40), ("A6", 67.35, 61.58, 30.10),
        ("A7", 82.17, 53.60, 32.62), ("A8", 96.19, 35.79, 33.96), ("A9", 57.85, 73.04, 35.05),
        ("A10", 53.29, 78.27, 37.86), ("A11", 44.94, 89.23, 39.52), ("A12", 45.49, 74.21, 41.09),
        ("B1", 80.86, 53.05, 43.23), ("B2", 33.07, 83.34, 46.22), ("B3", 84.07, 35.08, 47.32),
        ("B4", 55.99, 68.38, 48.26), ("B5", 59.15, 59.81, 51.82), ("B6", 22.48, 96.86, 53.05),
        ("B7", 44.12, 64.76, 54.14), ("B8", 58.74, 38.01, 56.83), ("B9", 48.32, 42.19, 58.08),
        ("B10", 38.67, 65.95, 59.76), ("B11", 68.68, 81.38, 15.72), ("B12", 74.87, 71.06, 15.84),
        ("C1", 115.33, 39.54, 16.48), ("C2", 66.63, 94.16, 17.12), ("C3", 96.96, 46.55, 17.48),
        ("C4", 56.91, 92.81, 17.88), ("C5", 80.56, 74.46, 18.31), ("C6", 85.14, 57.94, 19.04),
        ("C7", 76.70, 57.30, 19.11), ("C8", 54.68, 92.17, 19.96), ("C9", 110.66, 41.06, 20.14),
        ("C10", 45.27, 87.70, 20.82), ("C11", 89.52, 54.79, 21.00), ("C12", 95.21, 47.84, 21.59),
        ("D1", 60.91, 80.40, 21.92), ("D2", 56.59, 69.87, 22.70), ("D3", 79.10, 67.24, 22.94),
        ("D4", 88.16, 48.59, 23.37), ("D5", 64.83, 85.16, 24.11), ("D6", 42.31, 94.63, 24.59),
        ("D7", 107.35, 37.05, 25.02), ("D8", 69.76, 76.90, 25.17), ("D9", 92.93, 60.93, 25.71),
        ("D10", 60.66, 70.28, 26.47), ("D11", 80.53, 43.78, 26.62), ("D12", 64.90, 81.00, 27.05),
        ("E1", 35.23, 99.52, 27.92), ("E2", 88.43, 50.95, 28.25), ("E3", 92.19, 50.15, 28.71),
        ("E4", 71.42, 63.30, 29.08), ("E5", 41.36, 89.79, 29.68), ("E6", 95.85, 40.61, 30.25),
        ("E7", 72.95, 74.63, 30.70), ("E8", 43.54, 95.66, 30.85), ("E9", 85.79, 55.74, 31.65),
        ("E10", 84.38, 42.51, 31.82), ("E11", 57.75, 66.44, 32.25), ("E12", 43.20, 84.63, 32.69),
        ("F1", 78.34, 55.14, 33.56), ("F2", 55.87, 78.92, 33.89), ("F3", 94.38, 43.72, 34.44),
        ("F4", 42.34, 99.17, 34.68), ("F5", 57.33, 76.28, 35.32), ("F6", 85.34, 34.22, 35.70),
        ("F7", 70.03, 62.89, 36.07), ("F8", 85.23, 38.33, 36.74), ("F9", 115.33, 75.18, 37.03),
        ("F10", 39.83, 86.85, 37.64), ("F11", 65.55, 61.85, 38.19), ("F12", 25.03, 91.09, 38.55),
        ("G1", 90.48, 45.79, 39.03), ("G2", 25.92, 82.88, 39.30), ("G3", 58.04, 68.85, 40.13),
        ("G4", 88.13, 40.03, 40.42), ("G5", 30.86, 96.03, 41.02), ("G6", 65.29, 56.86, 41.53),
        ("G7", 37.48, 72.85, 41.97), ("G8", 67.99, 51.94, 42.17), ("G9", 39.25, 67.97, 42.68),
        ("G10", 42.88, 88.62, 43.04), ("G11", 74.23, 52.12, 43.71), ("G12", 35.84, 79.35, 44.32),
        ("H1", 48.26, 58.42, 44.60), ("H2", 43.65, 82.43, 45.02), ("H3", 76.95, 44.93, 45.42),
        ("H4", 25.34, 93.65, 46.23), ("H5", 95.51, 36.71, 46.55), ("H6", 65.93, 59.08, 46.92),
        ("H7", 81.35, 33.42, 47.60), ("H8", 41.97, 71.56, 48.12), ("H9", 35.99, 86.34, 48.13),
        ("H10", 17.47, 97.32, 48.72), ("H11", 58.83, 64.34, 49.08), ("H12", 58.49, 49.10, 49.94)
    ]

    v_tea_5 = [
        ("A1", 49.64), ("A2", 43.77), ("A3", 26.42), ("A8", 34.06), ("A10", 30.57),
        ("B1", 22.87), ("B4", 27.37), ("B8", 46.42), ("B9", 51.41), ("B11", 34.21), ("B12", 38.22),
        ("C1", 28.65), ("C2", 22.09), ("C7", 46.88), ("C10", 46.21), ("D2", 50.83), ("D7", 30.58),
        ("D9", 20.43), ("D10", 42.59), ("D11", 49.07), ("E2", 32.36), ("E4", 36.19), ("E5", 39.16),
        ("E7", 21.72), ("F1", 32.95), ("F4", 23.81), ("F6", 44.74), ("F12", 45.33), ("G7", 47.70),
        ("G9", 50.09), ("H5", 21.23), ("H10", 36.49)
    ]

    v_tea_10 = [
        ("A4", 23.94), ("A5", 37.89), ("A6", 48.01), ("A7", 51.98), ("A9", 22.04), ("A11", 31.56), ("A12", 38.90),
        ("B2", 36.78), ("B3", 29.54), ("B5", 41.22), ("B6", 28.01), ("B7", 33.45), ("B10", 36.78),
        ("C3", 39.54), ("C4", 32.12), ("C5", 26.78), ("C6", 38.90), ("C8", 44.56), ("C9", 29.01), ("C11", 35.67), ("C12", 42.12),
        ("D1", 36.78), ("D3", 44.56), ("D4", 22.34), ("D5", 29.89), ("D6", 33.45), ("D8", 38.90), ("D12", 26.78),
        ("E1", 31.23), ("E3", 39.54), ("E6", 23.45), ("E8", 28.90), ("E9", 44.56), ("E10", 33.45), ("E11", 27.89), ("E12", 36.78),
        ("F2", 29.89), ("F3", 33.45), ("F5", 38.90), ("F7", 22.34), ("F8", 44.56), ("F9", 26.78), ("F10", 31.23), ("F11", 39.54),
        ("G1", 23.45), ("G2", 28.90), ("G3", 44.56), ("G4", 33.45), ("G5", 27.89), ("G6", 36.78), ("G8", 29.89), ("G10", 33.45), ("G11", 38.90), ("G12", 22.34),
        ("H1", 44.56), ("H2", 26.78), ("H3", 31.23), ("H4", 39.54), ("H6", 23.45), ("H7", 28.90), ("H8", 44.56), ("H9", 33.45), ("H11", 27.89), ("H12", 36.78)
    ]

    # --- 6. EJECUCIÓN ---

    vol_max_p200 = 190

    # PASO 1: AGUA
    protocol.comment("Distribuyendo Agua...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 40
    pipette.pick_up_tip(tipracks['A1'])
    for well, v_agua, v_peg, v_rf in vol_agua_peg_rf:
        pipette.aspirate(v_agua, agua.bottom(z=3))
        pipette.dispense(v_agua, plate[well].top(z=2))
        pipette.blow_out(plate[well].top(z=-2))
        protocol.delay(seconds=2)
    pipette.drop_tip(trash)

    # PASO 2: PEGDA (Viscoso)
    protocol.comment("Distribuyendo Pegda...")
    pipette.flow_rate.aspirate = 30
    pipette.flow_rate.dispense = 30
    pipette.pick_up_tip(tipracks['A2'])
    for well, v_agua, v_peg, v_rf in vol_agua_peg_rf:
        pipette.aspirate(v_peg, pegda_60.bottom(z=3))
        protocol.delay(seconds=3) 
        pipette.move_to(pegda_60.top(z=5),speed=10)
        pipette.dispense(v_peg, plate[well].top(z=2))
        pipette.blow_out(plate[well].top(z=-2))
        protocol.delay(seconds=2)
    pipette.drop_tip(trash)

    # PASO 3: TEA 5%
    protocol.comment("Distribuyendo TEA 5%...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 40
    pipette.pick_up_tip(tipracks['A3'])
    liquido_en_punta = 0
    for well, v_tea5 in v_tea_5:
        if liquido_en_punta < (v_tea5 + 10):
            espacio_libre = vol_max_p200 - liquido_en_punta
            pipette.aspirate(espacio_libre, tea_5.bottom(z=3))
            liquido_en_punta = vol_max_p200
        pipette.dispense(v_tea5, plate[well].top(z=2))
        pipette.touch_tip(v_offset=-3)
        protocol.delay(seconds=2)
        liquido_en_punta -= v_tea5
    pipette.drop_tip(trash)

    # PASO 4: TEA 10%
    pipette.pick_up_tip(tipracks['A4'])
    liquido_en_punta = 0
    for well, v_tea10 in v_tea_10:
       if liquido_en_punta < (v_tea10 + 10):
            espacio_libre = vol_max_p200 - liquido_en_punta
            pipette.aspirate(espacio_libre, tea_10.bottom(z=3))
            liquido_en_punta = vol_max_p200
        pipette.dispense(v_tea10, plate[well].top(z=2))
        pipette.touch_tip(v_offset=-3)
        protocol.delay(seconds=2)
        liquido_en_punta -= v_tea10
    pipette.drop_tip(trash)

    # PASO 5: RF
    pipette.pick_up_tip(tipracks['A5'])
    liquido_en_punta = 0
    numpozo = 0
    for well, v_agua, v_peg, v_rf in vol_agua_peg_rf:
        numpozo += 1
        fuente = rf_01 if numpozo <= 27 else rf_04
        if numpozo == 28:
            pipette.drop_tip(trash)
            pipette.pick_up_tip(tipracks['A6'])
            liquido_en_punta = 0
        if liquido_en_punta < (v_rf + 10):
            espacio_libre = vol_max_p200 - liquido_en_punta
            pipette.aspirate(espacio_libre, fuente.bottom(z=3))
            liquido_en_punta = vol_max_p200
        pipette.dispense(v_rf, plate[well].top(z=2))
        pipette.touch_tip(v_offset=-3)
        protocol.delay(seconds=2)
        liquido_en_punta -= v_rf
    pipette.drop_tip(trash)


    # --- 7. FINALIZACIÓN ---
    h_s.set_and_wait_for_shake_speed(1000)
    protocol.delay(minutes=2)
    h_s.deactivate_shaker() # SOLUCIÓN AL ERROR Attribute_Error
    h_s.open_labware_latch()