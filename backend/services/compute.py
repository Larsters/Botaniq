import pandas as pd
import numpy as np

df = pd.read_csv("extracted_data.csv")

# Heat Stress day
# Crop-specific thresholds
df["HeatStress"] = 9 * ((df["TMAX"] - 30) / (40 - 30)) 

# Drought Index
df["DroughtIndex"] = (df["Precipitation"] - df["Evapotranspiration"] + df["SoilMoisture"]) / df["TAVG"]

# Frost stress 
df["FrostStress"] = np.where(df["TMIN"] < 0, 1, 0)

# Crop-specific optimal values
crop_optimal_values = {
    "Soybean": {"GDD_opt": 2700, "P_opt": 575, "pH_opt": 6.4, "N_opt": 0.013},
    "Corn": {"GDD_opt": 2900, "P_opt": 650, "pH_opt": 6.4, "N_opt": 0.115},
    "Cotton": {"GDD_opt": 2400, "P_opt": 1000, "pH_opt": 6.3, "N_opt": 0.072},
}

# Define weighting factors for Yield Risk
w1, w2, w3, w4 = 0.3, 0.3, 0.2, 0.2

# Compute Yield Risk
df["YieldRisk"] = df.apply(lambda row: (
    w1 * (row["GDD"] - crop_optimal_values[row["Crop"]]["GDD_opt"])**2 +
    w2 * (row["Precipitation"] - crop_optimal_values[row["Crop"]]["P_opt"])**2 +
    w3 * (row["pH"] - crop_optimal_values[row["Crop"]]["pH_opt"])**2 +
    w4 * (row["N_Actual"] - crop_optimal_values[row["Crop"]]["N_opt"])**2
), axis=1)

# Rainfall Factor (RF) and Soil Moisture Factor (SMF)
df["RF"] = df["Precipitation"] / df["P_opt"]
df["SMF"] = df["SoilMoisture"] / 0.6  # Example optimal soil moisture = 60%

# Compute NUE
df["NUE"] = (df["Projected_Yield"] / df["N_Actual"]) * df["RF"] * df["SMF"]

# Compute pH Factor (pHf) for PUE
df["pHf"] = df["pH"] / crop_optimal_values[df["Crop"]]["pH_opt"]

# Compute Soil Factor (SF) for PUE
df["SF"] = (df["pHf"] + df["SMF"] + df["RF"]) / 3

# Compute PUE
df["PUE"] = (df["Projected_Yield"] / df["P_Actual"]) * df["SF"]

df.to_csv("final_dataset.csv", index=False)