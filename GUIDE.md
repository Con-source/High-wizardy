# High Wizardy - Quick Reference Guide

## 🎮 How to Start Playing

```bash
python3 game.py
```

## 🎯 Game Mechanics

### Energy System
- **Maximum Energy**: 100
- **Regeneration Rate**: 5 energy every 15 minutes
- **Combat Cost**: 25 energy per encounter
- Energy automatically regenerates over time when you play

### Combat System
- Turn-based combat against various enemies
- Each attack uses your equipped weapon's damage
- Armor reduces incoming damage
- Enemies drop gold and experience on defeat

### Stats
- **Health**: Your life points (starts at 100)
- **Mana**: Used for magical attacks (starts at 100)
- **Energy**: Required to initiate combat and training (starts at 100)
- **Currency**: Shillings and Pennies for purchases (starts at 8s 4d)
- **Happiness**: Bonus multiplier for gym training (0-100, from properties)

## 🛒 Shopping

### Currency System
- **1 Shilling (s) = 12 Pennies (d)**
- Prices displayed as "Xs Yd" (e.g., "4s 2d" = 4 shillings and 2 pennies)
- Starting currency: 8 shillings, 4 pennies (100 pennies total)

### Weapons (5 available)
1. **Wooden Sword** - 4s 2d, 5 damage
2. **Iron Sword** - 12s 6d, 15 damage
3. **Steel Sword** - 25s, 30 damage
4. **Fire Staff** - 33s 4d, 40 damage, 10 mana cost (magic)
5. **Legendary Blade** - 83s 4d, 80 damage, 5 mana cost (magic)

### Armor (5 available)
1. **Leather Armor** - 5s, 5 defense
2. **Iron Armor** - 15s, 15 defense
3. **Steel Armor** - 29s 2d, 30 defense
4. **Enchanted Robes** - 41s 8d, 40 defense
5. **Dragon Scale Armor** - 100s, 70 defense

### Properties (4 available)
1. **Cottage** - 50s (small cozy cottage)
2. **Town House** - 100s (comfortable house in town)
3. **Manor** - 200s (grand manor with gardens)
4. **Castle** - 400s (magnificent castle)

### Property Upgrades (5 available)
1. **Garden** - 20s, +5 happiness
2. **Library** - 30s, +8 happiness
3. **Workshop** - 40s, +10 happiness
4. **Enchanted Fountain** - 60s, +15 happiness
5. **Observatory** - 80s, +20 happiness

## 🎮 Main Menu Options

1. **Weapon Shop** - Browse and purchase weapons
2. **Armor Shop** - Browse and purchase armor
3. **Combat** - Fight enemies (requires 25 energy)
4. **Gym Training** - Train your stats (requires 15 energy)
5. **Property Management** - Manage properties and upgrades
6. **Rest** - Restore 50 health and 50 mana
7. **Save Game** - Save your progress
8. **Exit** - Quit the game (option to save)

## ⚔️ Combat Actions

During combat you can:
1. **Attack** - Regular attack with your weapon
2. **Use Magic** - Enhanced attack using mana (if weapon supports it)
3. **Flee** - Run away from combat

## 💡 Tips

- Start by buying basic equipment (Wooden Sword + Leather Armor)
- Rest after combat to restore health and mana
- Save frequently to preserve your progress
- Energy regenerates automatically, so don't worry if you run out
- Level up by gaining experience in combat
- Magical weapons deal more damage but require mana
- Buy properties to increase your happiness
- Higher happiness gives better gym training bonuses (up to 1.5x)
- Upgrade properties to maximize happiness
- Train at the gym regularly to improve your max stats

## 📊 Leveling System

- Gain experience by defeating enemies
- Level up when you reach required XP
- Each level increases:
  - Max Health (+20)
  - Max Mana (+10)
  - Max Energy (+10)
- All stats are fully restored on level up

## 💾 Save/Load System

- Game automatically saves to `savegame.json`
- Load your saved game from the main menu
- Save before exiting to preserve progress

## 🎯 Strategy Guide

### Early Game
- Buy Wooden Sword (4s 2d) and Leather Armor (5s)
- Fight easier enemies (Goblins) to gain currency and XP
- Save currency for a property when you have ~50s
- Upgrade to Iron equipment when you have enough currency

### Mid Game
- Buy your first property (Cottage or Town House)
- Add upgrades to increase happiness
- Get Steel equipment for better stats
- Fight stronger enemies (Orcs, Dark Mages)
- Use gym training to boost your max stats
- Consider magical weapons if you like spell combat

### Late Game
- Own multiple properties with upgrades
- Max out your happiness for 1.5x gym bonus
- Save for legendary equipment
- Challenge Dragons for big rewards
- Max out your character's level and equipment
- List properties on marketplace for trading

## 🏠 Property Management

### Buying Properties
- Properties provide happiness which boosts gym training
- Start with a Cottage (50s) if you can afford it
- Bigger properties cost more but provide a foundation for more upgrades

### Upgrading Properties
- Each upgrade adds happiness to your total
- Higher happiness = better gym training multipliers
- Observatory gives the most happiness (+20)
- Plan your upgrades based on your budget

### Property Marketplace
- List properties for sale or rent
- Set your own prices for listings
- Browse other players' properties (in multiplayer)
- Properties sell with all their upgrades included

## 💪 Gym Training System

### How It Works
- Costs 15 energy per training session
- Choose between Health, Mana, or Energy training
- Base gains: Health +10, Mana +5, Energy +5
- Happiness bonus multiplies these gains (1.0x to 1.5x)

### Maximizing Gains
- Max out your happiness first (100/100)
- With max happiness: Health +15, Mana +7, Energy +7
- Train regularly when you have spare energy
- Balance your stat improvements based on your playstyle

Enjoy your adventure in High Wizardy! 🧙✨
