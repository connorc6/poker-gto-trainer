# Poker GTO Trainer

An interactive, browser-based poker GTO trainer with real equity calculation, full table simulation, and decision coaching — no downloads, no installs.

🎮 **[Play it live →](https://connorc6.github.io/poker-gto-trainer/)**

---

## Features

### 🃏 Play
- **Manual mode** — enter your hand and villain range, then play through the streets entering real board cards as they come out
- **Full table mode** — 6-player simulation where villain AIs make decisions based on their position ranges and actual hand strength
- Sequential betting action in correct order (UTG → HJ → CO → BTN → SB → BB preflop, SB-first postflop)
- All-in support, blind posting, raise re-queuing

### 📊 Range Charts
- GTO-aligned opening ranges for all 6 positions (EP, HJ, CO, BTN, SB, BB)
- Color-coded 13×13 hand matrix — open/raise, call, and fold zones
- Ranges based on standard percentage guidance: EP ~8%, HJ ~14%, CO ~22%, BTN ~35%, SB ~30%

### 🧮 Pot Odds Calculator
- Live pot odds from any pot size and call amount
- Compares breakeven equity against your current hand equity
- Rule of 2 & 4 outs-to-equity calculator (flop and turn)
- Common draw reference table (flush draw, OESD, gutshot, etc.)

### 📖 Glossary
- 50+ poker terms defined across 6 categories
- Positions, preflop concepts, postflop betting, hand strength, GTO strategy, pot & action
- Live search filtering

### 📈 Session Stats & Scoring
- Every decision is scored: **good** (3 pts), **ok** (1 pt), **bad** (0 pts)
- Scoring based on equity vs. action: value bets, pot odds calls, correct folds
- Hand history with per-hand accuracy percentage
- Persists across sessions via localStorage

### 💡 GTO Coaching Tips
- Context-aware tips generated each street based on your hand, board, position, and equity
- Covers c-bet spots, check-raise opportunities, pot odds, SPR, and more

---

## How to Use

Open **[connorc6.github.io/poker-gto-trainer](https://connorc6.github.io/poker-gto-trainer/)** in any browser — desktop or mobile.

### Manual Mode
1. Enter your hand (e.g. `Ah Kh`), position, villain range, and stack depth
2. Hit **Deal hand** — you start preflop
3. Make your action (Fold / Check / Bet), then click **Deal flop →**
4. Enter the 3 flop cards (e.g. `Ah Ks Td`) or click **Random**
5. Continue through turn and river the same way
6. See your decision breakdown and score at showdown

### Full Table Mode
1. Select your position, then click **Deal hand**
2. A 6-player table is dealt — each seat gets a hand from their position's range
3. Action moves clockwise in order — villains act automatically
4. When it's your turn, choose Fold / Check / Call / Raise
5. Streets advance automatically with community cards

---

## Tech

- **Pure HTML/CSS/JS** — single self-contained file, zero dependencies, zero installs
- **Hand evaluator** — JavaScript port of the `treys` library (rank-frequency + flush/straight detection), handles all hand categories including wheel straight
- **Monte Carlo equity** — 2,000-iteration simulation using partial Fisher-Yates shuffle; runs async so the UI stays responsive
- **Multi-way equity** — hero equity calculated against all active villain hands simultaneously
- **Range parser** — expands shorthand notation (`ATs+`, `88-JJ`, `KQo`) into individual combos

---

## Running Locally

No build step needed — just open the file:

```bash
git clone https://github.com/connorc6/poker-gto-trainer.git
cd poker-gto-trainer
open index.html   # macOS
# or just drag index.html into any browser
```

---

## Updating the Live Site

After making changes to `webapp.html`:

```bash
cp webapp.html index.html
git add webapp.html index.html
git commit -m "your message"
git push
```

GitHub Pages rebuilds automatically — changes go live in ~1 minute.

---

## Positions Reference

| Position | Abbr | Acts (Preflop) | Open Range |
|----------|------|----------------|------------|
| Early Position / Under the Gun | EP | 1st | ~8% |
| Hijack / Middle Position | HJ | 2nd | ~14% |
| Cutoff | CO | 3rd | ~22% |
| Button | BTN | 4th | ~35% |
| Small Blind | SB | 5th | ~30% |
| Big Blind | BB | Last | Defense |
