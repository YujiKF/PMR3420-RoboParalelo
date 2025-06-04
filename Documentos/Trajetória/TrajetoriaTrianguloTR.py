import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Polias fixas
xP1, yP1 = -0.2, 0
xP2, yP2 =  0.2, 0
R = 0.02  # raio da polia

# Pontos do triângulo equilátero de lado 150mm (0.15m)
A = np.array([0.0, 0.0])
B = np.array([0.15, 0.0])
h = np.sqrt(3)/2 * 0.15
C = np.array([0.075, h])
pontos = [A, B, C, A]  # fecha o triângulo

# Tempo total e resolução
T = 6.0  # total de 6s para contornar o triângulo
dt = 0.01
t_vec = np.arange(0, T, dt)

# Interpolação linear de trajetória
traj_x = []
traj_y = []
segment_time = T / 3

for i in range(3):
    p0 = pontos[i]
    p1 = pontos[i+1]
    for t in np.linspace(0, 1, int(segment_time/dt)):
        traj_x.append((1 - t) * p0[0] + t * p1[0])
        traj_y.append((1 - t) * p0[1] + t * p1[1])

traj_x = np.array(traj_x)
traj_y = np.array(traj_y)

# Comprimentos dos cabos e ângulos
def L1(x, y): return np.sqrt((x - xP1)**2 + (y - yP1)**2)
def L2(x, y): return np.sqrt((xP2 - x)**2 + (yP2 - y)**2)

L10 = L1(traj_x[0], traj_y[0])
L20 = L2(traj_x[0], traj_y[0])

phi1 = (L10 - np.array([L1(x, y) for x, y in zip(traj_x, traj_y)])) / R
phi2 = (L20 - np.array([L2(x, y) for x, y in zip(traj_x, traj_y)])) / R

# Criação da animação
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

# Trajetória
ax1.plot(traj_x, traj_y, 'k--', label="trajetória alvo")
point, = ax1.plot([], [], 'ro', label="posição atual")
ax1.set_xlim(-0.05, 0.25)
ax1.set_ylim(-0.05, 0.2)
ax1.set_xlabel("x (m)")
ax1.set_ylabel("y (m)")
ax1.set_title("Trajetória do ponto")
ax1.legend()
ax1.grid()

# Ângulos das polias
line1, = ax2.plot([], [], label="phi1 (rad)")
line2, = ax2.plot([], [], label="phi2 (rad)")
ax2.set_xlim(0, T)
ax2.set_ylim(min(phi1.min(), phi2.min()) - 0.2, max(phi1.max(), phi2.max()) + 0.2)
ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel("Ângulo (rad)")
ax2.set_title("Variação dos ângulos das polias")
ax2.legend()
ax2.grid()

# Dados em tempo real
time_vals = []
phi1_vals = []
phi2_vals = []

def update(i):
    t = i * dt
    x = traj_x[i]
    y = traj_y[i]
    point.set_data([x], [y])
    
    time_vals.append(t)
    phi1_vals.append(phi1[i])
    phi2_vals.append(phi2[i])
    
    line1.set_data(time_vals, phi1_vals)
    line2.set_data(time_vals, phi2_vals)
    
    return point, line1, line2

ani = animation.FuncAnimation(fig, update, frames=len(traj_x), interval=dt*1000, blit=True)
plt.tight_layout()
plt.show()
