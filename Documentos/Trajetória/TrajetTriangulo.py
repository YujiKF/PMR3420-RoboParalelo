import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Dados do sistema
xP1, yP1 = -0.2, 0
xP2, yP2 =  0.2, 0
R = 0.02  # raio da polia

# Pontos do triângulo (150mm de lado)
A = np.array([0.07, 0.15])
B = np.array([0.22, 0.15])
C = np.array([0.145, 0.15 + 0.15 * np.sqrt(3)/2])

# Função para calcular coeficientes de interpolação quintica
def quintic(p0, v0, a0, pf, vf, af, T):
    M = np.array([
        [1, 0, 0,    0,     0,      0],
        [0, 1, 0,    0,     0,      0],
        [0, 0, 2,    0,     0,      0],
        [1, T, T**2, T**3,  T**4,   T**5],
        [0, 1, 2*T,  3*T**2, 4*T**3, 5*T**4],
        [0, 0, 2,    6*T, 12*T**2, 20*T**3]
    ])
    b = np.array([p0, v0, a0, pf, vf, af])
    return np.linalg.solve(M, b)

# Segmentos e coeficientes
T_seg = 2.0  # tempo por segmento
a1_x = quintic(A[0], 0, 0, B[0], 0, 0, T_seg)
a1_y = quintic(A[1], 0, 0, B[1], 0, 0, T_seg)
a2_x = quintic(B[0], 0, 0, C[0], 0, 0, T_seg)
a2_y = quintic(B[1], 0, 0, C[1], 0, 0, T_seg)
a3_x = quintic(C[0], 0, 0, A[0], 0, 0, T_seg)
a3_y = quintic(C[1], 0, 0, A[1], 0, 0, T_seg)

# Avaliação do polinômio
def poly_val(coefs, t):
    return np.polyval(coefs[::-1], t)

def x1(t):
    if t < 2.0:
        return poly_val(a1_x, t)
    elif t < 4.0:
        return poly_val(a2_x, t - 2.0)
    else:
        return poly_val(a3_x, t - 4.0)

def y1(t):
    if t < 2.0:
        return poly_val(a1_y, t)
    elif t < 4.0:
        return poly_val(a2_y, t - 2.0)
    else:
        return poly_val(a3_y, t - 4.0)

# Comprimento dos cabos e ângulos
def L1(t): return np.sqrt((x1(t) - xP1)**2 + (y1(t) - yP1)**2)
def L2(t): return np.sqrt((xP2 - x1(t))**2 + (yP2 - y1(t))**2)

L10 = L1(0)
L20 = L2(0)

def phi1(t): return (L10 - L1(t)) / R
def phi2(t): return (L20 - L2(t)) / R

# Tempo de simulação
t_total = 6.0
fps = 60
t_vec = np.linspace(0, t_total, int(t_total * fps))

# Prepara figuras
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Subplot 1: animação da trajetória
ax1.set_title("Trajetória")
ax1.set_xlim(-0.05, 0.3)
ax1.set_ylim(-0.05, 0.35)
ax1.set_xlabel("x (m)")
ax1.set_ylabel("y (m)")
ax1.grid(True)
point, = ax1.plot([], [], 'ro')
traj, = ax1.plot([], [], 'b--', alpha=0.3)

# Subplot 2: gráfico de ângulos das polias
ax2.set_title("Ângulos das polias (phi)")
ax2.set_xlim(0, t_total)
ax2.set_ylim(-8, 5)
ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel("Ângulo (rad)")
ax2.grid(True)
phi1_line, = ax2.plot([], [], label='phi1')
phi2_line, = ax2.plot([], [], label='phi2')
ax2.legend()

x_data, y_data = [], []
phi1_data, phi2_data, t_data = [], [], []

# Função de atualização da animação
def update(frame):
    t = t_vec[frame]
    x = x1(t)
    y = y1(t)
    ph1 = phi1(t)
    ph2 = phi2(t)

    point.set_data([x], [y])  # <-- aqui está a correção
    x_data.append(x)
    y_data.append(y)
    traj.set_data(x_data, y_data)

    phi1_data.append(ph1)
    phi2_data.append(ph2)
    t_data.append(t)
    phi1_line.set_data(t_data, phi1_data)
    phi2_line.set_data(t_data, phi2_data)

    return point, traj, phi1_line, phi2_line


ani = FuncAnimation(fig, update, frames=len(t_vec), interval=1000/fps, blit=True)
plt.tight_layout()
plt.show()
