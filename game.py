#!/usr/bin/env python3
"""
High Wizardy - A text-based RPG with combat, weapons, and magic
"""

import json
import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict


class Item:
    """Base class for game items"""
    def __init__(self, name: str, description: str, price: int):
        self.name = name
        self.description = description
        self.price = price


class Weapon(Item):
    """Weapon class with damage stats"""
    def __init__(self, name: str, description: str, price: int, damage: int, mana_cost: int = 0):
        super().__init__(name, description, price)
        self.damage = damage
        self.mana_cost = mana_cost
    
    def to_dict(self):
        return {
            'type': 'weapon',
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'damage': self.damage,
            'mana_cost': self.mana_cost
        }


class Armor(Item):
    """Armor class with defense stats"""
    def __init__(self, name: str, description: str, price: int, defense: int):
        super().__init__(name, description, price)
        self.defense = defense
    
    def to_dict(self):
        return {
            'type': 'armor',
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'defense': self.defense
        }


class PropertyUpgrade:
    """Property upgrade (library, gym, garden, etc.)"""
    def __init__(self, name: str, description: str, cost: int, happiness_bonus: int):
        self.name = name
        self.description = description
        self.cost = cost
        self.happiness_bonus = happiness_bonus
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'cost': self.cost,
            'happiness_bonus': self.happiness_bonus
        }


class Property:
    """Property that can be owned by players"""
    def __init__(self, property_type: str, name: str, description: str, 
                 price_shillings: int, price_pennies: int, size: int, max_upgrades: int):
        self.property_type = property_type  # cottage, manor, castle
        self.name = name
        self.description = description
        self.price_shillings = price_shillings
        self.price_pennies = price_pennies
        self.size = size
        self.max_upgrades = max_upgrades
        self.upgrades: List[PropertyUpgrade] = []
        self.is_rented = False
        self.rented_to: Optional[str] = None
        self.rent_amount = 0
        self.listed_for_rent = False
    
    def get_price_in_gold(self) -> int:
        """Convert shillings and pennies to gold (1 shilling = 12 pennies, 20 shillings = 1 gold)"""
        total_pennies = (self.price_shillings * 12) + self.price_pennies
        return total_pennies  # Simplified: using pennies as gold equivalent for game balance
    
    def add_upgrade(self, upgrade: PropertyUpgrade) -> bool:
        """Add an upgrade if there's room"""
        if len(self.upgrades) < self.max_upgrades:
            self.upgrades.append(upgrade)
            return True
        return False
    
    def calculate_happiness_bonus(self) -> int:
        """Calculate total happiness from this property and its upgrades"""
        base_happiness = {'cottage': 10, 'manor': 25, 'castle': 50}.get(self.property_type, 0)
        upgrade_happiness = sum(u.happiness_bonus for u in self.upgrades)
        return base_happiness + upgrade_happiness
    
    def to_dict(self):
        return {
            'property_type': self.property_type,
            'name': self.name,
            'description': self.description,
            'price_shillings': self.price_shillings,
            'price_pennies': self.price_pennies,
            'size': self.size,
            'max_upgrades': self.max_upgrades,
            'upgrades': [u.to_dict() for u in self.upgrades],
            'is_rented': self.is_rented,
            'rented_to': self.rented_to,
            'rent_amount': self.rent_amount,
            'listed_for_rent': self.listed_for_rent
        }


