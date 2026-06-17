import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import time
import seaborn as sns

# Configure page to be wider and have a nice title
st.set_page_config(page_title="Physics A1 - Trajectory", page_icon="🚀", layout="wide")

# Custom CSS to style some Streamlit components further
st.markdown("""
<style>
    /* Style latex blocks */
    .katex {
        color: #f1e4f3 !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom sidebar navigation
st.sidebar.title("🧭 Navigation Menu")
page = st.sidebar.radio(
    "Select Page:",
    ["📝 Detailed Math Derivation", "🎨 Trajectory Visualization"]
)

st.sidebar.divider()

# Shared parameters in the sidebar
st.sidebar.header("⚙️ Input Parameters")
st.sidebar.markdown("Adjust the values below to see dynamic changes.")
x0_val = st.sidebar.slider("$x_0$ (Amplitude along x-axis)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
y0_val = st.sidebar.slider("$y_0$ (Amplitude along y-axis)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
phi_deg = st.sidebar.slider("$\\varphi$ (Phase difference in degrees)", min_value=0, max_value=360, value=90, step=15)
phi_rad = np.radians(phi_deg)


# Page 1: Math Solver
if page == "📝 Detailed Math Derivation":
    st.title("📝 Detailed Mathematical Derivation")
    st.markdown("""
    **Problem Statement:** The position of a particle moving in the Oxy plane is determined by the radius vector:
    $$\\vec{r} = x_0 \\cos(5t)\\vec{i} + y_0 \\cos(5t + \\varphi)\\vec{j}$$.
    Find the trajectory equation of the particle.
    """)
    st.divider()

    st.subheader("1. Equations of Motion (Parametric Representation)")
    st.markdown("From the radius vector $\\vec{r}(t)$, we obtain the coordinate equations of the particle over time $t$:")
    st.latex(r"\begin{cases} x(t) = x_0 \cos(5t) \quad (1) \\ y(t) = y_0 \cos(5t + \varphi) \quad (2) \end{cases}")

    st.subheader("2. Eliminating the Time Parameter $t$")
    st.markdown("To find the trajectory equation in the form $f(x, y) = 0$, we eliminate the variable $t$ from the system of equations:")

    st.markdown("From equation (1), we have:")
    st.latex(r"\cos(5t) = \frac{x}{x_0}")

    st.markdown("Applying the cosine addition formula to equation (2):")
    st.latex(r"\cos(5t + \varphi) = \cos(5t)\cos(\varphi) - \sin(5t)\sin(\varphi)")
    st.markdown("Substituting this into (2) gives:")
    st.latex(r"\frac{y}{y_0} = \cos(5t)\cos(\varphi) - \sin(5t)\sin(\varphi)")
    st.latex(r"\implies \sin(5t)\sin(\varphi) = \frac{x}{x_0}\cos(\varphi) - \frac{y}{y_0}")

    st.markdown("Squaring both sides:")
    st.latex(r"\sin^2(5t)\sin^2(\varphi) = \left( \frac{x}{x_0}\cos(\varphi) - \frac{y}{y_0} \right)^2")

    st.markdown("Using the identity $\\sin^2(5t) = 1 - \\cos^2(5t) = 1 - \\frac{x^2}{x_0^2}$:")
    st.latex(r"\left(1 - \frac{x^2}{x_0^2}\right)\sin^2(\varphi) = \frac{x^2}{x_0^2}\cos^2(\varphi) - \frac{2xy}{x_0 y_0}\cos(\varphi) + \frac{y^2}{y_0^2}")

    st.markdown("Expanding and grouping the terms:")
    st.latex(r"\sin^2(\varphi) - \frac{x^2}{x_0^2}\sin^2(\varphi) = \frac{x^2}{x_0^2}\cos^2(\varphi) - \frac{2xy}{x_0 y_0}\cos(\varphi) + \frac{y^2}{y_0^2}")
    st.latex(r"\implies \frac{x^2}{x_0^2}\left(\sin^2(\varphi) + \cos^2(\varphi)\right) + \frac{y^2}{y_0^2} - \frac{2xy}{x_0 y_0}\cos(\varphi) = \sin^2(\varphi)")

    st.markdown(r"Since $\sin^2(\varphi) + \cos^2(\varphi) = 1$, we obtain the general trajectory equation of the particle:")
    st.latex(r"\frac{x^2}{x_0^2} + \frac{y^2}{y_0^2} - \frac{2xy}{x_0 y_0}\cos(\varphi) = \sin^2(\varphi)")

    st.divider()
    st.subheader("✏️ 3. Specific Solution for Current Parameters")
    st.markdown(f"Substituting the active parameters: $x_0 = {x0_val}$, $y_0 = {y0_val}$, $\\varphi = {phi_deg}^\\circ$:")

    # Symbolic computation for output
    x_sym, y_sym = sp.symbols('x y', real=True)
    expr = x_sym**2 / x0_val**2 + y_sym**2 / y0_val**2 - 2*x_sym*y_sym / (x0_val * y0_val) * np.cos(phi_rad)
    val = np.sin(phi_rad)**2
    nice_expr = sp.nsimplify(expr, tolerance=1e-10, rational=True)

    st.markdown("**Specific Trajectory Equation:**")
    st.latex(f"{sp.latex(nice_expr)} = {val:.4g}")

# Page 2: Visualization
else:
    st.title("🎨 Trajectory Visualization")
    st.markdown("This page visualizes the motion of the particle along its trajectory, along with physical vectors (Velocity & Acceleration) at different points in time.")
    st.divider()

    # Time controller setup
    col_ctrl1, col_ctrl2 = st.columns([1, 2])
    with col_ctrl1:
        st.write("### 🎮 Time Controller")
        t_val = st.slider("Time $t$ (seconds)", min_value=0.0, max_value=2*np.pi/5, value=0.0, step=0.01, format="%.3f s")
        run_animation = st.button("▶️ Run Simulation (Animation)")
        
        # Legend explanation
        st.markdown("""
        **Graph Legend Guide:**
        *   ⚪ **Particle**: Current position of the particle at time $t$.
        *   🌸 **Start Point**: Position of the particle at $t=0$.
        *   🔵 **Velocity Vector $\\vec{v}$**: Points in the direction of motion, magnitude scaled 1:5 for visualization.
        *   🌸 **Acceleration Vector $\\vec{a}$**: Points towards the center of motion, magnitude scaled 1:25 for visualization.
        """)
        
    with col_ctrl2:
        st.write("### 📈 Real-Time Trajectory Plot")
        plot_placeholder = st.empty()

        def draw_plot(current_t):
            # General trajectory path data
            time_array = np.linspace(0, 2*np.pi/5, 500)
            x_path = x0_val * np.cos(5 * time_array)
            y_path = y0_val * np.cos(5 * time_array + phi_rad)

            # Current position
            cx = x0_val * np.cos(5 * current_t)
            cy = y0_val * np.cos(5 * current_t + phi_rad)

            # Velocity components (v_x = -5*x_0*sin(5t), v_y = -5*y_0*sin(5t+phi))
            vx = -5 * x0_val * np.sin(5 * current_t)
            vy = -5 * y0_val * np.sin(5 * current_t + phi_rad)

            # Acceleration components (a_x = -25*x_0*cos(5t), a_y = -25*y_0*cos(5t+phi))
            ax_val = -25 * x0_val * np.cos(5 * current_t)
            ay_val = -25 * y0_val * np.cos(5 * current_t + phi_rad)

            # Set seaborn theme for aesthetic styling
            sns.set_theme(style="dark", rc={
                "axes.facecolor": "#0c122c",
                "figure.facecolor": "#0c122c",
                "grid.color": "#172554",
                "text.color": "#e0dbec",
                "axes.labelcolor": "#e0dbec",
                "xtick.color": "#e0dbec",
                "ytick.color": "#e0dbec"
            })

            # Create figure with a solid background color to take it out from the main background
            fig, ax = plt.subplots(figsize=(6.5, 6.5), facecolor='#0c122c')
            ax.set_facecolor('#0c122c')

            # 1. Plot the static trajectory using Seaborn (estimator=None to prevent aggregation artifact)
            sns.lineplot(x=x_path, y=y_path, color='#8b5cf6', linewidth=3, alpha=0.9, label='Trajectory', ax=ax, sort=False, estimator=None)

            # 2. Plot starting point using Seaborn
            sns.scatterplot(x=[x_path[0]], y=[y_path[0]], color='#fbcfe8', s=100, label='Start (t=0)', ax=ax, zorder=5)

            # 3. Plot current position using Seaborn
            sns.scatterplot(x=[cx], y=[cy], color='#ffffff', edgecolor='#a78bfa', s=150, label='Particle', ax=ax, zorder=6)

            # 4. Plot physical vectors using quiver (scaled for aesthetic rendering)
            # Scaling: velocity / 5 (Bright Blue), acceleration / 25 (Soft Pink)
            ax.quiver(cx, cy, vx/5, vy/5, color='#3b82f6', angles='xy', scale_units='xy', scale=1, 
                      width=0.007, headwidth=4, headlength=4, label='Velocity (x0.2)')
            ax.quiver(cx, cy, ax_val/25, ay_val/25, color='#fbcfe8', angles='xy', scale_units='xy', scale=1, 
                      width=0.007, headwidth=4, headlength=4, label='Acceleration (x0.04)')

            # Symmetrical limits to avoid stretching
            max_val = max(x0_val, y0_val) * 1.3
            ax.set_xlim(-max_val, max_val)
            ax.set_ylim(-max_val, max_val)

            # Move left and bottom spines to origin and style them to pop out
            ax.spines['left'].set_position('zero')
            ax.spines['left'].set_color('#3b82f6')
            ax.spines['left'].set_linewidth(1.5)
            
            ax.spines['bottom'].set_position('zero')
            ax.spines['bottom'].set_color('#3b82f6')
            ax.spines['bottom'].set_linewidth(1.5)
            
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')

            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            
            # Style tick labels and grid
            ax.tick_params(colors='#e0dbec', which='both', labelsize=8)
            ax.grid(color='#172554', linestyle='--', linewidth=0.5, alpha=0.5)
            ax.set_aspect('equal', adjustable='box')

            # Style axis labels
            ax.set_xlabel('x-axis', fontsize=9, loc='right', color='#e0dbec')
            ax.set_ylabel('y-axis', fontsize=9, loc='top', color='#e0dbec')

            # Place legend inside, made smaller and transparent
            ax.legend(loc='upper right', framealpha=0.3, facecolor='#ffffff', edgecolor='#172554', fontsize=6.5)

            return fig

        # If animation is running
        if run_animation:
            steps = 80
            for current_t in np.linspace(0, 2*np.pi/5, steps):
                fig = draw_plot(current_t)
                plot_placeholder.pyplot(fig)
                plt.close(fig) # prevent memory accumulation
                time.sleep(0.04) # smooth frame rate
        else:
            # Static drawing based on the slider value
            fig = draw_plot(t_val)
            plot_placeholder.pyplot(fig)
            plt.close(fig)
