import numpy as np
import matplotlib.pyplot as plt

# Constantes
m = 1.0   # massa do bloco (kg)
g = 9.81  # gravidade (m/s²)
d = 0.30  # distância entre os motores (m)
h = 0.40  # altura do centro da trajetória em relação aos motores (m)
r = 0.08  # raio da trajetória circular (m)

# Posições dos motores (embaixo)
motor1 = np.array([0, 0])
motor2 = np.array([d, 0])

# Centro da trajetória circular (em cima dos motores)
center = np.array([d / 2, h])

# Trajetória circular com 100 pontos
theta = np.linspace(0, 2 * np.pi, 100)
traj = center.reshape(1, 2) + r * np.vstack([np.cos(theta), np.sin(theta)]).T

# Vetores para armazenar as tensões
T1_list = []
T2_list = []

# Cálculo das tensões para cada ponto
for p in traj:
    vec1 = p - motor1  # vetor do motor1 até o bloco
    vec2 = p - motor2  # vetor do motor2 até o bloco

    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    # Cossenos e senos dos ângulos em relação à horizontal
    cos1 = vec1[0] / norm1
    sin1 = vec1[1] / norm1
    cos2 = vec2[0] / norm2
    sin2 = vec2[1] / norm2

    # Denominador comum
    denom = sin1 * cos2 + cos1 * sin2

    if np.abs(denom) < 1e-6:
        T1 = T2 = np.nan
    else:
        T2 = (-m * g * cos1) / denom
        T1 = (m * g * cos2) / denom

    T1_list.append(T1)
    T2_list.append(T2)

# Converter theta para graus
theta_degrees = theta * 180 / np.pi

# Criar máscara para selecionar apenas os ângulos entre 100 e 250 graus
mask = (theta_degrees >= 90) & (theta_degrees <= 270)

# Plotando a trajetória e tensões
plt.figure(figsize=(12, 5))

# Trajetória do bloco
plt.subplot(1, 2, 1)
plt.plot(traj[:, 0], traj[:, 1], label='Trajetória circular')
plt.scatter([motor1[0], motor2[0]], [motor1[1], motor2[1]], color='red', label='Motores (embaixo)')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Trajetória do bloco suspenso')
plt.axis('equal')
plt.legend()

# Tensão dos cabos (apenas entre 100 e 250 graus)
plt.subplot(1, 2, 2)
plt.plot(theta_degrees[mask], np.array(T1_list)[mask], label='T1 (N)')
plt.plot(theta_degrees[mask], np.array(T2_list)[mask], label='T2 (N)')
plt.xlabel('Ângulo na trajetória (graus)')
plt.ylabel('Tensão (N)')
plt.title('Tensões nos cabos')
plt.legend()

plt.tight_layout()
plt.show()