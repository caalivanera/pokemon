# Game Posters README

This directory contains official Pokemon game box art/posters.

## Structure

```
assets/games/
├── gen1/
│   ├── red.png
│   ├── blue.png
│   ├── yellow.png
│   └── green_jp.png
├── gen2/
│   ├── gold.png
│   ├── silver.png
│   └── crystal.png
├── gen3/
│   ├── ruby.png
│   ├── sapphire.png
│   ├── emerald.png
│   ├── firered.png
│   └── leafgreen.png
├── gen4/
│   ├── diamond.png
│   ├── pearl.png
│   └── platinum.png
├── gen5/
│   ├── black.png
│   ├── white.png
│   ├── black2.png
│   └── white2.png
├── gen6/
│   ├── x.png
│   └── y.png
├── gen7/
│   ├── sun.png
│   ├── moon.png
│   ├── ultrasun.png
│   └── ultramoon.png
├── gen8/
│   ├── sword.png
│   └── shield.png
└── gen9/
    ├── scarlet.png
    └── violet.png
```

## Game-Region Mapping

| Generation | Games | Region | Pokemon Count |
|------------|-------|--------|---------------|
| Gen 1 | Red, Blue, Yellow | Kanto | 151 |
| Gen 2 | Gold, Silver, Crystal | Johto | 100 |
| Gen 3 | Ruby, Sapphire, Emerald | Hoenn | 135 |
| Gen 4 | Diamond, Pearl, Platinum | Sinnoh | 107 |
| Gen 5 | Black, White, B2, W2 | Unova | 156 |
| Gen 6 | X, Y | Kalos | 72 |
| Gen 7 | Sun, Moon, Ultra | Alola | 88 |
| Gen 8 | Sword, Shield | Galar | 96 |
| Gen 9 | Scarlet, Violet | Paldea | 120 |

## Sources

Game box art sourced from:
- Official Pokemon websites
- Bulbapedia (fair use)
- Nintendo press kits
- Serebii.net archives

## Usage

Link Pokemon to their debut games using the `debut_game` column in the dataset.

```python
# Example: Get game poster for a Pokemon
def get_game_poster(generation):
    gen_map = {
        1: "gen1/red.png",
        2: "gen2/gold.png",
        3: "gen3/ruby.png",
        # ... etc
    }
    return f"assets/games/{gen_map.get(generation)}"
```

## Status

**Note:** Game posters are not included in the repository due to size constraints. 
To add them:

1. Download from official sources
2. Resize to consistent dimensions (512x512 recommended)
3. Save as PNG format
4. Follow the directory structure above

**Alternative:** Use placeholder images or external CDN links.
