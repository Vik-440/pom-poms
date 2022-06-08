# Створити клас Animal з атрбибутами name, size та з методами move, eat, sleep. Від цього классу створити 3 
# нащадки(dog, bird, fish) в яких повинні бути методи, які виводять в консоль, їх атрибути.
# Також в кожного классу повинен бути переписані методи Animal в залежності від назви(наприклад собака під 
# час move ходить, а риба пливе)

class Animal:
    def __init__(self, name, size):
            # super().__init__()
        self.name=name
        self.size=size
    def move(self):
        print ("Animals move in different method")
    def eat(self):
        print ("Animals eat in different method")
    def sleep(self):
        print ("Animals sleep in different method")

class Dog (Animal):
    def move(self):
        print(self.name + " has size " + self.size + " and run")
    def eat(self):
        print(self.name + " has size " + self.size + " and eat from plate")
    def sleep(self):
        print(self.name + " has size " + self.size + " and sleep in booth")

class Bird (Animal):
    def move(self):
        print(self.name + " has size " + self.size + " and fly")
    def eat(self):
        print(self.name + " has size " + self.size + " and eats with its beak")
    def sleep(self):
        print(self.name + " has size " + self.size + " and on branch")

class Fish (Animal):
    def move(self):
        print(self.name + " has size " + self.size + " and swim")
    def eat(self):
        print(self.name + " has size " + self.size + " and eat in water")
    def sleep(self):
        print(self.name + " has size " + self.size + " and sleep in water")

# треба ще сюди створити class Person, з атрибутами, status та money. Після цього створити класс Centaur,
# який наслідується від animal та person. Ініціалізувати його та вивести всі атрибути.

class Person:
    def __init__(self, status, money):
            # super().__init__()
        self.status=status
        self.money=money

class Centaur(Animal, Person):
    def __init__(self, *, name, size, status, money):
        Animal.__init__(self, name, size)
        Person.__init__(self, status, money)
    
    def print_parameters (self):
        print(self.name + " has size " + self.size + " in stutus " + self.status + " and has " + self.money + " money")


peter=Centaur(name="Peter", size="400 kg", status="fabulous animal", money="$ 3'000")
# peter=Centaur("Peter", "400 kg", "fabulous animal", "$ 3'000")
# peter1=Person("fabulous animal","$ 3'000")
# peter=Centaur("Peter", "400 kg")
# peter=Animal("Peter", "400 kg")
peter.print_parameters()


# dachshund=Dog("Mika", "30 cm")
# dachshund.move()
# dachshund.eat()
# dachshund.sleep()