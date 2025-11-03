# 🔥 Pokemon Variant System Guide - v4.1.0

## Overview
The Pokemon National Dex Dashboard now supports **1,130 unique Pokemon forms** including base forms, Mega evolutions, regional variants, Gigantamax forms, and shiny versions!

## What's New in v4.1.0

### ✨ Features Added

1. **Variant Forms Support**
   - 1,025 base Pokemon
   - 48 Mega Evolutions (50 forms - Charizard X/Y, Mewtwo X/Y)
   - 25 Regional Forms (Alolan, Galarian)
   - 32 Gigantamax Forms
   - Total: **1,130 unique entries**

2. **Shiny Mode** ✨
   - Toggle between normal and shiny sprites
   - Works across all views (Search, Gallery, etc.)
   - Separate shiny sprites for each variant

3. **Variant Switcher**
   - View all forms of a Pokemon side-by-side using tabs
   - Example: Charizard shows Base, Mega X, Mega Y, and Gigantamax tabs
   - Each tab displays unique stats, types, abilities

4. **Smart Sprite Loading**
   - Supports base Pokemon: `001.png`, `002.png`, etc.
   - Supports variants: `006_mega_x.png`, `006_mega_y.png`
   - Supports shinies: `006_shiny.png`, `006_mega_x_shiny.png`
   - Animated sprites: `001.gif`, `002.gif` (Gen 5 style)

5. **Variant Badges in Gallery**
   - 🔥 = Mega Evolution
   - 🌍 = Regional Form (Alolan/Galarian/Hisuian)
   - ⚡ = Gigantamax
   - ✨ = Shiny variant

## How to Use

### Filtering by Variant Type

In the sidebar, use the **"Show Forms"** multiselect:
- **Base Forms** - Original Pokemon (default)
- **Mega Evolution** - All Mega evolutions including X/Y variants
- **Regional Forms** - Alolan, Galarian, Hisuian, Paldean variants
- **Gigantamax** - Gigantamax forms with G-Max moves

### Viewing Multiple Forms

1. Navigate to **🔍 Pokemon Search** tab
2. Search for a Pokemon with variants (e.g., "Charizard")
3. Expand the Pokemon entry
4. You'll see tabs for each form:
   - **Charizard** (base)
   - **Mega Charizard X** (Fire/Dragon)
   - **Mega Charizard Y** (Fire/Flying)
   - **Gigantamax Charizard** (with G-Max Wildfire)

Each tab shows:
- Unique sprite
- Updated stats (BST, HP, Attack, etc.)
- Type changes (if applicable)
- Abilities (including Mega-specific abilities)
- Mega Stone required (for Mega evolutions)
- G-Max Move (for Gigantamax forms)

### Shiny Mode

Toggle **✨ Shiny Mode** in the sidebar to see shiny versions of all Pokemon throughout the app!

## Data Structure

### Enhanced CSV Columns

New columns in `national_dex_with_variants.csv`:

- `variant_type` - Values: base, mega, mega-x, mega-y, alolan, galarian, hisuian, paldean, gigantamax
- `base_pokemon_id` - Links variants to their base form
- `sprite_path_static` - Path to PNG sprite
- `sprite_path_animated` - Path to GIF sprite
- `sprite_path_shiny` - Path to shiny variant
- `form_name` - Human-readable form name (e.g., "Mega Charizard X")
- `mega_stone` - Required Mega Stone item
- `gmax_move` - Gigantamax signature move
- `form_description` - Physical differences description

### Example Entries

**Charizard Base:**
```
pokedex_number: 6
name: Charizard
variant_type: base
type_1: Fire
type_2: Flying
total_points: 534
```

**Mega Charizard X:**
```
pokedex_number: 6
name: Charizard
variant_type: mega-x
form_name: Mega Charizard X
base_pokemon_id: 6
type_1: Fire
type_2: Dragon  ← Changed!
total_points: 634  ← +100 BST!
ability_1: Tough Claws  ← New ability!
mega_stone: Charizardite X
```

**Mega Charizard Y:**
```
pokedex_number: 6
name: Charizard
variant_type: mega-y
form_name: Mega Charizard Y
base_pokemon_id: 6
type_1: Fire
type_2: Flying
total_points: 634
ability_1: Drought  ← Different ability!
mega_stone: Charizardite Y
```

## Notable Variant Changes

### Mega Evolutions with Type Changes

