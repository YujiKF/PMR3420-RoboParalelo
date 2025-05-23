import numpy as np
import matplotlib.pyplot as plt

# Parâmetros
xP1, yP1 = -0.2, 0
xP2, yP2 =  0.2, 0
R = 0.02  # Raio da polia (m)

# Círculo
r_circ = 0.15  # raio da trajetória circular (m)
xc, yc = 0.2, 0.2  # centro do círculo
T_circ = 6.0  # tempo total para dar uma volta

# Funções de interpolação
def x1(t):
    theta = 2*np.pi*(t/T_circ)
    return xc + r_circ * np.cos(theta)

def y1(t):
    theta = 2*np.pi*(t/T_circ)
    return yc + r_circ * np.sin(theta)

def dx1(t):
    theta = 2*np.pi*(t/T_circ)
    return -r_circ * np.sin(theta) * 2*np.pi/T_circ

def dy1(t):
    theta = 2*np.pi*(t/T_circ)
    return r_circ * np.cos(theta) * 2*np.pi/T_circ

def ddx1(t):
    theta = 2*np.pi*(t/T_circ)
    return -r_circ * np.cos(theta) * (2*np.pi/T_circ)**2

def ddy1(t):
    theta = 2*np.pi*(t/T_circ)
    return -r_circ * np.sin(theta) * (2*np.pi/T_circ)**2

# Cabos
def L1(t): return np.sqrt((x1(t) - xP1)**2 + (y1(t) - yP1)**2)
def L2(t): return np.sqrt((xP2 - x1(t))**2 + (yP2 - y1(t))**2)

def dL1(t):
    num = (x1(t) - xP1)*dx1(t) + (y1(t) - yP1)*dy1(t)
    return num / L1(t)

def dL2(t):
    num = (xP2 - x1(t))*(-dx1(t)) + (yP2 - y1(t))*(-dy1(t))
    return num / L2(t)

def ddL1(t):
    num1 = dx1(t)**2 + (x1(t) - xP1)*ddx1(t) + dy1(t)**2 + (y1(t) - yP1)*ddy1(t)
    num2 = ((x1(t) - xP1)*dx1(t) + (y1(t) - yP1)*dy1(t))**2 / L1(t)**2
    return (num1 - num2) / L1(t)

def ddL2(t):
    num1 = dx1(t)**2 + (xP2 - x1(t))*(-ddx1(t)) + dy1(t)**2 + (yP2 - y1(t))*(-ddy1(t))
    num2 = ((xP2 - x1(t))*(-dx1(t)) + (yP2 - y1(t))*(-dy1(t)))**2 / L2(t)**2
    return (num1 - num2) / L2(t)

# Polias
L10 = L1(0)
L20 = L2(0)

def phi1(t): return (L10 - L1(t)) / R
def phi2(t): return (L20 - L2(t)) / R

def dphi1(t): return -dL1(t) / R
def dphi2(t): return -dL2(t) / R

def ddphi1(t): return -ddL1(t) / R
def ddphi2(t): return -ddL2(t) / R

# Simulação
t_vec = np.linspace(0, T_circ, 600)
x_vec = np.array([x1(t) for t in t_vec])
y_vec = np.array([y1(t) for t in t_vec])
dx_vec = np.array([dx1(t) for t in t_vec])
dy_vec = np.array([dy1(t) for t in t_vec])
ddx_vec = np.array([ddx1(t) for t in t_vec])
ddy_vec = np.array([ddy1(t) for t in t_vec])

phi1_vec = np.array([phi1(t) for t in t_vec])
phi2_vec = np.array([phi2(t) for t in t_vec])
dphi1_vec = np.array([dphi1(t) for t in t_vec])
dphi2_vec = np.array([dphi2(t) for t in t_vec])
ddphi1_vec = np.array([ddphi1(t) for t in t_vec])
ddphi2_vec = np.array([ddphi2(t) for t in t_vec])

# Plotagem
plt.figure(figsize=(16,10))

# Trajetória
plt.subplot(2,3,1)
plt.plot(x_vec, y_vec)
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Trajetória circular')
plt.axis('equal')
plt.grid()

# Velocidade do ponto
plt.subplot(2,3,2)
plt.plot(t_vec, dx_vec, label='dx/dt')
plt.plot(t_vec, dy_vec, label='dy/dt')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.title('Velocidade do ponto')
plt.legend()
plt.grid()

# Aceleração do ponto
plt.subplot(2,3,3)
plt.plot(t_vec, ddx_vec, label='d²x/dt²')
plt.plot(t_vec, ddy_vec, label='d²y/dt²')
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (m/s²)')
plt.title('Aceleração do ponto')
plt.legend()
plt.grid()

# Ângulo das polias
plt.subplot(2,3,4)
plt.plot(t_vec, phi1_vec, label='phi1')
plt.plot(t_vec, phi2_vec, label='phi2')
plt.xlabel('Tempo (s)')
plt.ylabel('Ângulo (rad)')
plt.title('Ângulo das polias')
plt.legend()
plt.grid()

# Velocidade angular das polias
plt.subplot(2,3,5)
plt.plot(t_vec, dphi1_vec, label='dphi1/dt')
plt.plot(t_vec, dphi2_vec, label='dphi2/dt')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade angular (rad/s)')
plt.title('Velocidade angular')
plt.legend()
plt.grid()

# Aceleração angular das polias
plt.subplot(2,3,6)
plt.plot(t_vec, ddphi1_vec, label='d²phi1/dt²')
plt.plot(t_vec, ddphi2_vec, label='d²phi2/dt²')
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração angular (rad/s²)')
plt.title('Aceleração angular')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
