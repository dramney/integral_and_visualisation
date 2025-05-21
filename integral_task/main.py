import numpy as np
import json
from scipy import integrate
import os
import warnings

warnings.filterwarnings('ignore')

# параметри
l = 0.1
H = 0.05
q0 = 200
lambda_val = 67.9
alpha_val = 17.64

x_min, x_max = -0.1, 0.1
y_min, y_max = -0.1, 0.1

x_step = 0.01
y_step = 0.01


# гіперболічні функції з покращеною стабільністю
def ch(x):

    if x > 700:
        return float('inf')
    if x < -700:
        return float('inf')
    try:
        return np.cosh(x)
    except:
        return float('inf')


def sh(x):

    if x > 700:
        return float('inf')
    if x < -700:
        return -float('inf')
    try:
        return np.sinh(x)
    except:
        if x > 0:
            return float('inf')
        else:
            return -float('inf')


# параметр p з обробкою помилок
def P(z):
    try:
        tanz = np.tan(z)


        if abs(tanz) > 350:
            return float('inf')

        sh_term = sh(2 * l * tanz)
        ch_term = ch(2 * l * tanz)

        if np.isinf(sh_term) or np.isinf(ch_term):
            return float('inf')

        return lambda_val * tanz * sh_term - alpha_val * ch_term
    except:
        return float('inf')


# S
def S(y):
    if y > 0:
        return 1
    elif y == 0.0:
        return 0.5
    else:  # y < 0
        return 0


# сам інтеграл з обробкою помилок
def integrand(z, x, y):
    try:

        if abs(np.cos(z)) < 1e-10 or abs(z - np.pi / 2) < 1e-10:
            return 0.0

        tgz = np.tan(z)


        if abs(tgz) < 1e-10:
            return 0.0


        term1 = np.cos(x * tgz) / (tgz * (np.cos(z) ** 2))


        term2 = np.sin(H * tgz)


        p_value = P(z)
        if abs(p_value) < 1e-10 or np.isinf(p_value):
            return 0.0


        bracket_term1 = ch(tgz * (y + l)) / p_value


        if abs(tgz) < 1e-10:
            bracket_term2 = 0.0
        else:
            bracket_term2 = (2 * sh(tgz * (y - l))) / (lambda_val * tgz)


        s_value = S(y - l)
        bracket = bracket_term1 - (bracket_term2 * s_value)


        result = term1 * term2 * bracket


        if np.isnan(result) or np.isinf(result):
            return 0.0

        return result
    except:
        return 0.0


# обчислення всього виразу для конкретного x y
def calculate_integral(x, y):
    try:

        upper_limit = np.pi / 2 # - 1e-5


        result, _ = integrate.quad(
            lambda z: integrand(z, x, y),
            0,
            upper_limit,
            limit=100,
            epsabs=1e-6,
            epsrel=1e-6
        )
        return (q0 / np.pi) * result
    except Exception as e:
        print(f"Integration error at x={x}, y={y}: {str(e)}")
        return float('nan')


# генерує масив всіх значень x та y з певним кроком
x_values = np.arange(x_min, x_max + x_step / 2, x_step)
y_values = np.arange(y_min, y_max + y_step / 2, y_step)

# для прогресу
total_points = len(x_values) * len(y_values)
current_point = 0

print(f"Starting calculation of {total_points} points...")
results = {}

# обраховує всі значення
for x in x_values:
    x_key = f"x{x:.6f}"
    results[ x_key ] = {}

    for y in y_values:
        current_point += 1
        if current_point % 10 == 0:
            print(f"Progress: {current_point}/{total_points} ({current_point / total_points * 100:.1f}%)")

        try:
            integral_value = calculate_integral(x, y)

            if np.isnan(integral_value):
                results[ x_key ][ f"y{y:.6f}" ] = "NaN"
            else:
                results[ x_key ][ f"y{y:.6f}" ] = float(integral_value)
        except Exception as e:
            results[ x_key ][ f"y{y:.6f}" ] = f"Error: {str(e)}"

# зберігає в JSON
with open('integral_results.json', 'w') as f:
    json.dump(results, f, indent=4)

print(f"Calculation completed. Results saved to {os.path.abspath('integral_results.json')}")

# друкує малу кть для перевірки
sample_x = x_values[ 0 ]
sample_results = {f"x{sample_x:.6f}": {}}
for y in y_values[ :3 ]:
    try:
        integral_value = calculate_integral(sample_x, y)
        if np.isnan(integral_value):
            sample_results[ f"x{sample_x:.6f}" ][ f"y{y:.6f}" ] = "NaN"
        else:
            sample_results[ f"x{sample_x:.6f}" ][ f"y{y:.6f}" ] = float(integral_value)
    except Exception as e:
        sample_results[ f"x{sample_x:.6f}" ][ f"y{y:.6f}" ] = f"Error: {str(e)}"

print("\nSample results:")
print(json.dumps(sample_results, indent=4))