import numpy as np
import matplotlib.pyplot as plt

# Dados
tf = 2.0  # tempo final (s)
R = 0.02  # raio da polia (m)
xP1, yP1 = -0.2, 0  # posição da polia 1 (m)
xP2, yP2 =  0.2, 0  # posição da polia 2 (m)

# Condições de contorno para x1
x0, vx0, ax0 = 0.0, 0.0, 0.0
xf, vxf, axf = 0.2, 0.0, 0.0

# Condições de contorno para y1
y0, vy0, ay0 = 0.0, 0.0, 0.0
yf, vyf, ayf = 0.1, 0.0, 0.0

# Montar o sistema para polinômio quintico
def quintic_coefficients(p0, v0, a0, pf, vf, af, tf):
    M = np.array([
        [1, 0, 0,    0,    0,    0],
        [0, 1, 0,    0,    0,    0],
        [0, 0, 2,    0,    0,    0],
        [1, tf, tf**2, tf**3, tf**4, tf**5],
        [0, 1, 2*tf, 3*tf**2, 4*tf**3, 5*tf**4],
        [0, 0, 2,    6*tf, 12*tf**2, 20*tf**3],
    ])
    b = np.array([p0, v0, a0, pf, vf, af])
    a = np.linalg.solve(M, b)
    return a

# Coeficientes
ax = quintic_coefficients(x0, vx0, ax0, xf, vxf, axf, tf)
ay = quintic_coefficients(y0, vy0, ay0, yf, vyf, ayf, tf)

# Funções de trajetória
def x1(t): return np.polyval(ax[::-1], t)
def y1(t): return np.polyval(ay[::-1], t)

# Cálculo dos comprimentos dos cabos
def L1(t): return np.sqrt((x1(t) - xP1)**2 + (y1(t) - yP1)**2)
def L2(t): return np.sqrt((xP2 - x1(t))**2 + (yP2 - y1(t))**2)

# Ângulos das polias
L10 = L1(0)
L20 = L2(0)
def phi1(t): return (L10 - L1(t)) / R
def phi2(t): return (L20 - L2(t)) / R

# Simulação
t_vec = np.linspace(0, tf, 500)
x_vec = x1(t_vec)
y_vec = y1(t_vec)
phi1_vec = phi1(t_vec)
phi2_vec = phi2(t_vec)

# Plot
plt.figure(figsize=(12,6))

plt.subplot(2,2,1)
plt.plot(t_vec, x_vec, label='x1(t)')
plt.plot(t_vec, y_vec, label='y1(t)')
plt.title('Trajetória do ponto (x1, y1)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.legend()
plt.grid()

plt.subplot(2,2,2)
plt.plot(t_vec, phi1_vec, label='phi1(t)')
plt.plot(t_vec, phi2_vec, label='phi2(t)')
plt.title('Ângulos das Polias')
plt.xlabel('Tempo (s)')
plt.ylabel('Ângulo (rad)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
