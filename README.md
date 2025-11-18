# High-wizardy
My game project welcome to join and play :)

## 🎮 Game Features

High Wizardy is a text-based RPG with an exciting combat system and property management!

### Features:
- **Combat System**: Engage in turn-based combat with various enemies
- **Combat Stats**: Train strength, agility, and vitality at the gym to become stronger
- **Training Gym**: Improve your combat stats by spending gold on training
- **Property System**: Buy, upgrade, and rent properties to increase happiness
- **Happiness System**: Property ownership boosts happiness, providing training bonuses
- **Energy System**: 100 max energy that regenerates 5 points every 15 minutes
- **Combat Costs**: Each combat encounter costs 25 energy
- **Currency System**: Trade using Shillings (s) and Pennies (d) - 12 pennies = 1 shilling
- **Weapon Shop**: Buy and equip powerful weapons with various stats
- **Armor Shop**: Purchase armor to defend yourself in battle
- **Gym Training**: Train your stats with energy (costs 15 energy per session)
- **Property System**: Buy properties, upgrade them, and increase your happiness
- **Happiness Bar**: Higher happiness provides better gym stat bonuses (up to 1.5x)
- **Property Marketplace**: Buy, sell, and rent properties (multiplayer ready)
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
   - **Combat**: Fight enemies to gain currency and experience (costs 25 energy)
   - **Gym Training**: Train to increase your max stats (costs 15 energy)
   - **Property Management**: Buy properties, upgrade them, and manage rentals
   - **Rest**: Restore 50 health and 50 mana
   - **Training Gym**: Train combat stats (strength, agility, vitality) for gold
   - **Property Market**: Buy, upgrade, and rent properties to boost happiness
   - **View Leaderboard**: See rankings of all players
   - **Save Game**: Save your progress
   - **Exit**: Quit the game

## ⚔️ Combat System

- Combat requires **25 energy** per encounter
- Energy regenerates **5 points every 15 minutes** (up to 100 max)
- Choose between regular attacks or magical attacks (if your weapon supports magic)
- Defeat enemies to earn currency and experience
- Level up to increase your max health, mana, and energy!

## 💪 Gym Training System

- Train at the gym to increase your max stats (costs **15 energy** per session)
- Train Health, Mana, or Energy
- Higher happiness provides **better gym bonuses** (up to 1.5x multiplier)
- Stat gains depend on your happiness level from properties

## 🏠 Property System

- Buy properties to increase your happiness
- Upgrade properties with various improvements (Gardens, Libraries, Workshops, etc.)
- Each upgrade adds to your Happiness Bar
- Higher happiness = better gym training bonuses
- List properties for sale or rent in the marketplace
- Property marketplace ready for multiplayer trading

## 💰 Currency System

- Game uses **Shillings (s)** and **Pennies (d)**
- **12 pennies = 1 shilling**
- All transactions display prices in this format
- Earn currency by defeating enemies in combat

## 🛡️ Equipment

### Weapons
- Wooden Sword (4s 2d, 5 damage)
- Iron Sword (12s 6d, 15 damage)
- Steel Sword (25s, 30 damage)
- Fire Staff (33s 4d, 40 damage, magic)
- Legendary Blade (83s 4d, 80 damage, magic)

### Armor
- Leather Armor (5s, 5 defense)
- Iron Armor (15s, 15 defense)
- Steel Armor (29s 2d, 30 defense)
- Enchanted Robes (41s 8d, 40 defense)
- Dragon Scale Armor (100s, 70 defense)

### Properties
- Cottage (50s) - A small cozy cottage
- Town House (100s) - A comfortable house in town
- Manor (200s) - A grand manor with gardens
- Castle (400s) - A magnificent castle

### Property Upgrades
- Garden (20s) - +5 happiness
- Library (30s) - +8 happiness
- Workshop (40s) - +10 happiness
- Enchanted Fountain (60s) - +15 happiness
- Observatory (80s) - +20 happiness

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

## 🏠 Property System

Invest in properties to increase your happiness and gain training bonuses!

### Property Types
- **Cottage**: Small, affordable starter homes (50-75s + pennies)
  - Size: 100-120 sq ft
  - Max Upgrades: 2
  - Base Happiness: +10
  
- **Manor**: Spacious mid-tier properties (200-250s)
  - Size: 300-350 sq ft
  - Max Upgrades: 4
  - Base Happiness: +25
  
- **Castle**: Grand estates for the wealthy (500-1000s)
  - Size: 800-1200 sq ft
  - Max Upgrades: 6-8
  - Base Happiness: +50

### Property Upgrades
Each property can be upgraded with various improvements:

**Cottage Upgrades:**
- Small Garden (20g, +5 happiness)
- Bookshelf (25g, +5 happiness)

**Manor Upgrades:**
- Library (50g, +10 happiness)
- Training Room (60g, +10 happiness)
- Garden (40g, +8 happiness)
- Workshop (55g, +9 happiness)

**Castle Upgrades:**
- Grand Library (100g, +15 happiness)
- Full Gymnasium (120g, +15 happiness)
- Royal Garden (90g, +12 happiness)
- Armory (110g, +13 happiness)
- Chapel (80g, +11 happiness)
- Observatory (95g, +12 happiness)

### Property Actions
- **Buy Properties**: Purchase properties from the market
- **View Properties**: See all your owned properties and their status
- **Upgrade Properties**: Add improvements to increase happiness
- **Sell Properties**: Sell properties for 50% of purchase price
- **List for Rent**: Put properties on the rental market
- **Rent Properties**: Rent properties from other players

### Currency System
Properties use shillings (s) and pennies (p):
- 1 shilling = 12 pennies
- Prices are simplified to gold for gameplay balance

## 😊 Happiness System

Happiness is gained from owning and upgrading properties!

### Happiness Benefits
- **Training Bonus**: Happiness boosts stat gains at the gym
  - 0 happiness = 1.0x training (normal gains)
  - 50 happiness = 1.25x training 
  - 100 happiness = 1.5x training (maximum bonus)
  
### How to Increase Happiness
1. **Buy Properties**: Each property provides base happiness
2. **Upgrade Properties**: Add improvements for additional happiness
3. **Own Multiple Properties**: Happiness stacks from all properties

### Happiness Bar
The happiness bar shows visually in your status:
```
😊 Happiness: ████████████░░░░░░░░ 60/100 (x1.30 training bonus)
```

### Example Training with Happiness
- At 0 happiness: Train Strength (50g) → +1 STR
- At 100 happiness: Train Strength (50g) → +1 STR (with 1.5x bonus)
- At 100 happiness: Intensive Training (200g) → +3 to all stats!

## 🏆 Leaderboard

The leaderboard tracks all players who have saved their game:
- Players are ranked by level, then by experience points
- Top 3 players receive special medals (🥇🥈🥉)
- Displays player stats including level, experience, gold, and equipped weapon
- Updates automatically when you save your game

Enjoy your adventure in High Wizardy! 🧙✨
