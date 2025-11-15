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
- **Energy**: Required to initiate combat (starts at 100)
- **Gold**: Currency for buying equipment (starts at 100)

## 🛒 Shopping

### Weapons (5 available)
1. **Wooden Sword** - 50g, 5 damage
2. **Iron Sword** - 150g, 15 damage
3. **Steel Sword** - 300g, 30 damage
4. **Fire Staff** - 400g, 40 damage, 10 mana cost (magic)
5. **Legendary Blade** - 1000g, 80 damage, 5 mana cost (magic)

### Armor (5 available)
1. **Leather Armor** - 60g, 5 defense
2. **Iron Armor** - 180g, 15 defense
3. **Steel Armor** - 350g, 30 defense
4. **Enchanted Robes** - 500g, 40 defense
5. **Dragon Scale Armor** - 1200g, 70 defense

## 🎮 Main Menu Options

1. **Weapon Shop** - Browse and purchase weapons
2. **Armor Shop** - Browse and purchase armor
3. **Combat** - Fight enemies (requires 25 energy)
4. **Rest** - Restore 50 health and 50 mana
5. **Training Gym** - Train combat stats for gold
6. **View Leaderboard** - See rankings of all players
7. **Save Game** - Save your progress
8. **Exit** - Quit the game (option to save)

## ⚔️ Combat Actions

During combat you can:
1. **Attack** - Regular attack with your weapon
2. **Use Magic** - Enhanced attack using mana (if weapon supports it)
3. **Flee** - Run away from combat

## 💡 Tips

- Start by buying basic equipment (Wooden Sword + Leather Armor)
- Train at the gym to boost your combat stats early on
- Strength is great for dealing more damage in combat
- Vitality helps you survive longer by increasing defense
- Rest after combat to restore health and mana
- Save frequently to preserve your progress
- Energy regenerates automatically, so don't worry if you run out
- Level up by gaining experience in combat
- Magical weapons deal more damage but require mana
- Check the leaderboard to see how you rank against other players!
- Balance equipment purchases with training investments

## 📊 Leveling System

- Gain experience by defeating enemies
- Level up when you reach required XP
- Each level increases:
  - Max Health (+20)
  - Max Mana (+10)
  - Max Energy (+10)
- All stats are fully restored on level up

## 💪 Combat Stats System

Combat stats enhance your combat effectiveness:

### Strength (STR)
- Increases attack damage by **+3 per point**
- Stacks with weapon damage
- Example: 10 STR = +30 damage bonus

### Agility (AGI)
- Currently trains for future features
- Planned: dodge chance, critical hits

### Vitality (VIT)
- Increases defense by **+2 per point**
- Stacks with armor defense
- Example: 10 VIT = +20 defense bonus

### Training Costs
- Individual stat training: **50 gold** for +1 stat
- Intensive training: **200 gold** for +2 to all stats
- Train at the gym between missions to maximize power

## 💾 Save/Load System

- Game automatically saves to `savegame.json`
- Load your saved game from the main menu
- Save before exiting to preserve progress
- Your stats are automatically added to the leaderboard when you save

## 🏆 Leaderboard System

- All saved players appear on the leaderboard
- Rankings are based on level first, then experience points
- Top 3 players get special medal icons (🥇 Gold, 🥈 Silver, 🥉 Bronze)
- Displays key stats: Level, Experience, Gold, and equipped Weapon
- Updates automatically every time you save your game
- Compete with friends to reach the top of the leaderboard!

## 🎯 Strategy Guide

### Early Game
- Buy Wooden Sword (50g) and Leather Armor (60g)
- Train 1-2 points in Strength for extra damage
- Fight easier enemies (Goblins) to gain gold and XP
- Upgrade to Iron equipment when you have ~350g

### Mid Game
- Get Steel equipment for better stats
- Balance training stats with equipment upgrades
- Train Vitality to survive tougher enemies
- Fight stronger enemies (Orcs, Dark Mages)
- Consider magical weapons if you like spell combat

### Late Game
- Save for legendary equipment
- Max out combat stats (aim for 10+ in each)
- Challenge Dragons for big rewards
- Max out your character's level and equipment

### Combat Optimization
- **For Glass Cannon**: Focus on Strength + powerful weapons
- **For Tank**: Focus on Vitality + heavy armor
- **Balanced Build**: Distribute points evenly across all stats
- Strength scales best with high-damage weapons
- Vitality becomes more valuable against stronger enemies

Enjoy your adventure in High Wizardy! 🧙✨
