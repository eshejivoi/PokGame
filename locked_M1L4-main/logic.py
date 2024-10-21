import random
import requests
from datetime import datetime, timedelta


class Pokemon:
    pokemons = {}

    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer

        types = [Wizard, Fighter]
        self.type = random.choice(types)
        self.power = random.randint(1, 200)
        self.hp = random.randint(10, 150)
        self.pokemon_number = random.randint(1, 1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.last_feed_time = datetime.now()

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['other']['official-artwork']['front_default'])
        else:
            return "https://static.wikia.nocookie.net/pokemon/images/0/0d/025Pikachu.png/revision/latest/scale-to-width-down/1000?cb=20181020165701&path-prefix=ru"

    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    def attack(self, enemy):
        # if isinstance(enemy, Wizard):
        #    chance = random.randint(1, 5)
        #    if chance == 1:
        #        return "Покемон-волшебник применил щит в сражении"
        if enemy.hp == 0:
            return f"покемон @{enemy.pokemon_trainer} уже мертв, лежачих не бьют"
        if self.hp == 0:
            return f"покемон @{self.pokemon_trainer} мертв. Вы не можете атаковать"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "

    def bonus(self, enemy):
        if enemy.hp <= 0:
            self.power += 10
            return f'Вы получили бонус! +10 к силе'

    def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        timedelete = timedelta(hours=feed_interval)
        if (current_time - self.last_feed_time) > timedelete:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {current_time + timedelta(feed_interval)}"

            # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покеомона: {self.name}\n здоровье покемона: {self.hp}\n сила атаки: {self.power}\n класс: {self.type.__name__}"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img


class Wizard(Pokemon):
    def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"


class Fighter(Pokemon):
    def attack(self, enemy):
        if isinstance(enemy, Fighter):
            super_power = random.randint(5, 15)
            self.power += super_power
            result = super().attack(enemy)
            self.power -= super_power
            return result + f"\nБоец применил супер-атаку силой:{super_power}"
