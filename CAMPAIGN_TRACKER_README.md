# Hail of Fire: Operation Overlord Campaign Tracker

A web-based campaign tracker for the Hail of Fire WWII tabletop wargame.

## Live Demo

Host this on GitHub Pages to share with your gaming group!

## Features

- **Interactive Campaign Map** - Visual sector control with clickable markers
- **Player Management** - Track players, sides, coins, and rerolls
- **Game Recording** - Log battles with automatic sector updates
- **Coin System** - Track player rewards and reroll eligibility
- **Discord Integration** - Post game results and standings to your Discord server
- **Data Import/Export** - Backup and restore campaign data as JSON

## Quick Start (GitHub Pages Hosting)

### 1. Create a GitHub Repository

1. Go to [github.com](https://github.com) and create a new repository
2. Name it something like `hailoffire-campaign`
3. Make it public (required for free GitHub Pages)

### 2. Upload Files

Upload these files to your repository:
- `index.html` (rename `campaign-tracker.html` to this)
- `mapv3.jpg` (the campaign map image)

### 3. Enable GitHub Pages

1. Go to your repository Settings
2. Click "Pages" in the left sidebar
3. Under "Source", select "Deploy from a branch"
4. Choose "main" branch and "/ (root)" folder
5. Click Save

### 4. Access Your Site

Your tracker will be live at: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`

## Discord Integration

To connect to Discord:

1. In your Discord server, go to **Server Settings** → **Integrations** → **Webhooks**
2. Click **New Webhook**
3. Name it (e.g., "Campaign Tracker")
4. Choose the channel for updates
5. Copy the webhook URL
6. In the tracker, go to **Import/Export** tab
7. Paste the webhook URL and click **Save Webhook**

### Discord Features

- **Test Connection** - Verify the webhook is working
- **Post Standings** - Share current campaign status
- **Auto-post Games** - After recording a game, you'll be prompted to post to Discord

## Data Storage

Campaign data is stored in your browser's localStorage. To share data between users:

1. Use **Export Data** to download a JSON backup
2. Share the JSON file with other campaign organizers
3. They can use **Import Data** to load it

**Important:** Each browser/device has its own localStorage. The data is NOT automatically synced between users.

## Files Overview

| File | Purpose |
|------|---------|
| `campaign-tracker.html` | Main web application (rename to `index.html` for hosting) |
| `mapv3.jpg` | Campaign map image |
| `*.csv` | Legacy CSV files (optional, for spreadsheet users) |

## Victory Conditions

- **Allied Victory:** Control all 7 cities for 7 consecutive days
- **Week 8:** Whoever controls more cities wins
- **Cities:** Cherbourg, Ste-Mere-Eglise, Carentan, Bayeux, Caen, Saint-Lo, Coutances

## Coin System

| Action | Coins |
|--------|-------|
| Play a game (report with photos) | +1 |
| Store purchase ($30+) | +1 (repeatable) |
| Paint/assemble in store | +1 per session |
| Use newly purchased unit | +2 (one-time) |
| Bring a new player | +2 |
| New player joins campaign | +2 (additional) |

**Rerolls:** 1 reroll per 4 coins earned

---

## Legacy CSV Files

For those who prefer spreadsheets, the original CSV files are included:

- `players.csv` - Player roster
- `games.csv` - Game results
- `coins.csv` - Coin transactions
- `sectors.csv` - Map sector data

These can be imported into Google Sheets or Excel.