class Player:
    """Player character with stats and inventory"""
    def __init__(self, name: str = "Hero"):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.mana = 100
        self.max_mana = 100
        self.energy = 100
        self.max_energy = 100
        self.gold = 100
        self.weapon: Optional[Weapon] = None
        self.armor: Optional[Armor] = None
        self.inventory: List[Item] = []
        self.last_energy_update = datetime.now()
        self.experience = 0
        self.level = 1
        # Combat stats
        self.strength = 0
        self.agility = 0
        self.vitality = 0
        # Property system
        self.properties: List[Property] = []
        self.happiness = 0
        self.max_happiness = 100
    
    def update_energy(self):
        """Regenerate energy: 5 energy every 15 minutes"""
        current_time = datetime.now()
        time_elapsed = current_time - self.last_energy_update
        minutes_elapsed = time_elapsed.total_seconds() / 60
        
        if minutes_elapsed >= 15:
            intervals = int(minutes_elapsed // 15)
            energy_to_add = intervals * 5
            self.energy = min(self.max_energy, self.energy + energy_to_add)
            # Update last_energy_update by the intervals we just processed
            self.last_energy_update += timedelta(minutes=intervals * 15)
            return energy_to_add
        return 0
    
    def use_energy(self, amount: int) -> bool:
        """Use energy if available"""
        self.update_energy()
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False
    
    def use_mana(self, amount: int) -> bool:
        """Use mana if available"""
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False
    
    def heal(self, amount: int):
        """Heal the player"""
        self.health = min(self.max_health, self.health + amount)
    
    def restore_mana(self, amount: int):
        """Restore mana"""
        self.mana = min(self.max_mana, self.mana + amount)
    
    def calculate_happiness(self):
        """Calculate happiness based on owned properties and upgrades"""
        total_happiness = sum(prop.calculate_happiness_bonus() for prop in self.properties)
        self.happiness = min(total_happiness, self.max_happiness)
        return self.happiness
    
    def get_happiness_multiplier(self) -> float:
        """Get stat gain multiplier based on happiness (1.0 to 1.5x)"""
        self.calculate_happiness()
        # At max happiness (100), get 50% bonus
        return 1.0 + (self.happiness / 200.0)
    
    def add_property(self, property: Property):
        """Add a property to player's collection"""
        self.properties.append(property)
        self.calculate_happiness()
    
    def check_dodge(self) -> bool:
        """Check if player dodges an attack based on agility"""
        import random
        # Each agility point gives 2% dodge chance, capped at 50%
        dodge_chance = min(self.agility * 2, 50)
        return random.randint(1, 100) <= dodge_chance
    
    def take_damage(self, damage: int) -> tuple[int, bool]:
        """Take damage, reduced by armor and vitality. Returns (actual_damage, dodged)"""
        # Check for dodge first
        if self.check_dodge():
            return (0, True)
        
        defense = self.armor.defense if self.armor else 0
        vitality_defense = self.vitality * 2  # Each vitality point adds 2 defense
        total_defense = defense + vitality_defense
        actual_damage = max(1, damage - total_defense)
        self.health = max(0, self.health - actual_damage)
        return (actual_damage, False)
    
    def attack_damage(self) -> int:
        """Calculate attack damage with strength bonus"""
        base_damage = 10
        weapon_damage = self.weapon.damage if self.weapon else 0
        strength_bonus = self.strength * 3  # Each strength point adds 3 damage
        return base_damage + weapon_damage + strength_bonus
    
    def equip_weapon(self, weapon: Weapon):
        """Equip a weapon"""
        self.weapon = weapon
    
    def equip_armor(self, armor: Armor):
        """Equip armor"""
        self.armor = armor
    
    def gain_experience(self, exp: int):
        """Gain experience and level up if needed"""
        self.experience += exp
        exp_needed = self.level * 100
        if self.experience >= exp_needed:
            self.level_up()
    
    def level_up(self):
        """Level up the player"""
        self.level += 1
        self.max_health += 20
        self.max_mana += 10
        self.max_energy += 10
        self.health = self.max_health
        self.mana = self.max_mana
        self.energy = self.max_energy
        print(f"\n🎉 Level Up! You are now level {self.level}!")
        print(f"Max Health: {self.max_health}, Max Mana: {self.max_mana}, Max Energy: {self.max_energy}")
    
    def to_dict(self):
        """Convert player to dictionary for saving"""
        return {
            'name': self.name,
            'health': self.health,
            'max_health': self.max_health,
            'mana': self.mana,
            'max_mana': self.max_mana,
            'energy': self.energy,
            'max_energy': self.max_energy,
            'gold': self.gold,
            'weapon': self.weapon.to_dict() if self.weapon else None,
            'armor': self.armor.to_dict() if self.armor else None,
            'last_energy_update': self.last_energy_update.isoformat(),
            'experience': self.experience,
            'level': self.level,
            'strength': self.strength,
            'agility': self.agility,
            'vitality': self.vitality,
            'properties': [p.to_dict() for p in self.properties],
            'happiness': self.happiness,
            'max_happiness': self.max_happiness
        }


class Enemy:
    """Enemy character"""
    def __init__(self, name: str, health: int, damage: int, exp_reward: int, gold_reward: int):
        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
    
    def take_damage(self, damage: int) -> int:
        """Take damage"""
        self.health = max(0, self.health - damage)
        return damage
    
    def is_alive(self) -> bool:
        """Check if enemy is alive"""
        return self.health > 0


class Shop:
    """Shop for buying weapons and armor"""
    def __init__(self):
        self.weapons = [
            Weapon("Wooden Sword", "A basic wooden sword", 50, 5),
            Weapon("Iron Sword", "A sturdy iron sword", 150, 15),
            Weapon("Steel Sword", "A sharp steel sword", 300, 30),
            Weapon("Fire Staff", "A magical staff that shoots fire", 400, 40, mana_cost=10),
            Weapon("Legendary Blade", "A legendary weapon of immense power", 1000, 80, mana_cost=5),
        ]
        self.armors = [
            Armor("Leather Armor", "Basic leather protection", 60, 5),
            Armor("Iron Armor", "Sturdy iron plating", 180, 15),
            Armor("Steel Armor", "Strong steel armor", 350, 30),
            Armor("Enchanted Robes", "Magical robes with protection", 500, 40),
            Armor("Dragon Scale Armor", "Armor made from dragon scales", 1200, 70),
        ]


class PropertyMarket:
    """Market for buying and renting properties"""
    def __init__(self):
        self.available_properties = [
            Property("cottage", "Cozy Cottage", "A small but comfortable dwelling", 50, 0, 100, 2),
            Property("cottage", "Village Cottage", "A charming cottage in the village", 75, 6, 120, 2),
            Property("manor", "Stone Manor", "A sturdy stone manor with multiple rooms", 200, 0, 300, 4),
            Property("manor", "Lakeside Manor", "A beautiful manor by the lake", 250, 0, 350, 4),
            Property("castle", "Small Castle", "A modest castle with defensive walls", 500, 0, 800, 6),
            Property("castle", "Grand Castle", "A magnificent castle fit for nobility", 1000, 0, 1200, 8),
        ]
        self.available_upgrades = {
            'cottage': [
                PropertyUpgrade("Small Garden", "A pleasant garden for relaxation", 20, 5),
                PropertyUpgrade("Bookshelf", "A cozy reading corner", 25, 5),
            ],
            'manor': [
                PropertyUpgrade("Library", "An extensive collection of books", 50, 10),
                PropertyUpgrade("Training Room", "Basic workout equipment", 60, 10),
                PropertyUpgrade("Garden", "A well-maintained garden", 40, 8),
                PropertyUpgrade("Workshop", "A place for crafts and hobbies", 55, 9),
            ],
            'castle': [
                PropertyUpgrade("Grand Library", "A magnificent library with rare books", 100, 15),
                PropertyUpgrade("Full Gymnasium", "Complete training facilities", 120, 15),
                PropertyUpgrade("Royal Garden", "Sprawling gardens with exotic plants", 90, 12),
                PropertyUpgrade("Armory", "A well-stocked armory", 110, 13),
                PropertyUpgrade("Chapel", "A peaceful place for meditation", 80, 11),
                PropertyUpgrade("Observatory", "For studying the stars", 95, 12),
            ]
        }
        self.rental_listings: List[Dict] = []


class Game:
    """Main game class"""
    def __init__(self):
        self.player = Player()
        self.shop = Shop()
        self.property_market = PropertyMarket()
        self.save_file = "savegame.json"
        self.leaderboard_file = "leaderboard.json"
    
    def display_status(self):
        """Display player status"""
        energy_regen = self.player.update_energy()
        if energy_regen > 0:
            print(f"⚡ Regenerated {energy_regen} energy!")
        
        print("\n" + "="*50)
        print(f"🧙 {self.player.name} - Level {self.player.level}")
        print(f"❤️  Health: {self.player.health}/{self.player.max_health}")
        print(f"💙 Mana: {self.player.mana}/{self.player.max_mana}")
        print(f"⚡ Energy: {self.player.energy}/{self.player.max_energy}")
        print(f"💰 Gold: {self.player.gold}")
        print(f"⭐ Experience: {self.player.experience}/{self.player.level * 100}")
        
        if self.player.weapon:
            print(f"⚔️  Weapon: {self.player.weapon.name} (Damage: {self.player.weapon.damage})")
        else:
            print("⚔️  Weapon: None (Fists)")
        
        if self.player.armor:
            print(f"🛡️  Armor: {self.player.armor.name} (Defense: {self.player.armor.defense})")
        else:
            print("🛡️  Armor: None")
        
        # Display combat stats
        print(f"💪 Combat Stats - STR: {self.player.strength} | AGI: {self.player.agility} | VIT: {self.player.vitality}")
        
        # Display happiness bar
        self.player.calculate_happiness()
        happiness_bar = self.create_bar(self.player.happiness, self.player.max_happiness, 20)
        multiplier = self.player.get_happiness_multiplier()
        print(f"😊 Happiness: {happiness_bar} {self.player.happiness}/{self.player.max_happiness} (x{multiplier:.2f} training bonus)")
        
        # Display properties count
        if self.player.properties:
            print(f"🏠 Properties: {len(self.player.properties)} owned")
        
        print("="*50)
    
    def create_bar(self, current: int, maximum: int, length: int) -> str:
        """Create a visual progress bar"""
        filled = int((current / maximum) * length) if maximum > 0 else 0
        return "█" * filled + "░" * (length - filled)
    
    def weapon_shop(self):
        """Weapon shop menu"""
        while True:
            print("\n🗡️  WEAPON SHOP 🗡️")
            print(f"Your gold: {self.player.gold}")
            print("\nAvailable Weapons:")
            for i, weapon in enumerate(self.shop.weapons, 1):
                mana_info = f", Mana: {weapon.mana_cost}" if weapon.mana_cost > 0 else ""
                print(f"{i}. {weapon.name} - {weapon.price}g (Damage: {weapon.damage}{mana_info})")
                print(f"   {weapon.description}")
            
            print("\n0. Back to main menu")
            
            choice = input("\nSelect weapon to buy (0 to exit): ").strip()
            
            if choice == "0":
                break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.shop.weapons):
                    weapon = self.shop.weapons[idx]
                    if self.player.gold >= weapon.price:
                        self.player.gold -= weapon.price
                        old_weapon = self.player.weapon
                        self.player.equip_weapon(weapon)
                        print(f"\n✅ Purchased and equipped {weapon.name}!")
                        if old_weapon:
                            # Sell old weapon for half price
                            refund = old_weapon.price // 2
                            self.player.gold += refund
                            print(f"💰 Sold old weapon for {refund}g")
                    else:
                        print(f"\n❌ Not enough gold! Need {weapon.price}g, have {self.player.gold}g")
                else:
                    print("\n❌ Invalid choice!")
            except ValueError:
                print("\n❌ Invalid input!")
    
    def armor_shop(self):
        """Armor shop menu"""
        while True:
            print("\n🛡️  ARMOR SHOP 🛡️")
            print(f"Your gold: {self.player.gold}")
            print("\nAvailable Armor:")
            for i, armor in enumerate(self.shop.armors, 1):
                print(f"{i}. {armor.name} - {armor.price}g (Defense: {armor.defense})")
                print(f"   {armor.description}")
            
            print("\n0. Back to main menu")
            
            choice = input("\nSelect armor to buy (0 to exit): ").strip()
            
            if choice == "0":
                break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.shop.armors):
                    armor = self.shop.armors[idx]
                    if self.player.gold >= armor.price:
                        self.player.gold -= armor.price
                        old_armor = self.player.armor
                        self.player.equip_armor(armor)
                        print(f"\n✅ Purchased and equipped {armor.name}!")
                        if old_armor:
                            # Sell old armor for half price
                            refund = old_armor.price // 2
                            self.player.gold += refund
                            print(f"💰 Sold old armor for {refund}g")
                    else:
                        print(f"\n❌ Not enough gold! Need {armor.price}g, have {self.player.gold}g")
                else:
                    print("\n❌ Invalid choice!")
            except ValueError:
                print("\n❌ Invalid input!")
    
    def combat(self):
        """Initiate combat with an enemy"""
        # Check energy requirement
        if not self.player.use_energy(25):
            print("\n❌ Not enough energy! Combat requires 25 energy.")
            print(f"Current energy: {self.player.energy}/{self.player.max_energy}")
            print("Energy regenerates 5 points every 15 minutes.")
            return
        
        # Create enemy based on player level
        enemies = [
            Enemy("Goblin", 30 + (self.player.level * 10), 8 + self.player.level, 20, 30),
            Enemy("Orc", 50 + (self.player.level * 15), 12 + self.player.level, 35, 50),
            Enemy("Dark Mage", 40 + (self.player.level * 12), 15 + self.player.level, 50, 70),
            Enemy("Dragon", 100 + (self.player.level * 25), 20 + self.player.level, 100, 150),
        ]
        
        import random
        enemy = random.choice(enemies)
        
        print(f"\n⚔️  A wild {enemy.name} appears!")
        print(f"Enemy Health: {enemy.health}/{enemy.max_health}")
        print(f"Enemy Damage: {enemy.damage}")
        
        while enemy.is_alive() and self.player.health > 0:
            print(f"\n--- Combat Round ---")
            print(f"Your Health: {self.player.health}/{self.player.max_health}")
            print(f"Your Mana: {self.player.mana}/{self.player.max_mana}")
            print(f"Enemy Health: {enemy.health}/{enemy.max_health}")
            print("\n1. Attack")
            print("2. Use Magic (if weapon has mana cost)")
            print("3. Flee")
            
            choice = input("\nYour action: ").strip()
            
            if choice == "1":
                # Regular attack
                damage = self.player.attack_damage()
                enemy.take_damage(damage)
                print(f"\n💥 You attack {enemy.name} for {damage} damage!")
                
            elif choice == "2":
                # Magic attack
                if self.player.weapon and self.player.weapon.mana_cost > 0:
                    if self.player.use_mana(self.player.weapon.mana_cost):
                        damage = int(self.player.attack_damage() * 1.5)
                        enemy.take_damage(damage)
                        print(f"\n🔮 You cast a spell with {self.player.weapon.name} for {damage} damage!")
                    else:
                        print("\n❌ Not enough mana!")
                        continue
                else:
                    print("\n❌ Your weapon cannot cast spells!")
                    continue
                    
            elif choice == "3":
                print("\n🏃 You flee from combat!")
                return
            else:
                print("\n❌ Invalid choice!")
                continue
            
            # Check if enemy is defeated
            if not enemy.is_alive():
                print(f"\n🎉 Victory! You defeated {enemy.name}!")
                self.player.gold += enemy.gold_reward
                self.player.gain_experience(enemy.exp_reward)
                print(f"💰 Gained {enemy.gold_reward} gold")
                print(f"⭐ Gained {enemy.exp_reward} experience")
                return
            
            # Enemy attacks
            damage = enemy.damage
            actual_damage, dodged = self.player.take_damage(damage)
            if dodged:
                print(f"\n💨 You dodged {enemy.name}'s attack!")
            else:
                print(f"\n💢 {enemy.name} attacks you for {actual_damage} damage!")
            
            # Check if player is defeated
            if self.player.health <= 0:
                print("\n💀 You have been defeated!")
                print("Game Over!")
                exit(0)
    
    def rest(self):
        """Rest to restore health and mana"""
        print("\n😴 Resting...")
        self.player.heal(50)
        self.player.restore_mana(50)
        print(f"✅ Restored 50 health and 50 mana!")
    
    def gym(self):
        """Gym for training combat stats"""
        while True:
            print("\n💪 TRAINING GYM 💪")
            print(f"Your gold: {self.player.gold}")
            multiplier = self.player.get_happiness_multiplier()
            print(f"😊 Happiness Bonus: x{multiplier:.2f} stat gains")
            print(f"\nCurrent Combat Stats:")
            print(f"  Strength: {self.player.strength} (+{self.player.strength * 3} damage)")
            dodge_chance = min(self.player.agility * 2, 50)
            print(f"  Agility: {self.player.agility} ({dodge_chance}% dodge chance)")
            print(f"  Vitality: {self.player.vitality} (+{self.player.vitality * 2} defense)")
            
            print("\n--- Training Options ---")
            print(f"1. Train Strength (50 gold, +{int(1 * multiplier)} STR)")
            print(f"2. Train Agility (50 gold, +{int(1 * multiplier)} AGI)")
            print(f"3. Train Vitality (50 gold, +{int(1 * multiplier)} VIT)")
            print(f"4. Intensive Training (200 gold, +{int(2 * multiplier)} to all stats)")
            print("0. Back to main menu")
            
            choice = input("\nWhat would you like to train? ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                if self.player.gold >= 50:
                    self.player.gold -= 50
                    gain = int(1 * multiplier)
                    self.player.strength += gain
                    print(f"\n💪 Strength training complete! +{gain} STR (now {self.player.strength})")
                    if gain > 1:
                        print(f"   ✨ Happiness bonus gave you extra gains!")
                else:
                    print("\n❌ Not enough gold! Need 50 gold.")
            elif choice == "2":
                if self.player.gold >= 50:
                    self.player.gold -= 50
                    gain = int(1 * multiplier)
                    self.player.agility += gain
                    print(f"\n🏃 Agility training complete! +{gain} AGI (now {self.player.agility})")
                    if gain > 1:
                        print(f"   ✨ Happiness bonus gave you extra gains!")
                else:
                    print("\n❌ Not enough gold! Need 50 gold.")
            elif choice == "3":
                if self.player.gold >= 50:
                    self.player.gold -= 50
                    gain = int(1 * multiplier)
                    self.player.vitality += gain
                    print(f"\n🛡️  Vitality training complete! +{gain} VIT (now {self.player.vitality})")
                    if gain > 1:
                        print(f"   ✨ Happiness bonus gave you extra gains!")
                else:
                    print("\n❌ Not enough gold! Need 50 gold.")
            elif choice == "4":
                if self.player.gold >= 200:
                    self.player.gold -= 200
                    gain = int(2 * multiplier)
                    self.player.strength += gain
                    self.player.agility += gain
                    self.player.vitality += gain
                    print(f"\n🌟 Intensive training complete! +{gain} to all stats")
                    print(f"STR: {self.player.strength}, AGI: {self.player.agility}, VIT: {self.player.vitality}")
                    if gain > 2:
                        print(f"   ✨ Happiness bonus gave you extra gains!")
                else:
                    print("\n❌ Not enough gold! Need 200 gold.")
            else:
                print("\n❌ Invalid choice!")
    
    def property_menu(self):
        """Property management menu"""
        while True:
            print("\n🏠 PROPERTY MARKET 🏠")
            print(f"Your gold: {self.player.gold}")
            print(f"\nYou own {len(self.player.properties)} properties")
            
            print("\n--- Property Options ---")
            print("1. Browse Properties for Sale")
            print("2. View My Properties")
            print("3. Upgrade a Property")
            print("4. Sell a Property")
            print("5. List Property for Rent")
            print("6. View Rental Listings")
            print("0. Back to main menu")
            
            choice = input("\nWhat would you like to do? ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self.browse_properties()
            elif choice == "2":
                self.view_my_properties()
            elif choice == "3":
                self.upgrade_property()
            elif choice == "4":
                self.sell_property()
            elif choice == "5":
                self.list_for_rent()
            elif choice == "6":
                self.view_rental_listings()
            else:
                print("\n❌ Invalid choice!")
    
    def browse_properties(self):
        """Browse and buy properties"""
        print("\n🏠 PROPERTIES FOR SALE 🏠")
        print(f"Your gold: {self.player.gold}")
        print("\nAvailable Properties:")
        
        for i, prop in enumerate(self.property_market.available_properties, 1):
            price = prop.get_price_in_gold()
            happiness = {'cottage': 10, 'manor': 25, 'castle': 50}.get(prop.property_type, 0)
            print(f"{i}. {prop.name} ({prop.property_type.capitalize()})")
            print(f"   Price: {prop.price_shillings}s {prop.price_pennies}p ({price}g)")
            print(f"   Size: {prop.size} sq ft | Max Upgrades: {prop.max_upgrades}")
            print(f"   Base Happiness: +{happiness}")
            print(f"   {prop.description}")
        
        print("\n0. Back")
        
        choice = input("\nSelect property to buy (0 to go back): ").strip()
        
        if choice == "0":
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.property_market.available_properties):
                prop = self.property_market.available_properties[idx]
                price = prop.get_price_in_gold()
                
                if self.player.gold >= price:
                    confirm = input(f"\nBuy {prop.name} for {price}g? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.player.gold -= price
                        # Create a new instance to avoid sharing references
                        new_prop = Property(
                            prop.property_type, prop.name, prop.description,
                            prop.price_shillings, prop.price_pennies,
                            prop.size, prop.max_upgrades
                        )
                        self.player.add_property(new_prop)
                        print(f"\n✅ Congratulations! You are now the owner of {prop.name}!")
                        print(f"😊 Your happiness increased to {self.player.happiness}!")
                else:
                    print(f"\n❌ Not enough gold! Need {price}g, have {self.player.gold}g")
            else:
                print("\n❌ Invalid choice!")
        except ValueError:
            print("\n❌ Invalid input!")
    
    def view_my_properties(self):
        """View player's owned properties"""
        if not self.player.properties:
            print("\n🏚️  You don't own any properties yet.")
            return
        
        print("\n🏠 MY PROPERTIES 🏠")
        for i, prop in enumerate(self.player.properties, 1):
            status = "🔒 Rented" if prop.is_rented else "✅ Vacant"
            print(f"\n{i}. {prop.name} ({prop.property_type.capitalize()}) - {status}")
            print(f"   Size: {prop.size} sq ft")
            print(f"   Upgrades: {len(prop.upgrades)}/{prop.max_upgrades}")
            print(f"   Happiness Bonus: +{prop.calculate_happiness_bonus()}")
            
            if prop.upgrades:
                print(f"   Installed Upgrades:")
                for upgrade in prop.upgrades:
                    print(f"     • {upgrade.name} (+{upgrade.happiness_bonus} happiness)")
            
            if prop.is_rented:
                print(f"   Rented to: {prop.rented_to}")
                print(f"   Rent: {prop.rent_amount}g/period")
        
        input("\nPress Enter to continue...")
    
    def upgrade_property(self):
        """Upgrade a property"""
        if not self.player.properties:
            print("\n🏚️  You don't own any properties yet.")
            return
        
        print("\n🔧 UPGRADE PROPERTY 🔧")
        print("Select a property to upgrade:")
        
        for i, prop in enumerate(self.player.properties, 1):
            print(f"{i}. {prop.name} - Upgrades: {len(prop.upgrades)}/{prop.max_upgrades}")
        
        print("\n0. Back")
        
        choice = input("\nSelect property: ").strip()
        
        if choice == "0":
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.properties):
                prop = self.player.properties[idx]
                
                if len(prop.upgrades) >= prop.max_upgrades:
                    print(f"\n❌ {prop.name} is fully upgraded!")
                    return
                
                # Show available upgrades for this property type
                available_upgrades = self.property_market.available_upgrades.get(prop.property_type, [])
                
                if not available_upgrades:
                    print(f"\n❌ No upgrades available for {prop.property_type}s!")
                    return
                
                print(f"\n🔧 Available Upgrades for {prop.name}:")
                for i, upgrade in enumerate(available_upgrades, 1):
                    print(f"{i}. {upgrade.name} - {upgrade.cost}g (+{upgrade.happiness_bonus} happiness)")
                    print(f"   {upgrade.description}")
                
                print("\n0. Cancel")
                
                upgrade_choice = input("\nSelect upgrade: ").strip()
                
                if upgrade_choice == "0":
                    return
                
                try:
                    upgrade_idx = int(upgrade_choice) - 1
                    if 0 <= upgrade_idx < len(available_upgrades):
                        upgrade = available_upgrades[upgrade_idx]
                        
                        if self.player.gold >= upgrade.cost:
                            confirm = input(f"\nInstall {upgrade.name} for {upgrade.cost}g? (y/n): ").strip().lower()
                            if confirm == 'y':
                                self.player.gold -= upgrade.cost
                                # Create new upgrade instance
                                new_upgrade = PropertyUpgrade(
                                    upgrade.name, upgrade.description,
                                    upgrade.cost, upgrade.happiness_bonus
                                )
                                prop.add_upgrade(new_upgrade)
                                self.player.calculate_happiness()
                                print(f"\n✅ Installed {upgrade.name}!")
                                print(f"😊 Your happiness increased to {self.player.happiness}!")
                        else:
                            print(f"\n❌ Not enough gold! Need {upgrade.cost}g, have {self.player.gold}g")
                    else:
                        print("\n❌ Invalid choice!")
                except ValueError:
                    print("\n❌ Invalid input!")
            else:
                print("\n❌ Invalid choice!")
        except ValueError:
            print("\n❌ Invalid input!")
    
    def sell_property(self):
        """Sell a property"""
        if not self.player.properties:
            print("\n🏚️  You don't own any properties yet.")
            return
        
        print("\n💰 SELL PROPERTY 💰")
        print("Select a property to sell:")
        
        for i, prop in enumerate(self.player.properties, 1):
            sell_price = prop.get_price_in_gold() // 2
            print(f"{i}. {prop.name} - Sell for: {sell_price}g (50% of purchase price)")
        
        print("\n0. Back")
        
        choice = input("\nSelect property to sell: ").strip()
        
        if choice == "0":
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.properties):
                prop = self.player.properties[idx]
                sell_price = prop.get_price_in_gold() // 2
                
                confirm = input(f"\nSell {prop.name} for {sell_price}g? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.player.gold += sell_price
                    self.player.properties.pop(idx)
                    self.player.calculate_happiness()
                    print(f"\n✅ Sold {prop.name} for {sell_price}g!")
                    print(f"😊 Your happiness is now {self.player.happiness}")
            else:
                print("\n❌ Invalid choice!")
        except ValueError:
            print("\n❌ Invalid input!")
    
    def list_for_rent(self):
        """List a property for rent"""
        if not self.player.properties:
            print("\n🏚️  You don't own any properties yet.")
            return
        
        print("\n📋 LIST FOR RENT 📋")
        print("Select a property to list:")
        
        available = [p for p in self.player.properties if not p.is_rented and not p.listed_for_rent]
        
        if not available:
            print("\n❌ No available properties to list! (All are rented or already listed)")
            return
        
        for i, prop in enumerate(available, 1):
            print(f"{i}. {prop.name}")
        
        print("\n0. Back")
        
        choice = input("\nSelect property: ").strip()
        
        if choice == "0":
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available):
                prop = available[idx]
                suggested_rent = prop.get_price_in_gold() // 10
                
                rent_input = input(f"\nSet rent amount (suggested: {suggested_rent}g): ").strip()
                
                try:
                    rent = int(rent_input) if rent_input else suggested_rent
                    
                    if rent > 0:
                        prop.listed_for_rent = True
                        prop.rent_amount = rent
                        self.property_market.rental_listings.append({
                            'owner': self.player.name,
                            'property': prop,
                            'rent': rent
                        })
                        print(f"\n✅ Listed {prop.name} for {rent}g per period!")
                    else:
                        print("\n❌ Rent must be positive!")
                except ValueError:
                    print("\n❌ Invalid rent amount!")
            else:
                print("\n❌ Invalid choice!")
        except ValueError:
            print("\n❌ Invalid input!")
    
    def view_rental_listings(self):
        """View properties available for rent"""
        if not self.property_market.rental_listings:
            print("\n📋 No properties currently listed for rent.")
            return
        
        print("\n🏘️  RENTAL LISTINGS 🏘️")
        print(f"Your gold: {self.player.gold}")
        
        for i, listing in enumerate(self.property_market.rental_listings, 1):
            prop = listing['property']
            print(f"\n{i}. {prop.name} ({prop.property_type.capitalize()})")
            print(f"   Owner: {listing['owner']}")
            print(f"   Rent: {listing['rent']}g per period")
            print(f"   Happiness Bonus: +{prop.calculate_happiness_bonus()}")
        
        print("\n0. Back")
        
        choice = input("\nSelect property to rent (0 to go back): ").strip()
        
        if choice == "0":
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.property_market.rental_listings):
                listing = self.property_market.rental_listings[idx]
                prop = listing['property']
                rent = listing['rent']
                
                if listing['owner'] == self.player.name:
                    print("\n❌ You can't rent your own property!")
                    return
                
                if self.player.gold >= rent:
                    confirm = input(f"\nRent {prop.name} for {rent}g? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.player.gold -= rent
                        prop.is_rented = True
                        prop.rented_to = self.player.name
                        prop.listed_for_rent = False
                        self.property_market.rental_listings.pop(idx)
                        print(f"\n✅ You are now renting {prop.name}!")
                        print(f"💡 Note: Rental mechanics are simplified in this version.")
                else:
                    print(f"\n❌ Not enough gold! Need {rent}g, have {self.player.gold}g")
            else:
                print("\n❌ Invalid choice!")
        except ValueError:
            print("\n❌ Invalid input!")
    
    def save_game(self):
        """Save game to file"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.player.to_dict(), f, indent=2)
            print("\n💾 Game saved successfully!")
            # Update leaderboard
            self.update_leaderboard()
        except Exception as e:
            print(f"\n❌ Failed to save game: {e}")
    
    def load_game(self):
        """Load game from file"""
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
            
            self.player.name = data['name']
            self.player.health = data['health']
            self.player.max_health = data['max_health']
            self.player.mana = data['mana']
            self.player.max_mana = data['max_mana']
            self.player.energy = data['energy']
            self.player.max_energy = data['max_energy']
            self.player.gold = data['gold']
            self.player.experience = data['experience']
            self.player.level = data['level']
            self.player.last_energy_update = datetime.fromisoformat(data['last_energy_update'])
            
            # Load combat stats (with defaults for older save files)
            self.player.strength = data.get('strength', 0)
            self.player.agility = data.get('agility', 0)
            self.player.vitality = data.get('vitality', 0)
            
            # Load properties and happiness (with defaults for older save files)
            self.player.happiness = data.get('happiness', 0)
            self.player.max_happiness = data.get('max_happiness', 100)
            
            if 'properties' in data:
                for p_data in data['properties']:
                    prop = Property(
                        p_data['property_type'], p_data['name'], p_data['description'],
                        p_data['price_shillings'], p_data['price_pennies'],
                        p_data['size'], p_data['max_upgrades']
                    )
                    prop.is_rented = p_data.get('is_rented', False)
                    prop.rented_to = p_data.get('rented_to')
                    prop.rent_amount = p_data.get('rent_amount', 0)
                    prop.listed_for_rent = p_data.get('listed_for_rent', False)
                    
                    # Load upgrades
                    for u_data in p_data.get('upgrades', []):
                        upgrade = PropertyUpgrade(
                            u_data['name'], u_data['description'],
                            u_data['cost'], u_data['happiness_bonus']
                        )
                        prop.upgrades.append(upgrade)
                    
                    self.player.properties.append(prop)
            
            if data['weapon']:
                w = data['weapon']
                self.player.weapon = Weapon(w['name'], w['description'], w['price'], w['damage'], w.get('mana_cost', 0))
            
            if data['armor']:
                a = data['armor']
                self.player.armor = Armor(a['name'], a['description'], a['price'], a['defense'])
            
            print("\n📂 Game loaded successfully!")
            return True
        except FileNotFoundError:
            print("\n❌ No save file found!")
            return False
        except Exception as e:
            print(f"\n❌ Failed to load game: {e}")
            return False
    
    def update_leaderboard(self):
        """Update leaderboard with current player stats"""
        try:
            # Load existing leaderboard
            leaderboard = []
            try:
                with open(self.leaderboard_file, 'r') as f:
                    leaderboard = json.load(f)
            except FileNotFoundError:
                pass
            
            # Create player entry
            player_entry = {
                'name': self.player.name,
                'level': self.player.level,
                'experience': self.player.experience,
                'gold': self.player.gold,
                'max_health': self.player.max_health,
                'weapon': self.player.weapon.name if self.player.weapon else "None",
                'armor': self.player.armor.name if self.player.armor else "None"
            }
            
            # Update or add player to leaderboard
            updated = False
            for i, entry in enumerate(leaderboard):
                if entry['name'] == self.player.name:
                    leaderboard[i] = player_entry
                    updated = True
                    break
            
            if not updated:
                leaderboard.append(player_entry)
            
            # Save updated leaderboard
            with open(self.leaderboard_file, 'w') as f:
                json.dump(leaderboard, f, indent=2)
                
        except Exception as e:
            print(f"\n⚠️  Failed to update leaderboard: {e}")
    
    def display_leaderboard(self):
        """Display the leaderboard"""
        try:
            with open(self.leaderboard_file, 'r') as f:
                leaderboard = json.load(f)
            
            if not leaderboard:
                print("\n📊 Leaderboard is empty!")
                return
            
            # Sort by level (descending), then by experience (descending)
            leaderboard.sort(key=lambda x: (x['level'], x['experience']), reverse=True)
            
            print("\n" + "="*70)
            print("🏆 LEADERBOARD 🏆".center(70))
            print("="*70)
            print(f"{'Rank':<6} {'Name':<15} {'Level':<7} {'Exp':<10} {'Gold':<10} {'Weapon':<15}")
            print("-"*70)
            
            for i, entry in enumerate(leaderboard, 1):
                rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                print(f"{rank_icon:<6} {entry['name']:<15} {entry['level']:<7} {entry['experience']:<10} {entry['gold']:<10} {entry['weapon']:<15}")
            
            print("="*70)
            
        except FileNotFoundError:
            print("\n📊 Leaderboard is empty! Play the game and save to appear on the leaderboard.")
        except Exception as e:
            print(f"\n❌ Failed to load leaderboard: {e}")
    
    def main_menu(self):
        """Main game menu"""
        print("\n" + "="*50)
        print("🧙 HIGH WIZARDY 🧙")
        print("="*50)
        print("\nWelcome to High Wizardy!")
        print("\n1. New Game")
        print("2. Load Game")
        print("3. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            name = input("\nEnter your character name: ").strip()
            if name:
                self.player.name = name
            print(f"\nWelcome, {self.player.name}!")
        elif choice == "2":
            if not self.load_game():
                return False
        elif choice == "3":
            print("\nGoodbye!")
            exit(0)
        else:
            print("\n❌ Invalid choice!")
            return False
        
        return True
    
    def play(self):
        """Main game loop"""
        if not self.main_menu():
            return
        
        while True:
            self.display_status()
            print("\n--- MAIN MENU ---")
            print("1. Weapon Shop")
            print("2. Armor Shop")
            print("3. Combat (Costs 25 Energy)")
            print("4. Rest")
            print("5. Training Gym")
            print("6. Property Market")
            print("7. View Leaderboard")
            print("8. Save Game")
            print("9. Exit")
            
            choice = input("\nWhat would you like to do? ").strip()
            
            if choice == "1":
                self.weapon_shop()
            elif choice == "2":
                self.armor_shop()
            elif choice == "3":
                self.combat()
            elif choice == "4":
                self.rest()
            elif choice == "5":
                self.gym()
            elif choice == "6":
                self.property_menu()
            elif choice == "7":
                self.display_leaderboard()
            elif choice == "8":
                self.save_game()
            elif choice == "9":
                print("\n👋 Thanks for playing High Wizardy!")
                save = input("Save game before exit? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_game()
                break
            else:
                print("\n❌ Invalid choice!")


if __name__ == "__main__":
    game = Game()
    game.play()
