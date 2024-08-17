# Домашнее задание по теме "Очереди для обмена данными между потоками." Применить очереди в работе с потоками,
# используя класс Queue.

import threading
import time
import random
from threading import Thread
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()  # вызываем метод родит_ого класса (Thread) чтобы
        # класс Guest корректно инициализировался как поток
        self.name = name

    def run(self):
        pause = random.randint(3, 10)
        time.sleep(pause)  # время пока гость ест


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()  # очередь из гостей которым нет места за столом
        self.tables = list(tables)  # список столов

    def guest_arrival(self, *guests):
        for guest in guests:
            # Выводим информацию о текущем состоянии столов
            for table in self.tables:
                print(f'Стол номер {table.number} {'свободен' if table.guest is None else f'занят гостем '
                                                                                          f'{table.guest.name}'}')

            # Ищем свободный стол
            free_table = next((table for table in self.tables if table.guest is None), None)
            if free_table:  # если нашли свободный стол (True)
                print(f"Гость {guest.name} садится за стол номер {free_table.number}")
                free_table.guest = guest  # закрепляем стол за гостем
                guest.start()  # Запуск потока гостя и его метода run()
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:
                self.queue.put(guest)  # помещаем гостя в очередь
                print(f"{guest.name} в очереди")

    # def guest_arrival(self, *guests):
    #     for guest in guests:
    #         # Ищем свободный стол
    #         free_table = next((table for table in self.tables if table.guest is None), None)
    #         if free_table:  # если нашли свободный стол (True)
    #             free_table.guest = guest  # закрепляем стол за гостем
    #             guest.start()  # Запуск потока гостя и его метода run()
    #             print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
    #         else:
    #             self.queue.put(guest) # помещаем гостя в очередь
    #             print(f"{guest.name} в очереди")


    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None  # Освободить стол

                    if not self.queue.empty():
                        next_guest = self.queue.get()
                        table.guest = next_guest
                        next_guest.start()  # Запуск потока нового гостя
                        print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
