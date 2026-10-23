Create setup_check.py. Import NumPy, Matplotlib and OpenCV (cv2), and print their versions. Use NumPy
to create x = 0, 1, 2, 3, 4 and plot y = x squared. Label the axes, save setup_check.png and display the
plot. Also create requirements.txt listing numpy, matplotlib and opencv-python. Use the selected Python
interpreter; do not install packages or change unrelated files.

add point markers

delete the png and in the same document create a video of a square that has a dot inside in a random site and moves in right lines. when it encounters a walls it bounces and continue moving

now create a random animateed video of whatever you want. 10 seconds. the video has to be a sismple story thats shows any plot (you have complete freedom)

lets make that better looking, the classroom seen from the upper part sealing. use more natural colors lite browns and oranges. be creative enough to make the video self explanatory without using text or captions

lets make that better looking, the classroom seen from the upper part sealing. use more natural colors lite browns and oranges. be creative enough to make the video self explanatory without using text or captions

now make the same video but in 3d

Act as a Senior Scientific Visualization Developer in Python.

Create a standalone, publication-quality Python script using Matplotlib and NumPy to plot the temporal velocity profile v_z(t) of a sphere falling in a viscous fluid under Stokes' drag regime.
----------
### 1. Physics & Mathematical Formulation:
- Formula: v_z(t) = v_tz * (1 - exp(-t / tau))
- Terminal Velocity Component: v_tz = - (2 * R^2 * g * (rho_obj - rho_fluid)) / (9 * mu)
- Time Constant: tau = (2 * R^2 * rho_obj) / (9 * mu)
- Realistic Parameters (Glass sphere in Glycerol):
  * Radius: R = 1.0e-3  # meters (1 mm)
  * Object Density: rho_obj = 2500.0  # kg/m^3
  * Fluid Density: rho_fluid = 1260.0  # kg/m^3
  * Dynamic Viscosity: mu = 0.95  # Pa·s
  * Gravity: g = 9.81  # m/s^2

### 2. Time Domain & Data Points:
- Define time array t from 0 to 6 * tau with 500 resolution points.

### 3. Styling & Visual Enhancements:
- Use 'seaborn-v0_8-whitegrid' theme with 300 DPI and figure size (8, 5).
- Plot the main curve v_z(t) using a bold crimson/navy line (linewidth=2.5).
- Draw a horizontal dashed line representing the asymptote at v_z = v_tz.
- Add markers with dotted projection lines to both axes for:
  1. t = tau  --> v_z(tau) = 0.632 * v_tz
  2. t = 3*tau --> v_z(3*tau) = 0.950 * v_tz
  3. t = 5*tau --> v_z(5*tau) = 0.993 * v_tz
- Annotate these points with clean text labels showing the percentages reached.

### 4. LaTeX Labels & Annotations:
- Title: r"Temporal Velocity Profile $v_z(t)$ of a Falling Sphere (Stokes' Flow)"
- X-axis Label: r"Time $t$ [s]"
- Y-axis Label: r"Vertical Velocity Component $v_z(t)$ [m/s]"
- Include a small styled inset text box displaying parameter values (R, rho_obj, rho_fluid, mu, calculated tau, and calculated v_tz).

### 5. Execution:
- Apply plt.tight_layout() and ensure the figure displays properly with plt.show().



Act as an expert Python scientific developer specializing in Matplotlib visualizations for fluid mechanics homework deliverables.

Write a complete, standalone Python script to generate a purely symbolic, parametric plot of the temporal velocity profile v_z(t) = v_{t,z} * (1 - exp(-t / tau)) for Homework 5.

### CRITICAL CONSTRAINTS:
1. NO SPECIFIC MATERIAL NUMBERS (No glycerol, no hardcoded sphere dimensions, no arbitrary physical values).
2. Plot using dimensionless/normalized variables:
   - X-axis array: t_norm = t / tau from 0 to 5.
   - Y-axis array: v_norm = v_z(t) / v_{t,z} = 1 - exp(-t_norm).
3. STEREOTYPIC / SYMBOLIC AXIS LABELS:
   - X-axis custom ticks at [0, 1, 2, 3, 4, 5] labeled as [r'$0$', r'$\tau$', r'$2\tau$', r'$3\tau$', r'$4\tau$', r'$5\tau$'].
   - Y-axis custom ticks at [0, 0.632, 0.950, 1.0] labeled as [r'$0$', r'$0.632\,v_{t,z}$', r'$0.950\,v_{t,z}$', r'$v_{t,z}$'].
------
### ZERO-OVERLAP & ANTI-SUPERPOSITION LAYOUT INSTRUCTIONS:
- Ensure ZERO text collision or label superposition anywhere on the plot.
- Set plot dimensions to (8, 5) with dpi=300 and use 'seaborn-v0_8-whitegrid' theme.
- Main curve: Solid bold navy line (linewidth=2.5).
- Asymptote: Horizontal dashed line at v_norm = 1 (labeled r'Asymptote: $v_z(t) \to v_{t,z}$').
- Dotted projection lines:
  * From t/tau = 1 to v_norm = 0.632
  * From t/tau = 3 to v_norm = 0.950
- Annotations:
  * Place text annotations with distinct offsets (xytext and textcoords='offset points') and light background boxes (bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none', alpha=0.8)) to guarantee NO overlap with grid lines, axis ticks, or the main curve.

### TITLES & AXIS FORMATTING:
- Title: r"Normalized Velocity Profile $v_z(t) / v_{t,z} = 1 - e^{-t/\tau}$"
- X-axis Label: r"Time $t$ [units of $\tau$]" (labelpad=10)
- Y-axis Label: r"Velocity Component $v_z(t)$ [units of $v_{t,z}$]" (labelpad=12)
- Apply plt.tight_layout() and plt.show().