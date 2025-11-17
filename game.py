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
    """Property upgrade that adds happiness"""
    def __init__(self, name: str, description: str, price: int, happiness_boost: int):
        self.name = name
        self.description = description
        self.price = price
        self.happiness_boost = happiness_boost
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'happiness_boost': self.happiness_boost
        }


class Property:
    """Property that can be owned, upgraded, and traded"""
    def __init__(self, name: str, description: str, base_price: int):
        self.name = name
        self.description = description
        self.base_price = base_price
        self.upgrades: List[PropertyUpgrade] = []
        self.owner: Optional[str] = None
        self.for_sale = False
        self.sale_price = 0
        self.for_rent = False
        self.rent_price = 0
        self.renter: Optional[str] = None
    
    def get_total_happiness(self) -> int:
        """Calculate total happiness from all upgrades"""
        return sum(upgrade.happiness_boost for upgrade in self.upgrades)
    
    def get_total_value(self) -> int:
        """Calculate total value including upgrades"""
        upgrade_value = sum(upgrade.price for upgrade in self.upgrades)
        return self.base_price + upgrade_value
    
    def add_upgrade(self, upgrade: PropertyUpgrade):
        """Add an upgrade to the property"""
        self.upgrades.append(upgrade)
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'base_price': self.base_price,
            'upgrades': [u.to_dict() for u in self.upgrades],
            'owner': self.owner,
            'for_sale': self.for_sale,
            'sale_price': self.sale_price,
            'for_rent': self.for_rent,
            'rent_price': self.rent_price,
            'renter': self.renter
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
        # Currency: 1 Shilling = 12 Pennies
        self.shillings = 8  # Starting with 8 shillings, 4 pennies (equivalent to 100 pennies)
        self.pennies = 4
        self.weapon: Optional[Weapon] = None
        self.armor: Optional[Armor] = None
        self.inventory: List[Item] = []
        self.last_energy_update = datetime.now()
        self.experience = 0
        self.level = 1
        # Property and happiness system
        self.properties: List['Property'] = []
        self.happiness = 0
        self.max_happiness = 100
    
    def add_currency(self, shillings: int = 0, pennies: int = 0):
        """Add currency and handle conversion (12 pennies = 1 shilling)"""
        self.pennies += pennies
        self.shillings += shillings
        
        # Convert excess pennies to shillings
        if self.pennies >= 12:
            extra_shillings = self.pennies // 12
            self.shillings += extra_shillings
            self.pennies = self.pennies % 12
    
    def remove_currency(self, shillings: int = 0, pennies: int = 0) -> bool:
        """Remove currency if available, return True if successful"""
        # Convert to total pennies for comparison
        total_needed = shillings * 12 + pennies
        total_have = self.shillings * 12 + self.pennies
        
        if total_have >= total_needed:
            # Remove the currency
            self.shillings -= shillings
            self.pennies -= pennies
            
            # Handle negative pennies
            while self.pennies < 0:
                self.shillings -= 1
                self.pennies += 12
            
            return True
        return False
    
    def get_total_pennies(self) -> int:
        """Get total currency in pennies"""
        return self.shillings * 12 + self.pennies
    
    def format_currency(self, shillings: int = None, pennies: int = None) -> str:
        """Format currency for display"""
        if shillings is None and pennies is None:
            shillings = self.shillings
            pennies = self.pennies
        elif pennies is None:
            pennies = 0
        elif shillings is None:
            shillings = 0

        if shillings == 0 and pennies == 0:
            return "0s 0d"
        elif shillings > 0 and pennies > 0:
            return f"{shillings}s {pennies}d"
        elif shillings > 0:
            return f"{shillings}s"
        else:
            return f"{pennies}d"
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
    
    def take_damage(self, damage: int) -> int:
        """Take damage, reduced by armor"""
        defense = self.armor.defense if self.armor else 0
        actual_damage = max(1, damage - defense)
        self.health = max(0, self.health - actual_damage)
        return actual_damage
    
    def attack_damage(self) -> int:
        """Calculate attack damage"""
        base_damage = 10
        weapon_damage = self.weapon.damage if self.weapon else 0
        return base_damage + weapon_damage
    
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
    
    def update_happiness(self):
        """Update happiness based on owned properties"""
        self.happiness = 0
        for prop in self.properties:
            self.happiness += prop.get_total_happiness()
        self.happiness = min(self.max_happiness, self.happiness)
    
    def get_happiness_bonus(self) -> float:
        """Get gym stat bonus multiplier based on happiness (1.0 to 1.5)"""
        return 1.0 + (self.happiness / self.max_happiness) * 0.5
    
    def train_at_gym(self, stat: str) -> bool:
        """Train at gym to improve stats, requires energy"""
        cost = 15  # Energy cost for gym training
        if not self.use_energy(cost):
            return False
        
        bonus = self.get_happiness_bonus()
        
        if stat == "health":
            gain = int(10 * bonus)
            self.max_health += gain
            print(f"\n💪 Health training complete! Max Health +{gain} (Happiness Bonus: {bonus:.2f}x)")
        elif stat == "mana":
            gain = int(5 * bonus)
            self.max_mana += gain
            print(f"\n🔮 Mana training complete! Max Mana +{gain} (Happiness Bonus: {bonus:.2f}x)")
        elif stat == "energy":
            gain = int(5 * bonus)
            self.max_energy += gain
            print(f"\n⚡ Energy training complete! Max Energy +{gain} (Happiness Bonus: {bonus:.2f}x)")
        
        return True
    
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
            'shillings': self.shillings,
            'pennies': self.pennies,
            'weapon': self.weapon.to_dict() if self.weapon else None,
            'armor': self.armor.to_dict() if self.armor else None,
            'last_energy_update': self.last_energy_update.isoformat(),
            'experience': self.experience,
            'level': self.level,
            'happiness': self.happiness,
            'max_happiness': self.max_happiness,
            'properties': [prop.to_dict() for prop in self.properties]
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


