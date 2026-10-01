# STARCORE

Telegram game with exploration, evolution, competition and a separate monetization layer.

## Current Telegram menu

The main menu exposes the core game systems directly:

- 🧬 Profile
- 🎮 Game
- 📊 Statistics
- 🎒 Inventory
- 🎯 Missions
- 🏆 Achievements
- 🏅 Ranking
- 👥 Community
- 🛡 Guild
- 💱 Trading
- 🛒 Shop
- 🌌 Systems hub
- 🔔 Notifications
- ℹ️ Help
- 🧩 All sections
- ❌ Hide menu

`/sections` opens the complete systems navigator. Every inline callback is routed through a dedicated handler and the navigation includes a return path to the main menu.

## Stage 0

The foundation currently includes:

- Telegram bot entrypoint with `/start`
- SQLAlchemy database layer
- Player model and automatic player creation
- Credits, crystals, energy, XP and level foundations
- Environment configuration through `.env`
- Automated pytest checks through GitHub Actions
- Persistent game-state storage for genome, inventory, quests, exploration, combat, abilities and economy
- Social and guild database models

## Local setup

1. Copy `.env.example` to `.env`.
2. Set `BOT_TOKEN` from BotFather.
3. Optionally set `DATABASE_URL`. The default is SQLite for development.
4. Install dependencies with `pip install -r requirements.txt`.
5. Run `python bot.py`.

## Roadmap

1. Foundation
2. Player progression and economy
3. Exploration and events
4. PvE/PvP combat
5. Missions and achievements
6. Social/referral systems
7. Inventory and shop
8. Telegram Stars and compliant affiliate integrations
9. Anti-fraud and analytics
10. Admin tools
11. Full testing
12. Production launch

Telegram Stars are kept separate from the game's internal currencies. Real-money and Stars features will only use Telegram-supported mechanisms and will be added after the core game is stable.
