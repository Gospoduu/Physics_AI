# import
import pandas as pd
import numpy as np
import json
from utils import min_mse
import plotly.express as px
import os

#%%
# constants

ALPHA = 1/137
PI = np.pi

m_p_n = 1.67 * (10**-24)

#%%
# input data
element = input("Введите название элемента") # choose any
EeV = float(input("Введите E(eV)"))
#%% md

#%%
# data from element
path = "data/updated_periodic_table.csv"
periodic_table = pd.read_csv(path, usecols=[1, 3, 4, 20, 29])

periodic_table.columns = ["Z", "Symbol", "N", "ro", "chi"]
periodic_table.columns
data = periodic_table[periodic_table["Symbol"] == element]
#%%
# vars
Z = data["Z"].iloc[0]
N = data["N"].iloc[0]
ro = data["ro"].iloc[0]
chi = data["chi"].iloc[0]
print("Z =", Z, "N =", N, "ro =", ro,"chi =", chi)
#%%
# ather vars
m_e = 0.18 * (10**-24)
m_a = (N * m_p_n + Z * m_e)
n0_m = (ro / (5 * m_a))
k_n0_m = (n0_m * 10**4) / 125
om2 = ((4 * PI * Z) / 137) * k_n0_m
print("m_e = ", m_e, "m_a = ", m_a, "n0_m = ", n0_m, "k_n0_m = ", k_n0_m, "om2 = ", om2)


#%%
# get chi from JSON
chi_string = chi.replace("'", '"')
chi_dct = json.loads(chi_string)
dict_values = [float(i) for i in chi_dct]
dict_values[:5]
#%%
# vars
EeV_s = min_mse(EeV, dict_values)
omega = EeV_s * 10**5 /2
omega0 = (om2**0.5) * 10**5 /2

f1, f2 = chi_dct[str(EeV_s)].values()
X1 = (-f1/Z )* (omega0/omega)**2
#%%
# func and get x/y func
def get_y(theta, gamma, x1):
    return ALPHA/(PI**2) * theta ** 2 * (1/(theta** 2 + 1/(gamma**2)) - 1/(theta**2 + 1/(gamma**2) - x1))**2


def get_XY_for_plot(theta_cnt, gamma, x1, min_theta=-0.02, max_theta=0.02):
    x = np.linspace(min_theta, max_theta, theta_cnt )

    y = np.copy(x)
    for idx, theta in enumerate(x):
        y[idx] = get_y(theta, gamma, x1)
    return x, y

#%%
# graph
x_1, y_1 = get_XY_for_plot(1000, 500, X1)
x_2, y_2 = get_XY_for_plot(1000, 400, X1)


df = pd.DataFrame({
    "theta": np.concatenate([x_1, x_2]),
    "y": np.concatenate([y_1, y_2]),
    "label": ["График 1"] * len(x_1) + ["График 2"] * len(x_2)
})

fig = px.line(df, x="theta", y="y", color="label")


fig.update_layout(
    template="plotly_white"
)
fig.show()