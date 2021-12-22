from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    mean_type: str = 'Тип тренировки:'
    mean_duration: str = 'Длительность:'
    mean_distance: str = 'Дистанция:'
    mean_speed: str = 'Ср. скорость:'
    mean_calories: str = 'Потрачено ккал:'

    def get_message(self) -> str:
        """Возвращает сообщение с данными."""
        return (
            f'{self.mean_type} {self.training_type}; '
            f'{self.mean_duration} {self.duration:.3f} ч.; '
            f'{self.mean_distance} {self.distance:.3f} км; '
            f'{self.mean_speed} {self.speed:.3f} км/ч; '
            f'{self.mean_calories} {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    M_IN_H: int = 60
    LEN_STEP: float = 0.65
    coeff_run_1: int = 18
    coeff_run_2: int = 20
    coeff_walk_1: float = 0.035
    coeff_walk_2: float = 0.029
    coeff_swim_1: float = 1.1
    coeff_swim_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.coeff_run_1 * self.get_mean_speed()
                - self.coeff_run_2) * self.weight / self.M_IN_KM
                * self.duration * self.M_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.coeff_walk_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.coeff_walk_2 * self.weight)
                * self.duration * self.M_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.coeff_swim_1)
                * self.coeff_swim_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    class_name = dict[workout_type]
    return class_name(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
