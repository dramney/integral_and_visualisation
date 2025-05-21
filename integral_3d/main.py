import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Завантаження даних з JSON файлу
try:
    with open('integral_results.json', 'r') as f:
        results = json.load(f)
except FileNotFoundError:
    print("Файл integral_results.json не знайдено. Спочатку запустіть основний скрипт для обчислення інтеграла.")
    exit()

# Перетворення даних з JSON у формат для візуалізації
x_values = [ ]
y_values = [ ]
z_values = [ ]

for x_key in results.keys():
    x = float(x_key[ 1: ])  # Видаляємо 'x' і конвертуємо в число

    for y_key in results[ x_key ].keys():
        y = float(y_key[ 1: ])  # Видаляємо 'y' і конвертуємо в число
        value = results[ x_key ][ y_key ]

        # Перевіряємо, чи значення є числовим
        if isinstance(value, (int, float)) and not np.isnan(value):
            x_values.append(x)
            y_values.append(y)
            z_values.append(value)

# Перевірка наявності даних
if not x_values or not y_values or not z_values:
    print("Немає дійсних даних для побудови графіка.")
    exit()

# Створення фігури
fig = plt.figure(figsize=(12, 10))

# 3D графік
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
scatter = ax1.scatter(x_values, y_values, z_values, c=z_values, cmap=cm.jet, s=10)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Значення інтеграла')
ax1.set_title('3D візуалізація результатів інтеграла')
fig.colorbar(scatter, ax=ax1, pad=0.1, label='Значення')

# Теплова карта
ax2 = fig.add_subplot(2, 2, 2)
# Створюємо сітку для теплової карти
x_unique = sorted(list(set(x_values)))
y_unique = sorted(list(set(y_values)))
X, Y = np.meshgrid(x_unique, y_unique)
Z = np.zeros(X.shape)

# Заповнюємо сітку даними
for i, x in enumerate(x_unique):
    for j, y in enumerate(y_unique):
        # Знаходимо відповідне значення z
        for idx, (x_val, y_val, z_val) in enumerate(zip(x_values, y_values, z_values)):
            if abs(x_val - x) < 1e-6 and abs(y_val - y) < 1e-6:
                Z[ j, i ] = z_val
                break

heatmap = ax2.pcolormesh(X, Y, Z, cmap='jet', shading='auto')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_title('Теплова карта результатів інтеграла')
fig.colorbar(heatmap, ax=ax2, pad=0.1, label='Значення')

# Контурний графік
ax3 = fig.add_subplot(2, 2, 3)
contour = ax3.contourf(X, Y, Z, 20, cmap='jet')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_title('Контурний графік результатів інтеграла')
fig.colorbar(contour, ax=ax3, pad=0.1, label='Значення')

# Поверхневий графік (x, y)
ax4 = fig.add_subplot(2, 2, 4, projection='3d')
surf = ax4.plot_surface(X, Y, Z, cmap='jet', edgecolor='none', alpha=0.8)
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.set_zlabel('Значення інтеграла')
ax4.set_title('Поверхневий графік результатів інтеграла')
fig.colorbar(surf, ax=ax4, pad=0.1, shrink=0.5, label='Значення')

# Налаштування макету
plt.tight_layout()
plt.savefig('integral_visualization.png', dpi=300, bbox_inches='tight')
plt.show()

print("Візуалізація збережена у файлі 'integral_visualization.png'")