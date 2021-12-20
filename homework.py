class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories) -> None:
        self.training_type=training_type
        self.duration=duration
        self.distance=distance
        self.speed=speed
        self.calories=calories
    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int=1000
    M_IN_H: int=60
    LEN_STEP: float=0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action=action
        self.duration=duration
        self.weight=weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action*Training.LEN_STEP/Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance()/self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    coeff1_run: int=18
    coeff2_run: int=20

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (Running.coeff1_run*self.get_mean_speed()
                -Running.coeff2_run)*self.weight/Training.M_IN_KM*self.duration*Training.M_IN_H

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return super().show_training_info()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff1_walk: float=0.035
    coeff2_walk: float=0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
            super().__init__(action, duration, weight)
            self.height=height

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (SportsWalking.coeff1_walk*self.weight+(self.get_mean_speed()**2//self.height)
                *SportsWalking.coeff2_walk*self.weight)*self.duration*Training.M_IN_H

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return super().show_training_info()


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float=1.38
    coeff1_swim: float=1.1
    coeff2_swim: int=2

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool=length_pool
        self.count_pool=count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action*Swimming.LEN_STEP/Training.M_IN_KM 

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool*self.count_pool/Training.M_IN_KM/self.duration)

    def get_spent_calories(self) -> float:  
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed()+Swimming.coeff1_swim)*Swimming.coeff2_swim*self.weight

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return super().show_training_info()


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict={'SWM':Swimming, 'RUN':Running, 'WLK':SportsWalking}
    class_name=dict[workout_type]
    return class_name(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info=training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)