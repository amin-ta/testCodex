import matplotlib.pyplot as plt

# Original data points (larger and more varied)
# A list of 30 numbers representing some measurement
values = [
    88, 33, 55, 21, 5, 76, 67, 45, 90, 30,
    40, 60, 15, 81, 27, 37, 70, 24, 96, 52,
    63, 11, 83, 18, 92, 43, 58, 71, 68, 99,
]

# ----------- Normalization (Min-Max scaling) -----------
# Formula: x_norm = (x - x_min) / (x_max - x_min)

x_min = min(values)
x_max = max(values)

normalized = [(x - x_min) / (x_max - x_min) for x in values]

# ----------- Standardization (Z-score) -----------
# Formula: x_std = (x - mean) / std_dev

mean = sum(values) / len(values)
variance = sum((x - mean) ** 2 for x in values) / len(values)
std_dev = variance ** 0.5

standardized = [(x - mean) / std_dev for x in values]

# ----------- Visualization -----------
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.bar(range(len(values)), values)
plt.title("Original")
plt.xticks(range(len(values)))

plt.subplot(1, 3, 2)
plt.bar(range(len(values)), normalized)
plt.title("Normalized")
plt.xticks(range(len(values)))

plt.subplot(1, 3, 3)
plt.bar(range(len(values)), standardized)
plt.title("Standardized")
plt.xticks(range(len(values)))

plt.tight_layout()
plt.show()
