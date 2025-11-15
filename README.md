# High-wizardy
My game project welcome to join and play :)

## 🎮 Game Features

High Wizardy is a text-based RPG with an exciting combat system!

### Features:
- **Combat System**: Engage in turn-based combat with various enemies
- **Combat Stats**: Train strength, agility, and vitality at the gym to become stronger
- **Training Gym**: Improve your combat stats by spending gold on training
- **Energy System**: 100 max energy that regenerates 5 points every 15 minutes
- **Combat Costs**: Each combat encounter costs 25 energy
- **Weapon Shop**: Buy and equip powerful weapons with various stats
- **Armor Shop**: Purchase armor to defend yourself in battle
- **Mana System**: Use mana for magical attacks
- **Experience & Leveling**: Gain experience and level up to become stronger
- **Leaderboard**: Compete with other players and see your ranking
- **Save/Load**: Save your progress and continue later

## 🚀 How to Play

1. Run the game:
   ```bash
   python3 game.py
   ```

2. Choose to start a new game or load a saved game

3. Main Menu Options:
   - **Weapon Shop**: Buy weapons to increase your attack damage
   - **Armor Shop**: Buy armor to reduce damage taken
   - **Combat**: Fight enemies to gain gold and experience (costs 25 energy)
   - **Rest**: Restore 50 health and 50 mana
   - **Training Gym**: Train combat stats (strength, agility, vitality) for gold
   - **View Leaderboard**: See rankings of all players
   - **Save Game**: Save your progress
   - **Exit**: Quit the game

## ⚔️ Combat System

- Combat requires **25 energy** per encounter
- Energy regenerates **5 points every 15 minutes** (up to 100 max)
- Choose between regular attacks or magical attacks (if your weapon supports magic)
- Defeat enemies to earn gold and experience
- Level up to increase your max health, mana, and energy!

## 🛡️ Equipment

### Weapons
- Wooden Sword (50g, 5 damage)
- Iron Sword (150g, 15 damage)
- Steel Sword (300g, 30 damage)
- Fire Staff (400g, 40 damage, magic)
- Legendary Blade (1000g, 80 damage, magic)

### Armor
- Leather Armor (60g, 5 defense)
- Iron Armor (180g, 15 defense)
- Steel Armor (350g, 30 defense)
- Enchanted Robes (500g, 40 defense)
- Dragon Scale Armor (1200g, 70 defense)

## 📊 Stats

- **Health**: Your life points
- **Mana**: Used for magical attacks
- **Energy**: Required to initiate combat
- **Gold**: Currency for buying equipment and training
- **Experience**: Gain to level up and become stronger

### Combat Stats
- **Strength (STR)**: Increases attack damage by +3 per point
- **Agility (AGI)**: Increases dodge chance by +2% per point (capped at 50%)
- **Vitality (VIT)**: Increases defense by +2 per point

## 💪 Training Gym

Visit the gym to train your combat stats:
- **Train Strength**: 50 gold for +1 STR (adds +3 damage)
- **Train Agility**: 50 gold for +1 AGI (adds +2% dodge chance)
- **Train Vitality**: 50 gold for +1 VIT (adds +2 defense)
- **Intensive Training**: 200 gold for +2 to all stats

Combat stats stack with weapon damage and armor defense, making training a valuable investment!

**Dodge Mechanics**: When enemies attack, agility gives you a chance to completely avoid damage. Each point of agility provides 2% dodge chance, capped at 50% (25 AGI).

## 🏆 Leaderboard

The leaderboard tracks all players who have saved their game:
- Players are ranked by level, then by experience points
- Top 3 players receive special medals (🥇🥈🥉)
- Displays player stats including level, experience, gold, and equipped weapon
- Updates automatically when you save your game

Enjoy your adventure in High Wizardy! 🧙✨