class Game:
    """Main game class"""
    def __init__(self):
        self.player = Player()
        self.shop = Shop()
        self.save_file = "savegame.json"
    
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
        print(f"💰 Currency: {self.player.format_currency()}")
        print(f"😊 Happiness: {self.player.happiness}/{self.player.max_happiness} (Gym Bonus: {self.player.get_happiness_bonus():.2f}x)")
        print(f"⭐ Experience: {self.player.experience}/{self.player.level * 100}")
        
        if self.player.weapon:
            print(f"⚔️  Weapon: {self.player.weapon.name} (Damage: {self.player.weapon.damage})")
        else:
            print("⚔️  Weapon: None (Fists)")
        
        if self.player.armor:
            print(f"🛡️  Armor: {self.player.armor.name} (Defense: {self.player.armor.defense})")
        else:
            print("🛡️  Armor: None")
        
        if self.player.properties:
            print(f"🏠 Properties: {len(self.player.properties)}")
        
        print("="*50)
    
    def weapon_shop(self):
        """Weapon shop menu"""
        while True:
            print("\n🗡️  WEAPON SHOP 🗡️")
            print(f"Your currency: {self.player.format_currency()}")
            print("\nAvailable Weapons:")
            for i, weapon in enumerate(self.shop.weapons, 1):
                mana_info = f", Mana: {weapon.mana_cost}" if weapon.mana_cost > 0 else ""
                # Convert price to shillings and pennies
                shillings = weapon.price // 12
                pennies = weapon.price % 12
                price_str = f"{shillings}s {pennies}d" if pennies > 0 else f"{shillings}s"
                print(f"{i}. {weapon.name} - {price_str} (Damage: {weapon.damage}{mana_info})")
                print(f"   {weapon.description}")
            
            print("\n0. Back to main menu")
            
            choice = input("\nSelect weapon to buy (0 to exit): ").strip()
            
            if choice == "0":
                break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.shop.weapons):
                    weapon = self.shop.weapons[idx]
                    weapon_shillings = weapon.price // 12
                    weapon_pennies = weapon.price % 12
                    
                    if self.player.get_total_pennies() >= weapon.price:
                        self.player.remove_currency(weapon_shillings, weapon_pennies)
                        old_weapon = self.player.weapon
                        self.player.equip_weapon(weapon)
                        print(f"\n✅ Purchased and equipped {weapon.name}!")
                        if old_weapon:
                            # Sell old weapon for half price
                            refund_total = old_weapon.price // 2
                            refund_shillings = refund_total // 12
                            refund_pennies = refund_total % 12
                            self.player.add_currency(refund_shillings, refund_pennies)
                            refund_str = f"{refund_shillings}s {refund_pennies}d" if refund_pennies > 0 else f"{refund_shillings}s"
                            print(f"💰 Sold old weapon for {refund_str}")
                    else:
                        need_str = f"{weapon_shillings}s {weapon_pennies}d" if weapon_pennies > 0 else f"{weapon_shillings}s"
                        print(f"\n❌ Not enough currency! Need {need_str}, have {self.player.format_currency()}")
                else:
                    print("\n❌ Invalid choice!")
            except ValueError:
                print("\n❌ Invalid input!")
    
    def armor_shop(self):
        """Armor shop menu"""
        while True:
            print("\n🛡️  ARMOR SHOP 🛡️")
            print(f"Your currency: {self.player.format_currency()}")
            print("\nAvailable Armor:")
            for i, armor in enumerate(self.shop.armors, 1):
                # Convert price to shillings and pennies
                shillings = armor.price // 12
                pennies = armor.price % 12
                price_str = f"{shillings}s {pennies}d" if pennies > 0 else f"{shillings}s"
                print(f"{i}. {armor.name} - {price_str} (Defense: {armor.defense})")
                print(f"   {armor.description}")
            
            print("\n0. Back to main menu")
            
            choice = input("\nSelect armor to buy (0 to exit): ").strip()
            
            if choice == "0":
                break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.shop.armors):
                    armor = self.shop.armors[idx]
                    armor_shillings = armor.price // 12
                    armor_pennies = armor.price % 12
                    
                    if self.player.get_total_pennies() >= armor.price:
                        self.player.remove_currency(armor_shillings, armor_pennies)
                        old_armor = self.player.armor
                        self.player.equip_armor(armor)
                        print(f"\n✅ Purchased and equipped {armor.name}!")
                        if old_armor:
                            # Sell old armor for half price
                            refund_total = old_armor.price // 2
                            refund_shillings = refund_total // 12
                            refund_pennies = refund_total % 12
                            self.player.add_currency(refund_shillings, refund_pennies)
                            refund_str = f"{refund_shillings}s {refund_pennies}d" if refund_pennies > 0 else f"{refund_shillings}s"
                            print(f"💰 Sold old armor for {refund_str}")
                    else:
                        need_str = f"{armor_shillings}s {armor_pennies}d" if armor_pennies > 0 else f"{armor_shillings}s"
                        print(f"\n❌ Not enough currency! Need {need_str}, have {self.player.format_currency()}")
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
                reward_shillings = enemy.gold_reward // 12
                reward_pennies = enemy.gold_reward % 12
                self.player.add_currency(reward_shillings, reward_pennies)
                self.player.gain_experience(enemy.exp_reward)
                reward_str = f"{reward_shillings}s {reward_pennies}d" if reward_pennies > 0 else f"{reward_shillings}s"
                print(f"💰 Gained {reward_str}")
                print(f"⭐ Gained {enemy.exp_reward} experience")
                return
            
            # Enemy attacks
            damage = enemy.damage
            actual_damage = self.player.take_damage(damage)
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
    
    def gym_menu(self):
        """Gym menu for training stats"""
        while True:
            print("\n💪 GYM TRAINING 💪")
            print(f"Your energy: {self.player.energy}/{self.player.max_energy}")
            print(f"Happiness Bonus: {self.player.get_happiness_bonus():.2f}x")
            print("\nTraining Options (Costs 15 Energy):")
            print("1. Health Training (+10 Max Health per session)")
            print("2. Mana Training (+5 Max Mana per session)")
            print("3. Energy Training (+5 Max Energy per session)")
            print("\n0. Back to main menu")
            
            choice = input("\nSelect training (0 to exit): ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                if self.player.train_at_gym("health"):
                    print("✅ Training complete!")
                else:
                    print(f"\n❌ Not enough energy! Need 15 energy, have {self.player.energy}")
            elif choice == "2":
                if self.player.train_at_gym("mana"):
                    print("✅ Training complete!")
                else:
                    print(f"\n❌ Not enough energy! Need 15 energy, have {self.player.energy}")
            elif choice == "3":
                if self.player.train_at_gym("energy"):
                    print("✅ Training complete!")
                else:
                    print(f"\n❌ Not enough energy! Need 15 energy, have {self.player.energy}")
            else:
                print("\n❌ Invalid choice!")
    
    def property_menu(self):
        """Property management menu"""
        while True:
            print("\n🏠 PROPERTY MANAGEMENT 🏠")
            print(f"\nYour Properties: {len(self.player.properties)}")
            print(f"Total Happiness: {self.player.happiness}/{self.player.max_happiness}")
            
            if self.player.properties:
                for i, prop in enumerate(self.player.properties, 1):
                    print(f"\n{i}. {prop.name}")
                    print(f"   {prop.description}")
                    print(f"   Happiness: +{prop.get_total_happiness()}")
                    print(f"   Upgrades: {len(prop.upgrades)}")
                    if prop.for_sale:
                        sale_s = prop.sale_price // 12
                        sale_p = prop.sale_price % 12
                        print(f"   🏷️  FOR SALE: {sale_s}s {sale_p}d" if sale_p > 0 else f"   🏷️  FOR SALE: {sale_s}s")
                    if prop.for_rent:
                        rent_s = prop.rent_price // 12
                        rent_p = prop.rent_price % 12
                        print(f"   🏷️  FOR RENT: {rent_s}s {rent_p}d" if rent_p > 0 else f"   🏷️  FOR RENT: {rent_s}s")
            
            print("\n--- Options ---")
            print("1. Buy Property")
            print("2. Upgrade Property")
            print("3. List Property for Sale")
            print("4. List Property for Rent")
            print("5. Browse Marketplace")
            print("0. Back to main menu")
            
            choice = input("\nSelect option (0 to exit): ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self.buy_property()
            elif choice == "2":
                self.upgrade_property()
            elif choice == "3":
                self.list_property_for_sale()
            elif choice == "4":
                self.list_property_for_rent()
            elif choice == "5":
                self.property_marketplace()
            else:
                print("\n❌ Invalid choice!")
    
    def buy_property(self):
        """Buy a new property"""
        available_properties = [
            Property("Cottage", "A small cozy cottage", 600),
            Property("Town House", "A comfortable house in town", 1200),
            Property("Manor", "A grand manor with gardens", 2400),
            Property("Castle", "A magnificent castle", 4800),
        ]
        
        print("\n🏠 Available Properties:")
        for i, prop in enumerate(available_properties, 1):
            price_s = prop.base_price // 12
            price_p = prop.base_price % 12
            price_str = f"{price_s}s {price_p}d" if price_p > 0 else f"{price_s}s"
            print(f"{i}. {prop.name} - {price_str}")
            print(f"   {prop.description}")
        
        choice = input("\nSelect property to buy (0 to cancel): ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available_properties):
                prop = available_properties[idx]
                if self.player.get_total_pennies() >= prop.base_price:
                    price_s = prop.base_price // 12
                    price_p = prop.base_price % 12
                    self.player.remove_currency(price_s, price_p)
                    prop.owner = self.player.name
                    self.player.properties.append(prop)
                    self.player.update_happiness()
                    print(f"\n✅ Purchased {prop.name}!")
                else:
                    price_s = prop.base_price // 12
                    price_p = prop.base_price % 12
                    need_str = f"{price_s}s {price_p}d" if price_p > 0 else f"{price_s}s"
                    print(f"\n❌ Not enough currency! Need {need_str}, have {self.player.format_currency()}")
        except (ValueError, IndexError):
            print("\n❌ Invalid input!")
    
    def upgrade_property(self):
        """Upgrade a property"""
        if not self.player.properties:
            print("\n❌ You don't own any properties!")
            return
        
        print("\n🏠 Your Properties:")
        for i, prop in enumerate(self.player.properties, 1):
            print(f"{i}. {prop.name} (Upgrades: {len(prop.upgrades)})")
        
        choice = input("\nSelect property to upgrade (0 to cancel): ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.properties):
                prop = self.player.properties[idx]
                
                available_upgrades = [
                    PropertyUpgrade("Garden", "A beautiful garden", 240, 5),
                    PropertyUpgrade("Library", "A cozy library", 360, 8),
                    PropertyUpgrade("Workshop", "A crafting workshop", 480, 10),
                    PropertyUpgrade("Enchanted Fountain", "A magical fountain", 720, 15),
                    PropertyUpgrade("Observatory", "An astronomical observatory", 960, 20),
                ]
                
                print(f"\n🔧 Available Upgrades for {prop.name}:")
                for i, upgrade in enumerate(available_upgrades, 1):
                    price_s = upgrade.price // 12
                    price_p = upgrade.price % 12
                    price_str = f"{price_s}s {price_p}d" if price_p > 0 else f"{price_s}s"
                    print(f"{i}. {upgrade.name} - {price_str} (+{upgrade.happiness_boost} happiness)")
                    print(f"   {upgrade.description}")
                
                upgrade_choice = input("\nSelect upgrade (0 to cancel): ").strip()
                upgrade_idx = int(upgrade_choice) - 1
                
                if 0 <= upgrade_idx < len(available_upgrades):
                    upgrade = available_upgrades[upgrade_idx]
                    if self.player.get_total_pennies() >= upgrade.price:
                        price_s = upgrade.price // 12
                        price_p = upgrade.price % 12
                        self.player.remove_currency(price_s, price_p)
                        prop.add_upgrade(upgrade)
                        self.player.update_happiness()
                        print(f"\n✅ Added {upgrade.name} to {prop.name}!")
                        print(f"😊 Happiness is now {self.player.happiness}/{self.player.max_happiness}")
                    else:
                        price_s = upgrade.price // 12
                        price_p = upgrade.price % 12
                        need_str = f"{price_s}s {price_p}d" if price_p > 0 else f"{price_s}s"
                        print(f"\n❌ Not enough currency! Need {need_str}, have {self.player.format_currency()}")
        except (ValueError, IndexError):
            print("\n❌ Invalid input!")
    
    def list_property_for_sale(self):
        """List a property for sale"""
        if not self.player.properties:
            print("\n❌ You don't own any properties!")
            return
        
        print("\n🏠 Your Properties:")
        for i, prop in enumerate(self.player.properties, 1):
            status = ""
            if prop.for_sale:
                status = " [Already for sale]"
            elif prop.for_rent:
                status = " [Listed for rent]"
            print(f"{i}. {prop.name} (Value: ~{prop.get_total_value()} pennies){status}")
        
        choice = input("\nSelect property to list for sale (0 to cancel): ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.properties):
                prop = self.player.properties[idx]
                suggested_price = int(prop.get_total_value() * 1.2)
                sugg_s = suggested_price // 12
                sugg_p = suggested_price % 12
                print(f"\nSuggested price: {sugg_s}s {sugg_p}d" if sugg_p > 0 else f"\nSuggested price: {sugg_s}s")
                
                price_input = input("Enter sale price in shillings (0 to cancel): ").strip()
                price_shillings = int(price_input)
                
                if price_shillings > 0:
                    prop.for_sale = True
                    prop.sale_price = price_shillings * 12
                    prop.for_rent = False  # Can't be both
                    print(f"\n✅ {prop.name} is now listed for sale at {price_shillings}s!")
        except (ValueError, IndexError):
            print("\n❌ Invalid input!")
    
    def list_property_for_rent(self):
        """List a property for rent"""
        if not self.player.properties:
            print("\n❌ You don't own any properties!")
            return
        
        print("\n🏠 Your Properties:")
        for i, prop in enumerate(self.player.properties, 1):
            status = ""
            if prop.for_rent:
                status = " [Already for rent]"
            elif prop.for_sale:
                status = " [Listed for sale]"
            print(f"{i}. {prop.name}{status}")
        
        choice = input("\nSelect property to list for rent (0 to cancel): ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.properties):
                prop = self.player.properties[idx]
                suggested_rent = int(prop.get_total_value() * 0.1)
                sugg_s = suggested_rent // 12
                sugg_p = suggested_rent % 12
                print(f"\nSuggested rent: {sugg_s}s {sugg_p}d" if sugg_p > 0 else f"\nSuggested rent: {sugg_s}s")
                
                rent_input = input("Enter rent price in shillings (0 to cancel): ").strip()
                rent_shillings = int(rent_input)
                
                if rent_shillings > 0:
                    prop.for_rent = True
                    prop.rent_price = rent_shillings * 12
                    prop.for_sale = False  # Can't be both
                    print(f"\n✅ {prop.name} is now listed for rent at {rent_shillings}s!")
        except (ValueError, IndexError):
            print("\n❌ Invalid input!")
    
    def property_marketplace(self):
        """Browse and purchase/rent properties from marketplace"""
        # In a real multiplayer game, this would fetch from a server
        # For now, we'll simulate with properties listed by players
        print("\n🏪 PROPERTY MARKETPLACE 🏪")
        print("\n(In multiplayer, you would see other players' properties here)")
        print("For now, this is a placeholder for the marketplace system.")
        print("\nFeatures to be implemented in multiplayer:")
        print("- View all properties listed by other players")
        print("- Buy properties that are for sale")
        print("- Rent properties from other players")
        print("- Search and filter properties")
        input("\nPress Enter to continue...")
    
    def save_game(self):
        """Save game to file"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.player.to_dict(), f, indent=2)
            print("\n💾 Game saved successfully!")
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
            
            # Handle currency - backward compatibility with old gold system
            if 'shillings' in data and 'pennies' in data:
                self.player.shillings = data['shillings']
                self.player.pennies = data['pennies']
            elif 'gold' in data:
                # Convert old gold to new currency (1 gold = 1 penny)
                total_pennies = data['gold']
                self.player.shillings = total_pennies // 12
                self.player.pennies = total_pennies % 12
            
            self.player.experience = data['experience']
            self.player.level = data['level']
            self.player.last_energy_update = datetime.fromisoformat(data['last_energy_update'])
            
            # Load happiness system
            self.player.happiness = data.get('happiness', 0)
            self.player.max_happiness = data.get('max_happiness', 100)
            
            if data['weapon']:
                w = data['weapon']
                self.player.weapon = Weapon(w['name'], w['description'], w['price'], w['damage'], w.get('mana_cost', 0))
            
            if data['armor']:
                a = data['armor']
                self.player.armor = Armor(a['name'], a['description'], a['price'], a['defense'])
            
            # Load properties
            self.player.properties = []
            if 'properties' in data:
                for prop_data in data['properties']:
                    prop = Property(prop_data['name'], prop_data['description'], prop_data['base_price'])
                    prop.owner = prop_data.get('owner')
                    prop.for_sale = prop_data.get('for_sale', False)
                    prop.sale_price = prop_data.get('sale_price', 0)
                    prop.for_rent = prop_data.get('for_rent', False)
                    prop.rent_price = prop_data.get('rent_price', 0)
                    prop.renter = prop_data.get('renter')
                    
                    for upgrade_data in prop_data.get('upgrades', []):
                        upgrade = PropertyUpgrade(
                            upgrade_data['name'],
                            upgrade_data['description'],
                            upgrade_data['price'],
                            upgrade_data['happiness_boost']
                        )
                        prop.add_upgrade(upgrade)
                    
                    self.player.properties.append(prop)
            
            self.player.update_happiness()
            
            print("\n📂 Game loaded successfully!")
            return True
        except FileNotFoundError:
            print("\n❌ No save file found!")
            return False
        except Exception as e:
            print(f"\n❌ Failed to load game: {e}")
            return False
    
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
            print("4. Gym Training (Costs 15 Energy)")
            print("5. Property Management")
            print("6. Rest")
            print("7. Save Game")
            print("8. Exit")
            
            choice = input("\nWhat would you like to do? ").strip()
            
            if choice == "1":
                self.weapon_shop()
            elif choice == "2":
                self.armor_shop()
            elif choice == "3":
                self.combat()
            elif choice == "4":
                self.gym_menu()
            elif choice == "5":
                self.property_menu()
            elif choice == "6":
                self.rest()
            elif choice == "7":
                self.save_game()
            elif choice == "8":
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
