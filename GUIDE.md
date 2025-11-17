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
6. **Property Market** - Buy, upgrade, and rent properties
7. **View Leaderboard** - See rankings of all players
8. **Save Game** - Save your progress
9. **Exit** - Quit the game (option to save)

## ⚔️ Combat Actions

During combat you can:
1. **Attack** - Regular attack with your weapon
2. **Use Magic** - Enhanced attack using mana (if weapon supports it)
3. **Flee** - Run away from combat

## 💡 Tips

- Start by buying basic equipment (Wooden Sword + Leather Armor)
- Train at the gym to boost your combat stats early on
- **Invest in a cottage early** for the happiness bonus to training
- **Upgrade your properties** to maximize happiness and training gains
- Strength is great for dealing more damage in combat
- Agility helps you dodge attacks and survive longer
- Vitality helps you survive longer by increasing defense
- Rest after combat to restore health and mana
- Save frequently to preserve your progress
- Energy regenerates automatically, so don't worry if you run out
- Level up by gaining experience in combat
- Magical weapons deal more damage but require mana
- Check the leaderboard to see how you rank against other players!
- Balance equipment purchases with training investments
- High agility (15+) makes you very evasive in combat
- **At 100 happiness, you get 50% more stats from training!**
- **Properties can be sold for 50% of their value if you need gold**

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
- Provides dodge chance: **+2% per point**
- Allows you to completely avoid incoming attacks
- Maximum dodge chance: **50% (at 25 AGI)**
- Example: 10 AGI = 20% chance to dodge attacks

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
- **For Evasive Fighter**: Focus on Agility + moderate weapons (30%+ dodge is very effective)
- **For Tank**: Focus on Vitality + heavy armor
- **Balanced Build**: Distribute points evenly across all stats
- Strength scales best with high-damage weapons
- Agility is most valuable at 15-25 points (30-50% dodge)
- Vitality becomes more valuable against stronger enemies
- Combining moderate Agility (10-15) with high Vitality creates a very durable character

## 🏠 Property System Guide

The Property System allows you to own real estate that boosts your happiness!

### Getting Started with Properties

1. **First Property**: Save 50-75 gold and buy a cottage
2. **Immediate Benefit**: Gain +10 base happiness
3. **Upgrade**: Add 1-2 upgrades for +5 happiness each
4. **Result**: 20-25 happiness = 1.10-1.13x training bonus!

### Property Market Menu

Access via Main Menu → Option 6 (Property Market)

**Menu Options:**
1. **Browse Properties for Sale** - View and purchase available properties
2. **View My Properties** - See all properties you own and their stats
3. **Upgrade a Property** - Add improvements to your properties
4. **Sell a Property** - Sell for 50% of purchase price
5. **List Property for Rent** - Put a property on the rental market
6. **View Rental Listings** - Browse and rent properties from other players

### Property Details

#### Cottages (Affordable)
- **Cozy Cottage**: 50s 0p (~50g), 100 sq ft, 2 upgrades
- **Village Cottage**: 75s 6p (~75g), 120 sq ft, 2 upgrades
- Base Happiness: +10
- Best for: Early game, budget builds

#### Manors (Mid-Tier)
- **Stone Manor**: 200s 0p (~200g), 300 sq ft, 4 upgrades
- **Lakeside Manor**: 250s 0p (~250g), 350 sq ft, 4 upgrades
- Base Happiness: +25
- Best for: Mid game, balanced builds

#### Castles (Premium)
- **Small Castle**: 500s 0p (~500g), 800 sq ft, 6 upgrades
- **Grand Castle**: 1000s 0p (~1000g), 1200 sq ft, 8 upgrades
- Base Happiness: +50
- Best for: Late game, maximum happiness

### Upgrade System

Each property type has unique upgrades available:

#### Cottage Upgrades
- **Small Garden** (20g): A pleasant garden for relaxation (+5 happiness)
- **Bookshelf** (25g): A cozy reading corner (+5 happiness)
- Max Total: +20 happiness from upgrades

