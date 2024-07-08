import numpy as np
import matplotlib.pyplot as plt

# Define the region of absolute stability for Heun method
def heun_stability_region(z):
    return np.abs(1 + z + 0.5 * z**2)

# Generate grid of complex numbers
x = np.linspace(-4, 4, 400)
y = np.linspace(-4, 4, 400)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# Compute stability values for Heun method
heun_stability_values = heun_stability_region(Z)

# Plot the region of absolute stability for Heun method
plt.figure(figsize=(8, 6))
plt.contourf(X, Y, heun_stability_values, levels=[0, 1], cmap='Blues')
plt.title('Region of Absolute Stability: Heun Method')
plt.xlabel('Re(z)')
plt.ylabel('Im(z)')
plt.colorbar(label='Stability')
plt.grid(True)
plt.show()