- **Mega Charizard X**: Fire/Flying → Fire/Dragon
- **Mega Ampharos**: Electric → Electric/Dragon
- **Mega Pinsir**: Bug → Bug/Flying
- **Mega Gyarados**: Water/Flying → Water/Dark
- **Mega Sceptile**: Grass → Grass/Dragon

### Regional Forms with Type Changes

- **Alolan Rattata**: Normal → Dark/Normal
- **Alolan Raichu**: Electric → Electric/Psychic
- **Alolan Vulpix**: Fire → Ice
- **Alolan Ninetales**: Fire → Ice/Fairy
- **Alolan Sandshrew**: Ground → Ice/Steel
- **Galarian Ponyta**: Fire → Psychic
- **Galarian Weezing**: Poison → Poison/Fairy

### Gigantamax Signature Moves

- Venusaur: G-Max Vine Lash
- Charizard: G-Max Wildfire
- Blastoise: G-Max Cannonade
- Butterfree: G-Max Befuddle
- Pikachu: G-Max Volt Crash
- Meowth: G-Max Gold Rush
- ... and 26 more!

## Sprite Naming Convention

```
Base Pokemon:     001.png, 002.png, ..., 1025.png
Mega Evolution:   006_mega.png, 006_mega_x.png, 006_mega_y.png
Regional Forms:   019_alolan.png, 077_galarian.png
Gigantamax:       003_gigantamax.png, 006_gigantamax.png
Shiny Variants:   001_shiny.png, 006_mega_x_shiny.png
Animated:         001.gif, 002.gif, ... (in assets/animated/)
```

## Performance Considerations

- Sprites are cached using `@st.cache_data`
- Gallery limits adjustable (60-1025 sprites)
- Lazy loading: Sprites only load when visible
- Recommended: Keep gallery limit at 120 for optimal performance

## Testing Recommended Pokemon

To fully experience the variant system, try these Pokemon:

1. **Charizard (#6)** - 4 forms (Base, Mega X, Mega Y, Gigantamax)
2. **Mewtwo (#150)** - 3 forms (Base, Mega X, Mega Y)
3. **Venusaur (#3)** - 3 forms (Base, Mega, Gigantamax)
4. **Gengar (#94)** - 3 forms (Base, Mega, Gigantamax)
5. **Raichu (#26)** - 2 forms (Base, Alolan)
6. **Vulpix (#37)** - 2 forms (Base, Alolan)
7. **Ponyta (#77)** - 2 forms (Base, Galarian)

## Known Limitations

1. **Gigantamax Sprites**: Many Gigantamax forms use base sprites as placeholders (PokeAPI limitations)
2. **Hisuian/Paldean Forms**: Framework in place but data not yet added (coming in future update)
3. **Animated Variants**: Only base forms have animated sprites
4. **Some Mega Evolution IDs**: A few Mega forms have duplicate IDs in mapping (will be refined)

## Future Enhancements

- [ ] Add Hisuian regional forms
- [ ] Add Paldean regional forms
- [ ] Add Terastal forms
- [ ] Add form-specific Pokedex entries
- [ ] Add evolution chain visualization with variants
- [ ] Add sprite comparison view (side-by-side)
- [ ] Add variant filtering by stat changes
- [ ] Add "New Forms" filter for latest generation

## Technical Details

### Files Modified

- `src/core/app.py` - Added variant support throughout
- `data/national_dex_with_variants.csv` - Enhanced dataset
- `data/variant_summary.json` - Quick reference

### Files Created

- `build_variant_data.py` - Data generation script
- `download_all_sprites.py` - Comprehensive sprite downloader
- `IMPLEMENTATION_PLAN.md` - Full technical spec
- `VARIANT_SYSTEM_GUIDE.md` - This file!

### New Helper Functions

```python
load_sprite(pokemon_id, sprite_type='official', 
            use_animated=False, variant_type='base', shiny=False)
get_pokemon_variants(df, base_pokemon_id)
display_pokemon_card(pokemon, show_sprite=True, 
                     use_animated=True, shiny=False)
```

## Credits

- **PokeAPI** - Sprite sources and API
- **Bulbapedia** - Accurate variant stats and data
- **Pokemon Showdown** - Animated sprite inspiration

---

**Version**: 4.1.0  
**Release Date**: November 2025  
**Total Pokemon Forms**: 1,130  
**Sprite Count**: 2,200+ static, 1,025+ animated
