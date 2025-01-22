from manim import *
from scipy.integrate import solve_ivp


# Lorenz system equations
def lorenz_equation(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return np.array([dxdt, dydt, dzdt])


def integrate_lorenz(function, state0, time, dt=0.001):
    solution = solve_ivp(
        function, t_span=(0, time), y0=state0, t_eval=np.arange(0, time, dt)
    )
    return solution.y.T


# Create a 3D plot
class Lorenz(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=(-30, 30, 5), y_range=(-30, 30, 5), z_range=(0, 50, 5)
        ).shift(IN * 2)
        self.add(axes)

        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)
        # add ambient camera rotation
        self.begin_ambient_camera_rotation(rate=0.2)

        evolution_time = 100

        episilon = 1e-5
        n_states = 3

        states0 = (np.array([10.0, 10.0, 10.0 + i * episilon]) for i in range(n_states))
        colors = [ManimColor("#39FF14"), ManimColor("#00FEFC"), ManimColor("#FFFF00")]

        curves = VGroup()
        dots = []

        for state0, color in zip(states0, colors):
            points = integrate_lorenz(lorenz_equation, state0, evolution_time)

            curve = VMobject()
            curve.set_points_smoothly(axes.coords_to_point(points))
            curve.set_stroke(color=color, width=2)

            curves.add(curve)

            dot = AnnotationDot(
                radius=3,
                fill_color=DARKER_GRAY,
                fill_opacity=1,
                stroke_width=1,
                stroke_color=color,
            )
            dot.add_updater(lambda m, t: m.move_to(curve.points[-1]))

        self.play(
            *(Create(curve) for curve in curves),
            run_time=evolution_time,
            run_func=linear
        )
