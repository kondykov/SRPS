import numpy as np  # Импортируем библиотеку numpy для работы с массивами и математическими функциями
import tkinter as gui  # Импортируем библиотеку tkinter для создания графического интерфейса
import matplotlib.pyplot as plt  # Импортируем библиотеку matplotlib для построения графиков
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Импортируем FigureCanvasTkAgg для отображения графиков в tkinter
from scipy.optimize import fsolve  # Импортируем функцию fsolve из библиотеки scipy для решения уравнений

# Функция для расчета позиции цели
def calculate_target_position(distance, targetSpeed, reactionTime, targetAngle):
    t_flight = distance / float(startSpeedEntry.get())  # Время полета снаряда
    target_x = distance - targetSpeed * (t_flight + reactionTime) * np.cos(np.radians(targetAngle))  # Координата x цели
    target_y = float(heightEntry.get()) + targetSpeed * (t_flight + reactionTime) * np.sin(np.radians(targetAngle))  # Координата y цели
    return target_x, target_y  # Возвращаем координаты цели

# Функция для расчета угла возвышения
def calculate_angle(target_x, target_y, startSpeed):
    g = 9.8  # Ускорение свободного падения
    def equation(theta):
        return target_x * np.tan(theta) - (g * target_x**2) / (2 * startSpeed**2 * np.cos(theta)**2) - target_y  # Уравнение траектории

    initial_guess = np.radians(45)  # Начальное приближение для угла
    angle_rad = fsolve(equation, initial_guess)[0]  # Решаем уравнение для нахождения угла
    return np.degrees(angle_rad)  # Возвращаем угол в градусах

# Функция для обработки данных и построения графика
def handle():
    try:
        # Получаем значения из полей ввода
        distance = float(distanceEntry.get())
        height = float(heightEntry.get())
        startSpeed = float(startSpeedEntry.get())
        windAngle = float(windAngleEntry.get())
        windSpeed = float(windSpeedEntry.get())
        airResistance = float(airResistanceEntry.get())
        projectileMass = float(projectileMassEntry.get())
        targetSpeed = float(targetSpeedEntry.get())
        reactionTime = float(reactionTimeEntry.get())
        targetAngle = float(targetAngleEntry.get())

        # Рассчитываем позицию цели и угол возвышения
        target_x, target_y = calculate_target_position(distance, targetSpeed, reactionTime, targetAngle)
        theta = calculate_angle(target_x, target_y, startSpeed)
        print(f"Угол возвышения: {theta:.2f} градусов")

        # Рассчитываем траекторию полета снаряда
        #TODO: Сделать просчёт траектории снаряда с учётом движения цели
        t = np.linspace(0, 2 * distance / startSpeed, 1000)
        x = startSpeed * np.cos(np.radians(theta)) * t - windSpeed * t * np.cos(np.radians(windAngle))
        y = startSpeed * np.sin(np.radians(theta)) * t - 0.5 * 9.8 * t ** 2 - airResistance * t ** 2 / (2 * projectileMass)
        target_x = distance - targetSpeed * (t + reactionTime) * np.cos(np.radians(targetAngle))
        target_y = height + targetSpeed * (t + reactionTime) * np.sin(np.radians(targetAngle))

        # Создаем график
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y, label='Траектория снаряда')
        ax.plot(target_x, target_y, label='Траектория цели', linestyle='--')
        ax.scatter([target_x[-1]], [target_y[-1]], color='r', s=100, label='Цель')
        ax.set_xlabel('Дальность, м')
        ax.set_ylabel('Высота, м')
        ax.set_title('Траектория полета снаряда с учетом движения цели')
        ax.legend()
        ax.grid()

        # Отображаем график в окне tkinter
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=13, column=0, columnspan=2, padx=10, pady=3)
    except Exception as e:
        print(f"Ошибка: {e}")

# Главная функция программы
def main():
    # Устанавливаем глобальную область видимости для переменных
    global root, startSpeedEntry, heightEntry, distanceEntry, windAngleEntry, airResistanceEntry, projectileMassEntry, reactionTimeEntry, windSpeedEntry, targetSpeedEntry, targetAngleEntry

    root = gui.Tk()  # Создаем главное окно программы
    root.title("Моделирование траектории полёта снаряда")  # Устанавливаем заголовок окна

    # Инициализируем компоненты интерфейса
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
    targetSpeedLabel = gui.Label(root, text="Скорость цели (м/с):")
    targetSpeedEntry = gui.Entry(root, textvariable=gui.StringVar(value="0"))
    targetAngleLabel = gui.Label(root, text="Угол движения цели (град.):")
    targetAngleEntry = gui.Entry(root, textvariable=gui.StringVar(value="0"))
    handleBtn = gui.Button(root, text="Рассчитать траекторию", command=handle)

    # Размещаем компоненты интерфейса в окне программы
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
    targetSpeedLabel.grid(row=8, column=0, padx=10, pady=3)
    targetSpeedEntry.grid(row=8, column=1, padx=10, pady=3)
    targetAngleLabel.grid(row=9, column=0, padx=10, pady=3)
    targetAngleEntry.grid(row=9, column=1, padx=10, pady=3)
    handleBtn.grid(row=10, column=0, columnspan=2, padx=10, pady=3)

    # Создаем пустой график
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlabel('Дальность, м')
    ax.set_ylabel('Высота, м')
    ax.set_title('Траектория полета снаряда с учетом движения цели')
    ax.legend()
    ax.grid()

    root.mainloop()  # Запускаем главный цикл программы

# Точка входа в программу
if __name__ == "__main__":
    main()  # Вызываем главную функцию
