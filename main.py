import numpy as np # для работы с массивами и математическими функциями
import matplotlib.pyplot as plt


def f(x):
    """Функция для варианта 10."""
    if abs(np.sin(x)) < 1e-8:   # проверяем короче чтобы функция не равнялась 0
        return np.nan # проверка нуля
    return (2 * np.sin(x) + 5 * np.cos(x)) / (3 * np.sin(x))

def bisection(func, a, b, tol=1e-6):
    """Метод деления пополам для нахождения корня функции."""
    if func(a) * func(b) >= 0:
        print("Не выполняется условие f(a)*f(b) < 0 для метода деления пополам.") # если на данном интервале корень не ищется пишем об этом - бесполезно так как функция априори работает но пускай будет
        return None

    while (b - a) / 2 > tol:
        c = (a + b) / 2 # находим середину интервала
        if func(c) == 0:
            return c # если значение функции в середине интервала равно нулю, т возвращаем функцию - это и будет ее корень в общем
        elif func(a) * func(c) < 0: # если знаки функции в a и c разные, корень находится в интервале [a, c]
            b = c # сужаем интервал
        else: # иначе знаки разные в [c, b]
            a = c # сужаем интервал
    return (a + b) / 2 # возвращаем приближенное значение корня

def chord(func, a, b, tol=1e-6):
    """Метод хорд для нахождения корня функции."""
    x_prev = a # начальная точка x
    x_curr = b # конечная точка x
    while abs(x_curr - x_prev) > tol: # цикл работает пока разница между текущим и предыдущим приближениями больше заданной точности(tol - уже и так все поняли)
        x_next = x_curr - func(x_curr) * (x_curr - x_prev) / (func(x_curr) - func(x_prev)) # формула метода хорд для нахождения следующего приближения
        x_prev = x_curr # обновляем предыдущее приближение
        x_curr = x_next # обновляем текущее приближение
    return x_curr # возвращаем приближенное значение корня

def newton(func, x0, tol=1e-6, max_iter=100):
    """Метод Ньютона (касательных) для нахождения корня функции."""
    x = x0 # начальное приближение корня
    for i in range(max_iter): # цикл выполняется заданное количество итераций (чек 37 строчку)
        h = 1e-8  # берем малый шаг для численного вычисления производной
        derivative = (func(x + h) - func(x)) / h # вычисляем производную численно
        if abs(derivative) < 1e-8: # избегаем деления на ноль иначе капец
            print("Производная близка к нулю. Метод Ньютона не сходится.") # о чем я и говорил, произошел микро коллапс
            return None #
        x_next = x - func(x) / derivative # формула метода Ньютона для нахождения следующего приближения
        if abs(x_next - x) < tol:
            return x_next # возвращаем приближенное значение корня
        x = x_next # обновляем приближение
    print("Метод Ньютона не сошелся за {} итераций.".format(max_iter))
    return None

# 2. создаем массив инициализирующий все наши значения и задаем им размер
a = -1 # левая
b = 2.2 # правая
step = 0.4
x_values = np.arange(a, b + step, step)
print("x_values:", x_values) # выводим массив x

# 3. создание списка значений функции для всех значений x
y_values = [f(x) for x in x_values] # применяем функцию f(x) к каждому значению x из массива x_values и сохраняем результаты в список y_values
print("y_values:", y_values) # выводим список y

# 4. визуализация графика зависимости аргументов x от значения функции - почти закончил, я заебся, илюха следующая лаба на тебе
plt.figure(figsize=(10, 6)) # создаем новое окно для графика и задаем размер (ширина, высота)
plt.plot(x_values, y_values, marker='o', linestyle='-', label='f(x) с шагом 0.4')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('График функции f(x) = (2sin(x) + 5cos(x)) / (3sin(x))')
plt.grid(True)
plt.legend()
plt.show()

# 5. определение корней функции разными методами и визуализация

a = -1 # левая граница
b = 2.2 # правая граница


x_high_res = np.arange(a, b, 0.01)
y_high_res = [f(x) for x in x_high_res]

# методы поиска корней и построение графиков
methods = {
    "Bisection": bisection,
    "Chord": chord,
    "Newton": newton
}
# словарик короче наш сверху

for method_name, method in methods.items():
    plt.figure(figsize=(12, 8))

    # график функции с шагом 0.4
    plt.plot(x_values, y_values, marker='o', linestyle='-', label='f(x) с шагом 0.4')

    # график функции с шагом 0.01
    plt.plot(x_high_res, y_high_res, linestyle='--', label='f(x) с шагом 0.01')

    # поиски корней исходя из методов
    if method_name == "Newton":
        root = method(f, 0.5)
        roots = [root] if root else []
    else: # для методов деления пополам и хорд
        roots = []
        num_intervals = 5
        sub_interval_width = (b - a) / num_intervals # вычисляем ширину каждого подинтервала
        for i in range(num_intervals): # цикл по подинтервалам
            sub_a = a + i * sub_interval_width # левая граница подинтервала
            sub_b = a + (i + 1) * sub_interval_width # правая граница подинтервала
            try: # обработка возможных исключений
                root = method(f, sub_a, sub_b) # вызываем метод, передаем функцию и границы подинтервала
                if root and a <= root <= b: # проверяем, что корень находится в заданном интервале
                    roots.append(root) # добавляем найденный корень в список
            except Exception as e:
                print(f"Ошибка в {method_name} для интервала {sub_a}-{sub_b}: {e}") # сообщение о возможных ошибках - перегружаем код как можем


    if roots:
        root_x = [root for root in roots if root is not None]
        root_y = [f(root) for root in root_x]
        plt.scatter(root_x, root_y, color='red', marker='x', s=100, label='Корни') # отображаем корни на графике в виде крестиков
        for i, root in enumerate(root_x): # Цикл для добавления подписей к корням
            plt.annotate(f'Корень: {root:.3f}', (root, root_y[i]), textcoords="offset points", xytext=(0, 10), ha='center') # координаты корня

    # оформление графика
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'Поиск корней методом {method_name}')
    plt.grid(True)
    plt.legend()
    plt.xlim(a - 0.5, b + 0.5)
    # Устанавливаем пределы по y, чтобы избежать обрезки
    y_min = min(y_high_res) # Находим минимальное значение y
    y_max = max(y_high_res) # Находим максимальное значение y
    y_range = y_max - y_min # Вычисляем диапазон значений y
    plt.ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range) # устанавливаем пределы по y, чтобы график не обрезался

    plt.show()