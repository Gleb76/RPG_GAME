from classes.game import Bcolors, Player
from classes.magic import Spell
from classes.inventory import Item
import random

# Black magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 20, 200, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Mateor", 12, 120, "black")
quake = Spell("Quake", 14, 140, "black")

# White magic
cure = Spell("Cure", 25, 100, "white")
cura = Spell("Cura", 32, 180, "white")

# Inventory creation

potion = Item("Potion", "potion", " heal for 50 HP", 50)
hipotion = Item("hipotion", "potion", " heal for 100 HP", 100)
superpotion = Item("superpotion", "potion", "heal for 500 HP", 500)
elixer = Item("Elixer", "elixer", "Restores HP/MP of one member", 9999)
hielixer = Item("MegaElixer", "elixer", "Restores HP/MP of all members", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# initate Players
Player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, cure]
Player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5}, {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

person1 = Player("nikhil:", 3260, 132, 300, 34, Player_spells, Player_items)
person2 = Player("Kunal :", 3211, 156, 311, 120, Player_spells, Player_items)
person3 = Player("Rohan :", 1234, 256, 288, 120, Player_spells, Player_items)

enemy1 = Player("botv1.5  ", 1260, 505, 125, 325, enemy_spells, [])
enemy2 = Player("Megatron ", 11200, 705, 525, 25, enemy_spells, [])
enemy3 = Player("botv2.0  ", 1350, 600, 225, 325, enemy_spells, [])

Players = [person1, person2, person3]
enemies = [enemy1, enemy2, enemy3]

running = True
print(Bcolors.FAIL + Bcolors.BOLD + "An Enemy attack !!!" + Bcolors.ENDC)

while running:
    print("===================================")

    print("NAME                HP                                    MP")
    for person in Players:
        person.get_stats()

    for enemy in enemies:
        enemy.enemy_stats()
    for person in Players:
        person.choose_action()
        choice = input("Choose action : ")
        index = int(choice) - 1
        if index == 0:
            dmg = person.generate_damage()

            enemy = person.choose_target(enemies)
            enemies[enemy].take_dmg(dmg)

            print("You attacked " + enemies[enemy].name + "for", dmg, "points ")
            if enemies[enemy].get_hp() == 0:
                print(" " + enemies[enemy].name + "Died !!!")
                del enemies[enemy]
        elif index == 1:
            person.choose_magic()
            magic_choice = int(input("Choose Magic :")) - 1

            if magic_choice == -1:
                continue

            spell = person.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            cost = spell.cost

            current_mp = person.get_mp()
            if spell.cost > current_mp:
                print(Bcolors.FAIL + "\nNot enough MP\n" + Bcolors.ENDC)
                continue

            person.reduce_mp(spell.cost)

            if spell.type == "white":
                person.heal(magic_dmg)
                print(Bcolors.OKBLUE + "\n" + spell.name + "heal for" + str(magic_dmg) + Bcolors.ENDC)

            elif spell.type == "black":

                enemy = person.choose_target(enemies)
                enemies[enemy].take_dmg(magic_dmg)
                print(
                    Bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) + " points of damage to " + enemies[
                        enemy].name.replace(" ", "") + Bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(" " + enemies[enemy].name.replace(" ", "") + "Died !!!")
                    del enemies[enemy]

        elif index == 2:
            person.choose_items()
            item_choice = int(input("Choose Item : ")) - 1

            if item_choice == -1:
                continue
            item = person.items[item_choice]["item"]

            if person.items[item_choice]["quantity"] == 0:
                print(Bcolors.FAIL + "None Left....\n" + Bcolors.ENDC)
                continue

            person.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                person.heal(item.prop)
                print(Bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop), "HP" + Bcolors.ENDC)

            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in Players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                else:
                    person.hp = person.maxhp
                    person.mp = person.maxmp

            elif item.type == "attack":
                enemy = person.choose_target(enemies)
                enemies[enemy].take_dmg(item.prop)
                print(Bcolors.FAIL + "\n" + item.name + " deals for " + str(item.prop),
                      "HP to" + enemies[enemy].name.replace(" ", "") + Bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(" " + enemies[enemy].name.replace(" ", "") + "Died !!!")
                    del enemies[enemy]
    defeted_enemies = 0
    defeted_Players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeted_enemies += 1

    for person in Players:
        if person.get_hp() == 0:
            defeted_Players += 1

    if defeted_enemies == 2:
        print(Bcolors.OKGREEN + Bcolors.BOLD + "You win this game !!!" + Bcolors.ENDC)
        running = False

    elif defeted_Players == 2:
        print(Bcolors.FAIL + Bcolors.BOLD + "You Lost this game !!!" + Bcolors.ENDC)
        running = False

    print("\n")
    for enemy in enemies:

        enemy_choice = random.randrange(0, 2)
        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            Players[target].take_dmg(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacked " + Players[target].name.replace(":", "") + " for ",
                  enemy_dmg, " points ")

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(Bcolors.OKBLUE + spell.name + " heals " + enemy.name + " for " + str(magic_dmg) + Bcolors.ENDC)

            elif spell.type == "black":

                target = random.randrange(0, 3)
                Players[target].take_dmg(magic_dmg)
                print(Bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals " + str(
                    magic_dmg) + " points of damage to " +
                      Players[target].name.replace(" ", "") + Bcolors.ENDC)

                if Players[target].get_hp() == 0:
                    print(" " + Players[target].name.replace(":", "") + " has Died !!!")
                    del Players[target]

            # print("Enemy Chose ",spell," damage is ",magic_dmg)
