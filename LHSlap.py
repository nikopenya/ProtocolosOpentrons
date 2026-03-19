import pandas as pd
from scipy.stats import qmc

def generar_diseno_96_ordenado():
    # 1. Generar el diseño LHS (d=2: PEGDA e Iniciador)
    sampler = qmc.LatinHypercube(d=2, optimization="random-cd")
    muestra = sampler.random(n=96)
    
    # 2. Escalar a tus rangos: PEGDA (6-32%) e Iniciador (0.05-0.2%)
    l_bounds = [10, 0.05]
    u_bounds = [30, 0.2]
    tabla = qmc.scale(muestra, l_bounds, u_bounds)
    
    # 3. Crear el DataFrame
    df = pd.DataFrame(tabla, columns=['%_PEGDA', '%_Iniciador_LAP'])
    
    # --- LA PARTE NUEVA: ORDENAR ---
    # Ordenamos por la columna del iniciador de forma ascendente (creciente)
    df_ordenado = df.sort_values(by='%_Iniciador_LAP', ascending=True)
    
    # 4. Guardar el Excel
    df_ordenado.to_excel("diseno_experimental_96_ORDENADO.xlsx", index=False) 
    
    print("¡Excel generado y ordenado por concentración de LAP!")
    return df_ordenado

# Ejecutar
generar_diseno_96_ordenado()