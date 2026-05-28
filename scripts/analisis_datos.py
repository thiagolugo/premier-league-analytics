import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# LECTURA DEL DATASET
# ==========================================

df = pd.read_csv(
    "datos/premier_league.csv",
    encoding="latin1"
)

# ==========================================
# CALCULO DE PUNTOS
# ==========================================

df["HomePoints"] = df.apply(
    lambda x: 3 if x["FTHG"] > x["FTAG"]
    else 1 if x["FTHG"] == x["FTAG"]
    else 0,
    axis=1
)

df["AwayPoints"] = df.apply(
    lambda x: 3 if x["FTAG"] > x["FTHG"]
    else 1 if x["FTAG"] == x["FTHG"]
    else 0,
    axis=1
)

# ==========================================
# TABLA LOCAL
# ==========================================

home_table = df.groupby("HomeTeam").agg({
    "HomePoints": "sum",
    "FTHG": "sum"
}).reset_index()

home_table.columns = ["Equipo", "Puntos", "Goles"]

# ==========================================
# TABLA VISITANTE
# ==========================================

away_table = df.groupby("AwayTeam").agg({
    "AwayPoints": "sum",
    "FTAG": "sum"
}).reset_index()

away_table.columns = ["Equipo", "Puntos", "Goles"]

# ==========================================
# TABLA FINAL
# ==========================================

tabla = pd.concat([home_table, away_table])

tabla_final = tabla.groupby("Equipo").sum().reset_index()

tabla_final = tabla_final.sort_values(
    by="Puntos",
    ascending=False
)

# ==========================================
# MOSTRAR TABLA
# ==========================================

print("\nTABLA DE POSICIONES\n")

print(tabla_final)

# ==========================================
# PROMEDIO GOLES
# ==========================================

promedio_goles = (
    df["FTHG"].sum() +
    df["FTAG"].sum()
) / len(df)

print("\nPROMEDIO DE GOLES POR PARTIDO:")

print(round(promedio_goles, 2))

# ==========================================
# GRAFICO
# ==========================================

plt.figure(figsize=(14,7))

plt.bar(
    tabla_final["Equipo"],
    tabla_final["Puntos"]
)

plt.xticks(rotation=90)

plt.title("Puntos por Equipo - Premier League")

plt.xlabel("Equipos")

plt.ylabel("Puntos")

plt.tight_layout()

# ==========================================
# GUARDAR GRAFICO
# ==========================================

plt.savefig(
    "resultados/grafico_resultados.png"
)

print("\nGrafico guardado en /resultados")
