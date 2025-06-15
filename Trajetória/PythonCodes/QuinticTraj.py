def trapezoidal_trajectory(q0, qf, t0, tf, N, vmax, acc_time, dec_time):
    """
    Generates a trapezoidal trajectory.

    :param q0: Initial joint configuration.
    :param qf: Final joint configuration.
    :param t0: Initial time.
    :param tf: Final time.
    :param N: Number of points in the trajectory.
    :param vmax: Maximum velocity.
    :param acc_time: Acceleration time.
    :param dec_time: Deceleration time.
    :return: Tuple of arrays containing time, joint positions, velocities, and accelerations.
    """

    # Acceleration and deceleration rates
    a = vmax / acc_time
    d = vmax / dec_time

    times = np.linspace(t0, tf, N)
    positions = np.zeros((N, len(q0)))
    velocities = np.zeros((N, len(q0)))
    accelerations = np.zeros((N, len(q0)))

    constant_time = tf - t0 - acc_time - dec_time
    if constant_time < 0:
        raise ValueError("The sum of acceleration and deceleration times is greater than the total time.")

    for i, t in enumerate(times):
        if t < t0:
            # Before start
            positions[i] = q0
            velocities[i] = 0
            accelerations[i] = 0

        elif t0 <= t < t0 + acc_time:
            # Acceleration phase
            dt = t - t0
            positions[i] = q0 + 0.5 * a * dt ** 2
            velocities[i] = a * dt
            accelerations[i] = a

        elif t0 + acc_time <= t < t0 + acc_time + constant_time:
            # Constant velocity phase
            dt = t - (t0 + acc_time)
            positions[i] = q0 + 0.5 * a * acc_time ** 2 + vmax * dt
            velocities[i] = vmax
            accelerations[i] = 0

        elif t0 + acc_time + constant_time <= t <= tf:
            # Deceleration phase
            dt = t - (t0 + acc_time + constant_time)
            positions[i] = qf - 0.5 * d * (dec_time - dt) ** 2
            velocities[i] = d * (dec_time - dt)
            accelerations[i] = -d
        else:
            # After ebd
            positions[i] = qf
            velocities[i] = 0
            accelerations[i] = 0

    return times, positions, velocities, accelerations


def cubic_trajectory(q0, qf, t0, tf, num_points):
    """
    Generates a cubic trajectory.

    :param q0: Initial joint configuration.
    :param qf: Final joint configuration.
    :param t0: Initial time.
    :param tf: Final time.
    :param num_points: Number of points in the trajectory.
    :return: Tuple of arrays containing time, joint positions, velocities, and accelerations.
    """
    A = np.array([[1, t0, t0**2, t0**3],
                  [1, tf, tf**2, tf**3],
                  [0, 1, 2*t0, 3*t0**2],
                  [0, 1, 2*tf, 3*tf**2]])

    b = np.array([q0, qf, [0]*len(q0), [0]*len(q0)])
    coeffs = np.linalg.solve(A, b)

    times = np.linspace(t0, tf, num_points)

    T = times[:, None]
    positions = coeffs[0] + coeffs[1] * T + coeffs[2] * T ** 2 + coeffs[3] * T ** 3
    velocities = coeffs[1] + 2 * coeffs[2] * T + 3 * coeffs[3] * T ** 2
    accelerations = 2 * coeffs[2] + 6 * coeffs[3] * T

    return times, positions, velocities, accelerations


def quintic_trajectory(q0, qf, t0, tf, num_points):
    """
    Generates a quintic trajectory.

    :param q0: Initial joint configuration.
    :param qf
    :param t0: Initial time.
    :param tf: Final time.
    :param num_points: Number of points in the trajectory.
    :return: Tuple of arrays containing time, joint positions, velocities, and accelerations.
    """
    A = np.array([[1, t0, t0**2, t0**3, t0**4, t0**5],
                  [1, tf, tf**2, tf**3, tf**4, tf**5],
                  [0, 1, 2*t0, 3*t0**2, 4*t0**3, 5*t0**4],
                  [0, 1, 2*tf, 3*tf**2, 4*tf**3, 5*tf**4],
                  [0, 0, 2, 6*t0, 12*t0**2, 20*t0**3],
                  [0, 0, 2, 6*tf, 12*tf**2, 20*tf**3]])
    b = np.array([q0, qf, [0]*len(q0), [0]*len(q0), [0]*len(q0), [0]*len(q0)])
    coeffs = np.linalg.solve(A, b)

    times = np.linspace(t0, tf, num_points)
    T = times[:, None]
    positions = coeffs[0] + coeffs[1] * T + coeffs[2] * T ** 2 + coeffs[3] * T ** 3 + coeffs[4] * T ** 4 + coeffs[5] * T ** 5
    velocities = coeffs[1] + 2 * coeffs[2] * T + 3 * coeffs[3] * T ** 2 + 4 * coeffs[4] * T ** 3 + 5 * coeffs[5] * T ** 4
    accelerations = 2 * coeffs[2] + 6 * coeffs[3] * T + 12 * coeffs[4] * T ** 2 + 20 * coeffs[5] * T ** 3

    return times, positions, velocities, accelerations

