import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. Definisi variabel
suhu = ctrl.Antecedent(np.arange(0, 41, 1), 'suhu')
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')
kecepatan = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan')

# 2. Membership function (3 himpunan tiap variabel)
suhu['rendah'] = fuzz.trimf(suhu.universe, [0, 0, 20])
suhu['sedang'] = fuzz.trimf(suhu.universe, [10, 20, 30])
suhu['tinggi'] = fuzz.trimf(suhu.universe, [20, 40, 40])

kelembapan['rendah'] = fuzz.trimf(kelembapan.universe, [0, 0, 50])
kelembapan['sedang'] = fuzz.trimf(kelembapan.universe, [25, 50, 75])
kelembapan['tinggi'] = fuzz.trimf(kelembapan.universe, [50, 100, 100])

kecepatan['lambat'] = fuzz.trimf(kecepatan.universe, [0, 0, 50])
kecepatan['sedang'] = fuzz.trimf(kecepatan.universe, [25, 50, 75])
kecepatan['cepat'] = fuzz.trimf(kecepatan.universe, [50, 100, 100])

# 3. Aturan fuzzy (lengkap 3x3)
rule1 = ctrl.Rule(suhu['rendah'] & kelembapan['rendah'], kecepatan['lambat'])
rule2 = ctrl.Rule(suhu['rendah'] & kelembapan['sedang'], kecepatan['lambat'])
rule3 = ctrl.Rule(suhu['rendah'] & kelembapan['tinggi'], kecepatan['sedang'])

rule4 = ctrl.Rule(suhu['sedang'] & kelembapan['rendah'], kecepatan['lambat'])
rule5 = ctrl.Rule(suhu['sedang'] & kelembapan['sedang'], kecepatan['sedang'])
rule6 = ctrl.Rule(suhu['sedang'] & kelembapan['tinggi'], kecepatan['cepat'])

rule7 = ctrl.Rule(suhu['tinggi'] & kelembapan['rendah'], kecepatan['sedang'])
rule8 = ctrl.Rule(suhu['tinggi'] & kelembapan['sedang'], kecepatan['cepat'])
rule9 = ctrl.Rule(suhu['tinggi'] & kelembapan['tinggi'], kecepatan['cepat'])

# 4. Sistem kontrol
kipas_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3,
    rule4, rule5, rule6,
    rule7, rule8, rule9
])

kipas_sim = ctrl.ControlSystemSimulation(kipas_ctrl)

# 5. Input
kipas_sim.input['suhu'] = 30
kipas_sim.input['kelembapan'] = 70

# 6. Proses
kipas_sim.compute()

# 7. Output
hasil = kipas_sim.output['kecepatan']
print("Kecepatan kipas:", round(hasil, 2))

# 8. Visualisasi (opsional, tapi disarankan)
kecepatan.view(sim=kipas_sim)
plt.show()