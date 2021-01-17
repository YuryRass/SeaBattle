"""
    Программа Морской Бой. 
        Пользовательские корабли задаются однозначно через переменную 
    USER_SHIPS - список списков. Координаты кораблей робота генерируются
    с приминенением функции randint библиотеки random. 
        Для игры используется поле 6х6, где расставляются следующие корабли: 
    один трехпалубный, два двухпалубных и четыре однопалубных кораблей. Расстановка
    палуб осуществляется слева направо. Корабли находятся на расстоянии минимум
    одна клетка друг от друга.
        Ход пользователя происходит с помощью ввода в консольном окне 
    двух координат: y и x, разделенных между собой пробелом. Ход робота происходит 
    случайным образом без повторов.
        Выигрывает тот, кто уничтожит все корабли (11 палуб) противника. 
"""
import random
import os
import time

#Пользовательские корабли:
USER_SHIPS = [
    [0, 0, 3], [0, 1, 3], [0, 2, 3],
    [1, 3, 2], [1, 4, 2], [3, 0, 2],
    [3, 1, 2], [3, 4, 1], [4, 4, 1],
    [5, 0, 1], [5, 2, 1]
    ]

SIZE_OF_FIELD = 6

class Ship:
    def __init__(self, y, x, life):
        self.x = x
        self.y = y
        self.life = life

class Board (object):
    def __init__(self):
        self.field = (1, 2, 3, 4, 5, 6)
        self.ship_lifes = [3, 2, 2, 1, 1, 1, 1]
        self.board = [[None for _ in range(SIZE_OF_FIELD)] \
                                for _ in range(SIZE_OF_FIELD)]
        self.lifes = [[None for _ in range(SIZE_OF_FIELD)] \
                                for _ in range(SIZE_OF_FIELD)]
        self.ship_with_lifes = {'3': 3, '2': 4, '1': 4} # для подсчета палуб
    def add_ships_on_board(self, ships):
        for ship in ships:
            self.board[ship.y][ship.x] = '■'
            self.lifes[ship.y][ship.x] = ship.life
                    
class User (object):
    def __init__(self):
        self.ub = Board()
    def create_user_board(self, ships):
        user_ships = [Ship(y = u_ship[0], x = u_ship[1], life = u_ship[2]) for u_ship in ships]
        self.ub.add_ships_on_board(user_ships)
    
    def change_user_board(self, y, x, value = 'T'):
        self.ub.board[y][x] = value

    def draw_user_board(self):
        print("   |" + "|".join(str(num) for num in self.ub.field) + "|")
        count =  1
        for rec in self.ub.board:
            print (" {0} |".format(str(count)) + "|".join(el or 'О' for el in rec) + '|')
            count += 1

class Robot (object):
    def __init__(self):
        self.rb = Board()
        self.near = [-1, 1]
        self.robot_display_board = [[None for _ in range(SIZE_OF_FIELD)] \
                                for _ in range(SIZE_OF_FIELD)]
    def generate_robot_board(self):
        coords = []
        for life_ in self.rb.ship_lifes:
            while True:
                x_, y_ = random.randint(0, 5), random.randint(0, 5)
                temp_ships = []
                for i in range(life_):
                    ship = Ship(y = y_, x = x_ + i, life = life_)
                    if self.check_near_ships(ship):
                        temp_ships.append(ship)
                if len(temp_ships) == life_:
                    if [y_, x_] not in coords:
                        coords.append([y_, x_])
                        self.rb.add_ships_on_board(temp_ships)
                        break

    def check_near_ships(self, ship):
        for dx in self.near:
            try:
                if ship.x not in range(SIZE_OF_FIELD) or ship.y not in range(SIZE_OF_FIELD):
                    return False
                if self.rb.board[ship.y][ship.x + dx] == '■':
                    return False
            except IndexError:
                continue
        return True

    def draw_robot_board(self):
        print("   |" + "|".join(str(num) for num in self.rb.field) + "|")
        count =  1
        for rec in self.robot_display_board:
            print (" {0} |".format(str(count)) + "|".join(el or 'О' for el in rec) + '|')
            count += 1

    def check_step(self, y, x):
        if self.robot_display_board[y][x] is not None:
            return 'repeat'
        if self.rb.board[y][x] == '■':
            life = str(self.rb.lifes[y][x])
            self.rb.ship_with_lifes[life] -= 1
            if self.rb.ship_with_lifes[life] % self.rb.lifes[y][x] > 0:
                print("Вы ранили корабль робота!")
            else:
                print("Вы убили корабль робота!")
            return True
        else:
            print("Вы промохнулись! Далее ходит робот...")
            return False
            
class Game (object):
    def __init__(self):
        self.robot = Robot()
        self.user = User()
    def play_game(self):
        user_name = input("Введите свое имя: ")
        print("Приветсвую, {0}!".format(user_name))
        print("Вот ваши корабли для игры в Морской Бой:\n")
        self.user.create_user_board(USER_SHIPS)
        self.user.draw_user_board()
        input("\nВведите клавишу <ENTER> для генерации кораблей у Робота  ")
        self.robot.generate_robot_board()
        os.system("cls||clear")
        print("Робот сгенерировал свои корабли, скоро начнется игра...")
        time.sleep(2)
        os.system("cls||clear")
        while True:
            print("Робот: {0} жизней\n".format(sum(self.robot.rb.ship_with_lifes.values())))
            self.robot.draw_robot_board()
            print("\n{0}: {1} жизней\n".format(user_name, sum(self.user.ub.ship_with_lifes.values())))
            self.user.draw_user_board()
            coords = input('\nВаш ход "y x": ').split()
            try:
                y, x = int(coords[0]) - 1, int(coords[1]) - 1
                if y not in range(SIZE_OF_FIELD) or x not in range(SIZE_OF_FIELD):
                    raise ValueError
            except (ValueError, IndexError):
                print("Неверный ввод! Параметры у и х - целые числа из отрезка [1, 6]")
                continue
            res = self.make_user_step(y, x)
            if res == 'END':
                break
            elif res:
                continue
            if self.make_robot_step():
                break

    def make_user_step(self, y, x):
        result = self.robot.check_step(y, x)
        if result == 'repeat':
            print("Данный ход уже был. Сделайте другой ход!")
            return True
        elif result:
            self.robot.robot_display_board[y][x] = 'X'
            if self.check_win(list(self.robot.rb.ship_with_lifes.values())):
                print("Вы победили!!! УРА!!!")
                return 'END'
            return True
        else:
           self.robot.robot_display_board[y][x] = 'T'
    def make_robot_step(self):
        while True:
            y, x = random.randint(0, 5), random.randint(0, 5)
            if self.user.ub.board[y][x] == 'X' or self.user.ub.board[y][x] == 'T':
                continue
            elif self.user.ub.board[y][x] == '■':
                life = str(self.user.ub.lifes[y][x])
                self.user.ub.ship_with_lifes[life] -= 1
                print("Робот походил ({0}, {1}) - удачно".format(y + 1, x + 1))
                if self.check_win(list(self.user.ub.ship_with_lifes.values())):
                    print("Робот победил!!!")
                    return 'END'
                self.user.change_user_board(y, x, 'X')
                continue
            else:
                print("Робот походил ({0}, {1}) - мимо\n".format(y + 1, x + 1))
                self.user.change_user_board(y, x)
                break  
    def check_win(self, lifes):
        if lifes == [0] * 3:
            return True

if __name__ == "__main__":
    g = Game()
    g.play_game()


