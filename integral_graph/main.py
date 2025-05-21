import json
import numpy as np
import matplotlib.pyplot as plt

# Завантаження даних з JSON файлу
try:
    with open('integral_results.json', 'r') as f:
        results = json.load(f)
except FileNotFoundError:
    print("Файл integral_results.json не знайдено. Спочатку запустіть основний скрипт для обчислення інтеграла.")
    exit()

# Створюємо фігуру з двома графіками
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Графік 1: Крива для фіксованого y (найближчого до 0)
y_target = 5
closest_y_key = None
min_diff = float('inf')

# Знаходимо найближчий y до 0
for x_key in results.keys():
    for y_key in results[ x_key ].keys():
        y = float(y_key[ 1: ])
        diff = abs(y - y_target)
        if diff < min_diff:
            min_diff = diff
            closest_y_key = y_key

# Отримуємо дані для кривої з фіксованим y
x_values = [ ]
values_at_fixed_y = [ ]

for x_key in results.keys():
    x = float(x_key[ 1: ])
    if closest_y_key in results[ x_key ]:
        value = results[ x_key ][ closest_y_key ]
        if isinstance(value, (int, float)) and not np.isnan(value):
            x_values.append(x)
            values_at_fixed_y.append(value)

# Сортуємо точки для кривої з фіксованим y
points_y = sorted(zip(x_values, values_at_fixed_y))
x_values, values_at_fixed_y = zip(*points_y) if points_y else ([ ], [ ])

# Графік 2: Крива для фіксованого x = 0.05
x_target = 5
closest_x_key = None
min_diff_x = float('inf')

# Знаходимо найближчий x до 0.05
for x_key in results.keys():
    x = float(x_key[ 1: ])
    diff = abs(x - x_target)
    if diff < min_diff_x:
        min_diff_x = diff
        closest_x_key = x_key

# Отримуємо дані для кривої з фіксованим x
y_values = [ ]
values_at_fixed_x = [ ]

if closest_x_key in results:
    for y_key in results[ closest_x_key ].keys():
        y = float(y_key[ 1: ])
        value = results[ closest_x_key ][ y_key ]
        if isinstance(value, (int, float)) and not np.isnan(value):
            y_values.append(y)
            values_at_fixed_x.append(value)

# Сортуємо точки для кривої з фіксованим x
points_x = sorted(zip(y_values, values_at_fixed_x))
y_values, values_at_fixed_x = zip(*points_x) if points_x else ([ ], [ ])

# Малюємо перший графік (фіксоване y)
if x_values and values_at_fixed_y:
    ax1.plot(x_values, values_at_fixed_y, 'b-', linewidth=2)
    ax1.scatter(x_values, values_at_fixed_y, color='red', s=30)
    ax1.grid(True)
    ax1.set_xlabel('X координата')
    ax1.set_ylabel('Значення інтеграла')
    ax1.set_title(f'Крива інтеграла при y≈{float(closest_y_key[ 1: ]):.6f}')
else:
    ax1.text(0.5, 0.5, 'Немає даних для відображення', ha='center', va='center')
    ax1.set_title('Крива інтеграла при фіксованому y')

# Малюємо другий графік (фіксоване x)
if y_values and values_at_fixed_x:
    ax2.plot(y_values, values_at_fixed_x, 'g-', linewidth=2)
    ax2.scatter(y_values, values_at_fixed_x, color='purple', s=30)
    ax2.grid(True)
    ax2.set_xlabel('Y координата')
    ax2.set_ylabel('Значення інтеграла')
    ax2.set_title(f'Крива інтеграла при x≈{float(closest_x_key[ 1: ]):.6f}')
else:
    ax2.text(0.5, 0.5, 'Немає даних для відображення', ha='center', va='center')
    ax2.set_title('Крива інтеграла при фіксованому x')

plt.tight_layout()
plt.savefig('integral_curves.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"Графіки кривих інтеграла збережено у файлі 'integral_curves.png'")