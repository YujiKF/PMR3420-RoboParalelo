import numpy as np
import matplotlib.pyplot as plt

def gerar_trajetoria_circular(xc, yc, r, n_pontos):
    theta = np.linspace(0, 2*np.pi, n_pontos, endpoint=False)
    return [(xc + r * np.cos(t), yc + r * np.sin(t)) for t in theta]

def gerar_trajetoria_triangulo_equilatero(xc, yc, lado, n_pontos):
    # Altura do triângulo equilátero
    h = np.sqrt(3) / 2 * lado

    # Coordenadas dos vértices com o triângulo centrado em (xc, yc)
    A = (xc, yc + 2/3 * h)
    B = (xc - lado / 2, yc - 1/3 * h)
    C = (xc + lado / 2, yc - 1/3 * h)

    # Dividir os pontos igualmente entre os lados
    pontos_lado = n_pontos // 3
    resto = n_pontos % 3  # Se não for divisível por 3

    def interpolar(p1, p2, n):
        return [(p1[0] + (p2[0] - p1[0]) * i / n, p1[1] + (p2[1] - p1[1]) * i / n) for i in range(n)]

    # Gerar pontos ao longo dos lados
    pontos = (
        interpolar(A, B, pontos_lado) +
        interpolar(B, C, pontos_lado) +
        interpolar(C, A, pontos_lado + resto)
    )

    return pontos

# Parâmetros
xc, yc = 15, 20  # centro
r = 4            # raio do círculo em cm
lado = 15        # lado do triângulo em cm
n_pontos = 50

# Trajetórias
traj_circulo = gerar_trajetoria_circular(xc, yc, r, n_pontos)
traj_triangulo = gerar_trajetoria_triangulo_equilatero(xc, yc, lado, n_pontos)

# Gráfico da trajetória circular
plt.figure(figsize=(6, 8))
x_circ, y_circ = zip(*traj_circulo)
plt.plot(x_circ, y_circ, 'o-', label='Trajetória circular')
plt.plot(xc, yc, 'r+', label='Centro', markersize=10)

# Gráfico da trajetória triangular
x_tri, y_tri = zip(*traj_triangulo)
plt.plot(x_tri, y_tri, 's--', label='Trajetória triangular')

# Plano e ajustes
plt.xlim(0, 30)
plt.ylim(0, 40)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')
plt.title('Trajetórias Circular e Triangular no Plano')
plt.legend()
plt.show()
