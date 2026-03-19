import pandas as pd
from scipy.stats import qmc

def generar_diseno_96_RF():
    # 1. Generar el diseño LHS (d=2: PEGDA e Iniciador)
    sampler = qmc.LatinHypercube(d=3, optimization="random-cd")
    muestra = sampler.random(n=96)
    
    # 2. Escalar a tus rangos: PEGDA (10-30%) - RF (0.01-0.1%) - TEA (0.5 - 2%)
    l_bounds = [10, 0.01, 0.5]
    u_bounds = [30, 0.1, 2]
    tabla = qmc.scale(muestra, l_bounds, u_bounds)
    
    # 3. Crear el DataFrame
    df = pd.DataFrame(tabla, columns=['%_PEGDA', '%_RF', '%_TEA'])
    
    # 4. Guardar el Excel
    df.to_excel("diseno_experimental_96_RF.xlsx", index=False) 
    
    print("¡Excel generado!")
    return df

# Ejecutar
generar_diseno_96_RF()