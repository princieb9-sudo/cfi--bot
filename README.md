# Discord Match Score Bot

## Setup

1. Open `C:\discord-bot\.env`.
2. Replace `PASTE_YOUR_BOT_TOKEN_HERE` with your real Discord bot token.
3. Start the bot:

```powershell
cd C:\discord-bot
python bot.py
```

## Commands

Add a player's match percentage. The bot converts `1%` into `1300` score and adds it to that player's total:

```text
/score_add player: Prince percent: 5
```

Show the public Prestige leaderboard:

```text
/score_show
```

Remove one player:

```text
/score_reset_player player: Prince
```

Clear the whole leaderboard:

```text
/score_reset_all
```

Data is saved in `C:\discord-bot\data\scores.json`.
