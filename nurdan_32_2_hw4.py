import random
from enum import Enum
from random import choice, randint


class SuperAbility(Enum):
    NONE = 0
    CRITICAL_DAMAGE = 1
    BOOST = 2
    HEAL = 3
    BLOCK_DAMAGE_AND_REVERT = 4
    STUN = 5
    REVIVAL = 6
    AGGRESSION = 7
    SHURIKEN = 8
    DAMAGE_INCREASE_WITH_LOW_HP = 9




class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value <= 0:
            self.__health = 0
            self.__damage = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.__health} damage: {self.__damage}'




class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = SuperAbility.NONE

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes):
        hero = choice(heroes)
        self.__defence = hero.ability




    def attack(self, heroes):
        for hero in heroes:
            if hero.health > 0:
                if hero.ability == SuperAbility.BLOCK_DAMAGE_AND_REVERT:
                    hero.blocked_damage = self.damage // 5
                    hero.health -= (self.damage - hero.blocked_damage)
                else:
                    hero.health -= self.damage

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence.name}'




class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        if isinstance(ability, SuperAbility):
            self.__ability = ability
        else:
            raise ValueError('Wrong data type for ability')

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        if self.health > 0 and boss.health > 0:
            boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass




class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.CRITICAL_DAMAGE)

    def apply_super_power(self, boss, heroes):
        coefficent = randint(2, 7)
        boss.health -= self.damage * coefficent
        print(f'<<< Warrior {self.name} hit critically {self.damage * coefficent} >>>')




class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.BOOST)

    def apply_super_power(self, boss, heroes):

        coefficent = randint(1 ,5)
        for hero in heroes:
            if hero.health > 0 and hero != self:
                    hero.damage = hero.damage + coefficent




class Thor(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.STUN)

    def apply_super_power(self, boss, heroes):
        r = random.randint(0, 5)
        if self.health > 0:
            if r == 2:
                boss.damage = 0
                print(f'<<< Thor {self.name} stunned the boss {boss.name} >>>')
            else:
                boss.damage = 50




class Witcher(Hero):
    def __init__(self, name, health, damage=0):
        super().__init__(name, health, damage, SuperAbility.REVIVAL)

    def apply_super_power(self, boss, heroes):
        r = random.randint(0, 1)
        for hero in heroes:
            if r == 1:
                if hero.health <= 0:
                    hero.health = self.health
                    hero.damage = 15
                    self.health = 0
                    print(f'<<< {self.name} Revived the first dead >>>')
                    break




class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.BLOCK_DAMAGE_AND_REVERT)
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss, heroes):
        boss.health -= (self.blocked_damage + self.damage)
        print(f'<<< Berserk {self.name} reverted {self.blocked_damage + self.damage} >>>')




class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, SuperAbility.HEAL)
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and hero != self:
                hero.health += self.__heal_points


class Spitfire(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.AGGRESSION)

    def apply_super_power(self, boss, heroes):
        aggressive_damage = 80
        for hero in heroes:
            if hero.health <= 0:
                self.damage = (self.damage + aggressive_damage)
                break




class Reaper(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.DAMAGE_INCREASE_WITH_LOW_HP)

    def apply_super_power(self, boss, heroes):

        if self.health <= (self.health / 100) * 30:
            self.damage = self.damage * 2

        if self.health <= (self.health / 100) * 15:
            self.damage = self.damage * 3




class Samurai(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.SHURIKEN)

    def apply_super_power(self, boss, heroes):
        coefficent = (150)
        r = random.randint(0, 1)
        if self.health > 0:
            if r == 0:
                boss.health -= (self.damage + coefficent)
                print(f'<<< samurai {self.name} threw a shuriken of the first kind >>>')
            if r == 1:
                boss.health += coefficent
                print(f'<<< samurai {self.name} threw shuriken of the second kind >>>')







round_number = 0


def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
    return all_heroes_dead


def play_round(boss, heroes):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.ability != boss.defence:
            hero.attack(boss)
            if hero.health > 0 and boss.health > 0:
                hero.apply_super_power(boss, heroes)
    show_stats(boss, heroes)


def show_stats(boss, heroes):
    print(f'---------- ROUND {round_number} ----------')
    print(boss)
    for hero in heroes:
        print(hero)


def start_game():
    boss = Boss('Satana', 3000, 50)

    warrior = Warrior('Ahiles', 270, 10)
    doc = Medic('Avicenna', 250, 5, 15)
    berserk = Berserk('Gutz', 260, 10)
    assistant = Medic('Nurik', 300, 5, 5)
# ОСНОВНОЕ
    magic = Magic('Hendolf', 280, 15)
    thor = Thor('Halk', 290, 15)
    witcher = Witcher('Henry', 350)
# ДОПОЛНИТЕЛЬНОЕ
    spitfire = Spitfire('spit', 250, 5)
    samurai = Samurai('yakuza', 210, 14)
    reaper = Reaper('Zuko', 250, 15)


    heroes_list = [warrior, doc, magic, berserk, assistant, thor, witcher, spitfire, samurai, reaper]

    show_stats(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()