#### Manor Upgrades
- **Library** (50g): Extensive book collection (+10 happiness)
- **Training Room** (60g): Basic workout equipment (+10 happiness)
- **Garden** (40g): Well-maintained garden (+8 happiness)
- **Workshop** (55g): Place for crafts and hobbies (+9 happiness)
- Max Total: +37 happiness from upgrades

#### Castle Upgrades
- **Grand Library** (100g): Magnificent library with rare books (+15 happiness)
- **Full Gymnasium** (120g): Complete training facilities (+15 happiness)
- **Royal Garden** (90g): Sprawling gardens with exotic plants (+12 happiness)
- **Armory** (110g): Well-stocked armory (+13 happiness)
- **Chapel** (80g): Peaceful place for meditation (+11 happiness)
- **Observatory** (95g): For studying the stars (+12 happiness)
- Max Total: +78 happiness from upgrades

### Happiness Calculation

**Total Happiness = Sum of (Property Base + Property Upgrades)**

Examples:
- Cottage + 2 upgrades: 10 + 5 + 5 = 20 happiness
- Manor + 4 upgrades: 25 + 10 + 10 + 8 + 9 = 62 happiness
- Castle + 6 upgrades: 50 + 15 + 15 + 12 + 13 + 11 + 12 = 128 → capped at 100

### Training Bonus Formula

**Multiplier = 1.0 + (Happiness / 200)**

Examples:
- 0 happiness: 1.00x (no bonus)
- 20 happiness: 1.10x
- 40 happiness: 1.20x
- 60 happiness: 1.30x
- 80 happiness: 1.40x
- 100 happiness: 1.50x (maximum)

### Training Gains with Happiness

| Training Type | Base Cost | 0 Happy | 50 Happy | 100 Happy |
|--------------|-----------|---------|----------|-----------|
| Single Stat | 50g | +1 | +1 | +1 |
| Intensive | 200g | +2 | +2 | +3 |

*Note: Gains are rounded down from the multiplier*

### Rental Market

**Listing a Property:**
1. Own an unrented property
2. Go to Property Market → List Property for Rent
3. Set rent amount (suggested: 10% of property value)
4. Property appears on rental market

**Renting a Property:**
1. Browse rental listings
2. Pay one-time rent to gain happiness from that property
3. Note: Current implementation is simplified (no periodic payments)

### Property Strategy

#### Budget Strategy (Under 200g total)
- Buy 1 Cottage (50-75g)
- Add 2 upgrades (40-50g)
- Total: ~100-125g for 20 happiness (1.10x training)
- ROI: Every 5 training sessions saves 50g worth of stats

#### Balanced Strategy (200-500g total)
- Buy 1 Manor (200-250g)
- Add 2-3 upgrades (90-165g)
- Total: ~290-415g for 45-55 happiness (1.23-1.28x training)

#### Maximum Happiness Strategy (1000g+)
- Buy 1 Castle (500-1000g)
- Add 6+ upgrades (500-600g)
- Total: ~1500g for 100 happiness (1.50x training)
- Benefit: Permanent 50% boost to all training!

#### Multi-Property Strategy
- Buy multiple smaller properties
- Spread investments across property types
- Flexibility to sell if gold needed
- Example: 2 Cottages + upgrades = 40-50 happiness for ~200g

### When to Invest in Properties

**Early Game (Level 1-3):**
- Consider waiting until you have 150g saved
- Buy basic combat equipment first
- Then invest in a cottage

**Mid Game (Level 4-8):**
- Upgrade to a manor once affordable
- Max out upgrades on your property
- Training bonus pays for itself quickly

**Late Game (Level 9+):**
- Invest in a castle for maximum happiness
- Fully upgrade for 1.50x training multiplier
- Sell old properties if needed for castle funds

### Property Economics

**Break-Even Analysis:**
- At 1.50x training: Intensive Training gives +3 instead of +2
- Extra stat = 50g value (cost of single stat training)
- Every 4 intensive trainings = 200g saved
- Castle + full upgrades (~1500g) breaks even after ~30 training sessions

**Selling Properties:**
- Get 50% of purchase price back
- Lose all upgrade investments
- Useful if you need quick gold
- Better to save and buy bigger instead of upgrading then selling

Enjoy your adventure in High Wizardy! 🧙✨
