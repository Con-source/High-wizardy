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
            'vitality': self.vitality
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
        print("="*50)
    
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
            print(f"\nCurrent Combat Stats:")
            print(f"  Strength: {self.player.strength} (+{self.player.strength * 3} damage)")
            dodge_chance = min(self.player.agility * 2, 50)
            print(f"  Agility: {self.player.agility} ({dodge_chance}% dodge chance)")
            print(f"  Vitality: {self.player.vitality} (+{self.player.vitality * 2} defense)")
            
            print("\n--- Training Options ---")
            print("1. Train Strength (50 gold, +1 STR)")
            print("2. Train Agility (50 gold, +1 AGI)")
            print("3. Train Vitality (50 gold, +1 VIT)")
            print("4. Intensive Training (200 gold, +2 to all stats)")
            print("0. Back to main menu")
            
            choice = input("\nWhat would you like to train? ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                if self.player.gold >= 50:
                    self.player.gold -= 50
                    self.player.strength += 1
                    print(f"\n💪 Strength training complete! STR: {self.player.strength}")
                else:
                    print("\n❌ Not enough gold! Need 50 gold.")
            elif choice == "2":
                if self.player.gold >= 50:
                    self.player.gold -= 50
                    self.player.agility += 1
                    print(f"\n🏃 Agility training complete! AGI: {self.player.agility}")
                else:
                    print("\n❌ Not enough gold! Need 50 gold.")
            elif choice == "3":
                if self.player.gold >= 50:
                    self.player.gold -= 50
                    self.player.vitality += 1
                    print(f"\n🛡️  Vitality training complete! VIT: {self.player.vitality}")
                else:
                    print("\n❌ Not enough gold! Need 50 gold.")
            elif choice == "4":
                if self.player.gold >= 200:
                    self.player.gold -= 200
                    self.player.strength += 2
                    self.player.agility += 2
                    self.player.vitality += 2
                    print(f"\n🌟 Intensive training complete!")
                    print(f"STR: {self.player.strength}, AGI: {self.player.agility}, VIT: {self.player.vitality}")
                else:
                    print("\n❌ Not enough gold! Need 200 gold.")
            else:
                print("\n❌ Invalid choice!")
    
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
            print("6. View Leaderboard")
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
                self.rest()
            elif choice == "5":
                self.gym()
            elif choice == "6":
                self.display_leaderboard()
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