def generate_viapoint_trajectory(profile, q0, qf, viapoints, t0, tf, N, max_vel=None, acc_time=None, dec_time=None, plot=False):
    """
    Generate a trajectory with via-points.

    :param profile: A string indicating the type of trajectory profile to use ('cubic', 'quintic', or 'trapezoidal').
    :param q0: Initial joint configuration.
    :param qf: Final joint configuration.
    :param viapoints: List of via-points through which the trajectory must pass.
    :param t0: Initial time.
    :param tf: Final time.
    :param N: Number of points to generate for the entire trajectory.
    :param max_vel: Maximum velocity for the trapezoidal profile (required if profile is 'trapezoidal').
    :param acc_time: Acceleration time for the trapezoidal profile (required if profile is 'trapezoidal').
    :param dec_time: Deceleration time for the trapezoidal profile (required if profile is 'trapezoidal').
    :param plot: Boolean flag indicating whether to plot the trajectory profiles (default is False).

    :return: A tuple containing lists of joint positions, velocities, and accelerations.
    """

    waypoints = [q0] + viapoints + [qf]
    num_waypoints = len(waypoints)
    if num_waypoints < 2:
        raise ValueError("At least two waypoints are required for via-point trajectory.")

    if profile == 'cubic':
        # Generate trajectory between via-points using cubic polynomials
        times, positions, velocities, accelerations = [], [], [], []
        for i in range(num_waypoints - 1):
            via_points_times, via_points_positions, via_points_velocities, via_points_accelerations = cubic_trajectory(
                waypoints[i], waypoints[i + 1], t0, tf, N // (num_waypoints - 1))
            times.extend(via_points_times)
            positions.extend(via_points_positions)
            velocities.extend(via_points_velocities)
            accelerations.extend(via_points_accelerations)

    elif profile == 'quintic':
        # Generate trajectory between via-points using quintic polynomials
        times, positions, velocities, accelerations = [], [], [], []
        for i in range(num_waypoints - 1):
            via_points_times, via_points_positions, via_points_velocities, via_points_accelerations = quintic_trajectory(
                waypoints[i], waypoints[i + 1], t0, tf, N // (num_waypoints - 1))
            times.extend(via_points_times)
            positions.extend(via_points_positions)
            velocities.extend(via_points_velocities)
            accelerations.extend(via_points_accelerations)

    elif profile == 'trapezoidal':
        # Generate trajectory between via-points using trapezoidal profile
        times, positions, velocities, accelerations = [], [], [], []
        for i in range(num_waypoints - 1):
            via_points_times, via_points_positions, via_points_velocities, via_points_accelerations = trapezoidal_trajectory(
                waypoints[i], waypoints[i + 1], t0, tf, N // (num_waypoints - 1), max_vel, acc_time, dec_time)
            times.extend(via_points_times)
            positions.extend(via_points_positions)
            velocities.extend(via_points_velocities)
            accelerations.extend(via_points_accelerations)

    else:
        raise ValueError("Invalid trajectory profile")

    # if plot:
    #     # Plot trajectory profiles
    #     plot_trajectory_profiles(times, positions, velocities, accelerations)

    return times, positions, velocities, accelerations

import numpy as np

# Função auxiliar (já criada antes)
def gerar_trajetoria_circular(xc, yc, r, n_pontos):
    theta = np.linspace(0, 2*np.pi, n_pontos, endpoint=False)
    return [(xc + r * np.cos(t), yc + r * np.sin(t)) for t in theta]

# Parâmetros
xc, yc = 15, 20
r = 4
n_pontos = 100

# Gerar pontos da trajetória circular
trajetoria_circular = gerar_trajetoria_circular(xc, yc, r, n_pontos)

# Definir q0, qf e viapoints
q0 = trajetoria_circular[0]
qf = trajetoria_circular[-1]
viapoints = trajetoria_circular[1:-1]  # remove o primeiro e o último

# Chamar a função
times, positions, velocities, accelerations = generate_viapoint_trajectory(
    profile='quintic',
    q0=q0,
    qf=qf,
    viapoints=viapoints,
    t0=0,
    tf=10,
    N=500,
    plot=False  # True se quiser ver os gráficos de posição, velocidade e aceleração
)

# Opcional: plotar trajetória 2D no plano
import matplotlib.pyplot as plt

x_vals = [p[0] for p in positions]
y_vals = [p[1] for p in positions]

plt.figure(figsize=(6, 8))
plt.plot(x_vals, y_vals, label='Trajetória Quintic')
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')
plt.title('Trajetória Interpolada com Perfil Quintic')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()

import matplotlib.pyplot as plt

# Gera a trajetória
times, positions, velocities, accelerations = quintic_trajectory(
    q0=np.array(q0),
    qf=np.array(qf),
    t0=0,
    tf=10,
    num_points=500
)

positions = np.array(positions)
velocities = np.array(velocities)
accelerations = np.array(accelerations)

# Posição - Janela 1
plt.figure("Posição")
plt.plot(times, positions[:, 0], label='x')
plt.plot(times, positions[:, 1], label='y')
plt.xlabel('Tempo [s]')
plt.ylabel('Posição [m]')
plt.title('Perfil de Posição')
plt.legend()
plt.grid(True)

# Velocidade - Janela 2
plt.figure("Velocidade")
plt.plot(times, velocities[:, 0], label='vx')
plt.plot(times, velocities[:, 1], label='vy')
plt.xlabel('Tempo [s]')
plt.ylabel('Velocidade [m/s]')
plt.title('Perfil de Velocidade')
plt.legend()
plt.grid(True)

# Aceleração - Janela 3
plt.figure("Aceleração")
plt.plot(times, accelerations[:, 0], label='ax')
plt.plot(times, accelerations[:, 1], label='ay')
plt.xlabel('Tempo [s]')
plt.ylabel('Aceleração [m/s²]')
plt.title('Perfil de Aceleração')
plt.legend()
plt.grid(True)

# Mostrar todas as janelas ao mesmo tempo
plt.show()