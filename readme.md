# Расчёт угла возвышения орудия с заданными параметрами
## Установка зависимостей

```commandline
pip install -r requirements.txt
```
---
## Подробное описание кода

```python
import numpy as np
import tkinter as gui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import fsolve
```
**Импортируем необходимые библиотеки:**
- `numpy` (сокращенно `np`) для работы с массивами и математическими функциями.
- `tkinter` (сокращенно `gui`) для создания графического интерфейса пользователя (GUI).
- `matplotlib.pyplot` (сокращенно `plt`) для построения графиков.
- `FigureCanvasTkAgg` для интеграции графиков `matplotlib` в интерфейс `tkinter`.
- `fsolve` из `scipy.optimize` для численного решения уравнений.

```python
def calculate_angle(distance, height, startSpeed):
    g = 9.8  # ускорение свободного падения
```
**Функция `calculate_angle` вычисляет угол возвышения:**
- `distance` - расстояние до цели.
- `height` - высота цели.
- `startSpeed` - начальная скорость снаряда.
- `g` - ускорение свободного падения (9.8 м/с²).

```python
    def equation(theta):
        return distance * np.tan(theta) - (g * distance**2) / (2 * startSpeed**2 * np.cos(theta)**2) - height
```
**Вложенная функция `equation` описывает уравнение движения снаряда:**
- Использует тригонометрические функции для расчета траектории.

```python
    initial_guess = np.radians(45)  # начальное приближение
    angle_rad = fsolve(equation, initial_guess)[0]
    return np.degrees(angle_rad)
```
**Решаем уравнение для нахождения угла:**
- `initial_guess` - начальное приближение для угла (45 градусов).
- `fsolve` решает уравнение и возвращает угол в радианах.
- Преобразуем угол из радиан в градусы и возвращаем его.

```python
def handle():
    try:
        distance = float(distanceEntry.get())
        height = float(heightEntry.get())
        startSpeed = float(startSpeedEntry.get())
        windAngle = float(windAngleEntry.get())
        windSpeed = float(windSpeedEntry.get())
        airResistance = float(airResistanceEntry.get())
        projectileMass = float(projectileMassEntry.get())
        targetSpeed = 0
        reactionTime = 0
        targetAngle = 0
```
**Функция `handle` обрабатывает ввод пользователя и вычисляет траекторию:**
- Получаем значения из полей ввода и преобразуем их в числа.

```python
        theta = calculate_angle(distance, height, startSpeed)
        print(f"Угол возвышения: {theta:.2f} градусов")
```
**Вычисляем угол возвышения с помощью функции `calculate_angle` и выводим его:**

```python
        t = np.linspace(0, 2 * distance / startSpeed, 1000)
        x = startSpeed * np.cos(np.radians(theta)) * t - windSpeed * t * np.cos(np.radians(windAngle))
        y = startSpeed * np.sin(np.radians(theta)) * t - 0.5 * 9.8 * t ** 2 - airResistance * t ** 2 / (2 * projectileMass)
        target_x = distance - targetSpeed * reactionTime * np.cos(np.radians(targetAngle))
        target_y = height + targetSpeed * reactionTime * np.sin(np.radians(targetAngle))
```
**Моделируем траекторию полета снаряда:**
- `t` - массив времени.
- `x` и `y` - координаты снаряда с учетом начальной скорости, угла возвышения, ветра и сопротивления воздуха.
- `target_x` и `target_y` - координаты цели.

```python
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y)
        ax.scatter([target_x], [target_y], color='r', s=100)
        ax.set_xlabel('Дальность, м')
        ax.set_ylabel('Высота, м')
        ax.set_title('Траектория полета снаряда с учетом внешних факторов')
        ax.grid()
```
**Создаем график траектории:**
- `fig, ax` - создаем фигуру и оси для графика.
- `ax.plot` - строим график траектории.
- `ax.scatter` - отмечаем цель на графике.
- Устанавливаем подписи осей и заголовок.

```python
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=10, column=0, columnspan=2, padx=10, pady=3)
    except Exception as e:
        print(f"Ошибка: {e}")
```
**Отображаем график в интерфейсе:**
- `canvas` - создаем холст для графика.
- `canvas.draw` - рисуем график.
- `canvas.get_tk_widget().grid` - размещаем график в интерфейсе.
- Обрабатываем возможные ошибки и выводим их.

```python
def main():
    global root, startSpeedEntry, heightEntry, distanceEntry, windAngleEntry, airResistanceEntry, projectileMassEntry, reactionTimeEntry, windSpeedEntry

    root = gui.Tk()
    root.title("Моделирование траектории полёта снаряда")
```
**Функция `main` создает графический интерфейс:**
- `root` - главное окно приложения.
- Устанавливаем заголовок окна.

```python
    startSpeedLabel = gui.Label(root, text="Начальная скорость (м/c):")
    startSpeedEntry = gui.Entry(root, textvariable=gui.StringVar(value="500"))
    heightLabel = gui.Label(root, text="Высота цели (м):")
    heightEntry = gui.Entry(root, textvariable=gui.StringVar(value="50"))
    distanceLabel = gui.Label(root, text="Дистанция до цели (м):")
    distanceEntry = gui.Entry(root, textvariable=gui.StringVar(value="2000"))
    windSpeedLabel = gui.Label(root, text="Скорость ветра (м/с):")
    windSpeedEntry = gui.Entry(root, textvariable=gui.StringVar(value="5"))
    windAngleLabel = gui.Label(root, text="Угол ветра (град.):")
    windAngleEntry = gui.Entry(root, textvariable=gui.StringVar(value="30"))
    airResistanceLabel = gui.Label(root, text="Коэф. сопротивление воздуха:")
    airResistanceEntry = gui.Entry(root, textvariable=gui.StringVar(value="0.5"))
    projectileMassLabel = gui.Label(root, text="Масса снаряда (кг):")
    projectileMassEntry = gui.Entry(root, textvariable=gui.StringVar(value="10"))
    reactionTimeLabel = gui.Label(root, text="Время реакции (с):")
    reactionTimeEntry = gui.Entry(root, textvariable=gui.StringVar(value="2"))
    handleBtn = gui.Button(root, text="Рассчитать траекторию", command=handle)
```
**Создаем и размещаем элементы интерфейса:**
- Метки (`Label`) и поля ввода (`Entry`) для ввода параметров.
- Кнопка (`Button`) для запуска расчета траектории.

```python
    startSpeedLabel.grid(row=0, column=0, padx=10, pady=3)
    startSpeedEntry.grid(row=0, column=1, padx=10, pady=3)
    heightLabel.grid(row=1, column=0, padx=10, pady=3)
    heightEntry.grid(row=1, column=1, padx=10, pady=3)
    distanceLabel.grid(row=2, column=0, padx=10, pady=3)
    distanceEntry.grid(row=2, column=1, padx=10, pady=3)
    reactionTimeLabel.grid(row=3, column=0, padx=10, pady=3)
    reactionTimeEntry.grid(row=3, column=1, padx=10, pady=3)
    airResistanceLabel.grid(row=4, column=0, padx=10, pady=3)
    airResistanceEntry.grid(row=4, column=1, padx=10, pady=3)
    projectileMassLabel.grid(row=5, column=0, padx=10, pady=3)
    projectileMassEntry.grid(row=5, column=1, padx=10, pady=3)
    windAngleLabel.grid(row=6, column=0, padx=10, pady=3)
    windAngleEntry.grid(row=6, column=1, padx=10, pady=3)
    windSpeedLabel.grid(row=7, column=0, padx=10, pady=3)
    windSpeedEntry.grid(row=7, column=1, padx=10, pady=3)
    handleBtn.grid(row=8, column=0, columnspan=2, padx=10, pady=3)
```

**Размещаем элементы интерфейса в окне:**
- Используем метод `grid` для размещения элементов в сетке.

```python
    root.mainloop()
```

**Запускаем главный цикл приложения:**
- `root.mainloop()` запускает главный цикл обработки событий, который позволяет взаимодействовать с интерфейсом.
---

