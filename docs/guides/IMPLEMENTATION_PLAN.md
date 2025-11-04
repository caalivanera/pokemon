# Pokemon Variant System Implementation Plan

## Executive Summary
This plan outlines the complete implementation of a Pokemon variant system supporting:
- Shiny forms (all 1,025 Pokemon)
- Mega Evolutions (48 Pokemon with 48 Mega forms, Charizard/Mewtwo have 2 each)
- Regional forms (Alolan: 19, Galarian: 19, Hisuian: 17, Paldean: 2)
- Gigantamax forms (32 Pokemon)
- Terastal forms (all Pokemon - visual effect only)

**Estimated Total Variants**: ~1,300+ unique form combinations

---

## Phase 1: Data Architecture Redesign

### 1.1 Enhanced CSV Structure
**New Columns to Add:**
```csv
variant_type,          # base, shiny, mega, mega-x, mega-y, alolan, galarian, hisuian, paldean, gigantamax
base_pokemon_id,       # References the base form's pokedex_number
sprite_path_static,    # Path to static PNG sprite
sprite_path_animated,  # Path to animated GIF sprite
sprite_path_shiny,     # Path to shiny variant sprite
form_name,             # Human-readable: "Mega Charizard X", "Alolan Vulpix"
mega_stone,            # Charizardite X, Charizardite Y, etc.
gmax_move,             # G-Max Wildfire, G-Max Vine Lash, etc.
form_description,      # Physical differences for this variant
```

### 1.2 Example Entry - Charizard Family
```csv
# Base Charizard (existing entry stays mostly same)
6,Charizard,...,base,6,sprites/006.png,animated/006.gif,sprites/006_shiny.png,Charizard,,,,Original form

# Mega Charizard X (new entry)
6,Mega Charizard X,...,mega-x,6,sprites/006_mega_x.png,animated/006_mega_x.gif,sprites/006_mega_x_shiny.png,Mega Charizard X,Charizardite X,,Black dragon form with blue flames

# Mega Charizard Y (update existing)
6,Mega Charizard Y,...,mega-y,6,sprites/006_mega_y.png,animated/006_mega_y.gif,sprites/006_mega_y_shiny.png,Mega Charizard Y,Charizardite Y,,Sleeker with longer wings

# Gigantamax Charizard (new entry)
6,Gigantamax Charizard,...,gigantamax,6,sprites/006_gigantamax.png,animated/006_gigantamax.gif,sprites/006_gigantamax_shiny.png,Gigantamax Charizard,,G-Max Wildfire,Massive with flame wings

# Shiny handling: Each form has sprite_path_shiny
```

---

## Phase 2: Asset Acquisition Strategy

### 2.1 Static Sprites (PNG)
**Sources (in order of preference):**
1. **PokeAPI** - https://pokeapi.co/api/v2/pokemon/{id}/
   - Sprites: official-artwork, home, dream-world
   - Shiny variants available
2. **Bulbapedia Archives** - https://archives.bulbagarden.net/
3. **PokemonDB** - https://pokemondb.net/sprites
4. **Manual backup** - Serebii.net sprite project

**Total Required:**
- ~1,025 base forms (already have 782)
- ~1,025 shiny forms  
- ~150 variant forms (Mega, regional, Gmax)
- **Total: ~2,200 static sprites**

### 2.2 Animated Sprites (GIF)
**Sources:**
1. **Gen 5 Animated Sprites** - https://veekun.com/dex/downloads
2. **Pokemon Showdown** - https://github.com/smogon/pokemon-showdown-client/tree/master/sprites
3. **PokeAPI animated sprites**

**Total Required:**
- Same ~2,200 animated GIFs

### 2.3 Download Script Structure
```python
# download_all_variants.py
import requests
import pandas as pd
from pathlib import Path
import time

VARIANT_MAPPINGS = {
    # Format: base_id: [variant_forms]
    6: ['base', 'mega-x', 'mega-y', 'gigantamax'],  # Charizard
    3: ['base', 'mega', 'gigantamax'],              # Venusaur
    # ... 100+ more
}

SPRITE_SOURCES = {
    'static': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png',
    'static_shiny': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/{id}.png',
    'animated': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{id}.gif',
    'animated_shiny': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/shiny/{id}.gif',
}

def download_variant_sprites(pokemon_id, variant_type):
    """Download all sprite variations for a Pokemon variant"""
    # Implementation with retry logic, rate limiting, fallbacks
    pass
```

---

## Phase 3: Application Updates

### 3.1 Data Loading Function
```python
# src/core/data_loader.py
def load_pokemon_data(include_variants=True):
    """Load Pokemon data with variant support"""
    df = pd.read_csv('data/national_dex.csv')
    
    if include_variants:
        # Group by base_pokemon_id to enable variant filtering
        df['has_variants'] = df.groupby('base_pokemon_id')['variant_type'].transform('count') > 1
    
    return df

def get_pokemon_variants(base_id):
    """Get all variants for a specific Pokemon"""
    df = load_pokemon_data()
    return df[df['base_pokemon_id'] == base_id]
```

### 3.2 UI Enhancements

#### Variant Selector
```python
# Add to sidebar in app.py
variant_filter = st.sidebar.multiselect(
    "Show Variants",
    options=['Base Forms', 'Shiny', 'Mega Evolution', 'Regional Forms', 'Gigantamax'],
    default=['Base Forms']
)
```

#### Sprite Display with Variants
```python
def display_pokemon_card(pokemon_row):
    """Display Pokemon card with variant switcher"""
    base_id = pokemon_row['base_pokemon_id']
    variants = get_pokemon_variants(base_id)
    
    if len(variants) > 1:
        # Show variant selector
        variant_tabs = st.tabs([v['form_name'] for v in variants.iterrows()])
        for tab, (_, variant) in zip(variant_tabs, variants.iterrows()):
            with tab:
                st.image(variant['sprite_path_static'])
                st.write(f"**Type:** {variant['type_1']}/{variant['type_2']}")
                st.write(f"**BST:** {variant['total_points']}")
                # ... more stats
    else:
        # Single form display
        st.image(pokemon_row['sprite_path_static'])
```

### 3.3 Enhanced Features

#### Shiny Toggle
```python
# Global toggle for shiny mode
shiny_mode = st.sidebar.checkbox("✨ Shiny Mode", value=False)

def get_sprite_path(pokemon_row, shiny=False):
    """Get appropriate sprite path"""
    if shiny and pd.notna(pokemon_row['sprite_path_shiny']):
        return pokemon_row['sprite_path_shiny']
    return pokemon_row['sprite_path_static']
```

#### Sprite Everywhere (Task 3)
```python
# Add sprites to:
1. Table rows (thumbnail column)
2. Dropdown selections (with st.image inline)
3. Hover tooltips
4. Header/title sections
5. Comparison views (side-by-side)
6. Evolution chains (with arrows)
7. Type badges (mini icons)
```

---

## Phase 4: Comprehensive Variant Data

### 4.1 Mega Evolutions (Generation 6)
**Total: 48 Pokemon, 48 Mega forms** (Charizard/Mewtwo have 2 each)

```python
MEGA_EVOLUTIONS = {
    3: {'name': 'Venusaur', 'stone': 'Venusaurite', 'bst': 625},
    6: {
        'X': {'name': 'Charizard', 'stone': 'Charizardite X', 'bst': 634, 'type': 'Fire/Dragon'},
        'Y': {'name': 'Charizard', 'stone': 'Charizardite Y', 'bst': 634, 'type': 'Fire/Flying'},
    },
    9: {'name': 'Blastoise', 'stone': 'Blastoisite', 'bst': 630},
    # ... 45 more
}
```

### 4.2 Regional Forms
**Alolan Forms** (Generation 7): 19 Pokemon
```python
ALOLAN_FORMS = [19, 20, 26, 27, 28, 37, 38, 50, 51, 52, 53, 74, 75, 76, 88, 89, 103, 105]
# Rattata, Raticate, Raichu, Sandshrew, Sandslash, Vulpix, Ninetales, etc.
```

**Galarian Forms** (Generation 8): 19 Pokemon
```python
GALARIAN_FORMS = [52, 77, 78, 79, 80, 83, 110, 122, 144, 145, 146, 199, 222, 263, 264, 554, 555, 562, 618]
# Meowth, Ponyta, Rapidash, Slowpoke, Slowbro, Farfetch'd, Weezing, etc.
```

**Hisuian Forms** (Legends Arceus): 17 Pokemon
```python
HISUIAN_FORMS = [58, 59, 100, 101, 157, 211, 215, 503, 549, 550, 570, 571, 628, 705, 706, 713, 724]
# Growlithe, Arcanine, Voltorb, Electrode, Typhlosion, Qwilfish, etc.
```

**Paldean Forms** (Generation 9): 2 Pokemon
```python
PALDEAN_FORMS = [128, 194]  # Tauros (3 variants), Wooper
```

### 4.3 Gigantamax Forms (Generation 8)
**Total: 32 Pokemon**
```python
GIGANTAMAX_FORMS = {
    3: {'name': 'Venusaur', 'move': 'G-Max Vine Lash'},
    6: {'name': 'Charizard', 'move': 'G-Max Wildfire'},
    9: {'name': 'Blastoise', 'move': 'G-Max Cannonade'},
    12: {'name': 'Butterfree', 'move': 'G-Max Befuddle'},
    25: {'name': 'Pikachu', 'move': 'G-Max Volt Crash'},
    # ... 27 more
}
```

### 4.4 Terastal Forms (Generation 9)
**Note:** Terastal is a crystalline visual effect, not a permanent form change
- All 1,025 Pokemon can Terastallize
- 18 different Tera Types (one per type)
- Visual: Crystal crown with type symbol
- Implementation: Optional sparkle effect overlay on sprite

---

## Phase 5: Implementation Timeline

### Week 1: Data Architecture
- [ ] Design new CSV schema
- [ ] Create migration script for existing data
- [ ] Add new columns to national_dex.csv
- [ ] Create variant entries for top 50 Pokemon

### Week 2: Asset Collection
- [ ] Download base sprites for missing Pokemon (243)
- [ ] Download shiny sprites for all Pokemon (1,025)
- [ ] Download Mega evolution sprites (48)
- [ ] Download regional form sprites (57)
- [ ] Download Gigantamax sprites (32)
- [ ] Organize into proper folder structure

### Week 3: Animated Sprites
- [ ] Download Gen 5 animated sprites
- [ ] Download animated variants where available
- [ ] Create fallback logic for missing animations

### Week 4: Application Updates
- [ ] Update data loading functions
- [ ] Add variant selector UI components
- [ ] Implement shiny toggle
- [ ] Add sprites to all UI elements
- [ ] Create variant comparison views

### Week 5: Testing & Polish
- [ ] Test all variant displays
- [ ] Verify sprite paths
- [ ] Performance optimization
- [ ] Mobile responsiveness
- [ ] Documentation

### Week 6: Deployment
- [ ] Final testing
- [ ] Git commit with detailed changelog
- [ ] Push to GitHub
- [ ] Monitor Streamlit Cloud deployment
- [ ] User feedback collection

---

## Phase 6: Technical Specifications

### 6.1 Sprite Naming Convention
```
Static Sprites:
- Base: sprites/{pokedex_number:03d}.png           # 006.png
- Variant: sprites/{pokedex_number:03d}_{form}.png # 006_mega_x.png
- Shiny: sprites/{pokedex_number:03d}_shiny.png    # 006_shiny.png
- Variant Shiny: sprites/{pokedex_number:03d}_{form}_shiny.png

Animated Sprites:
- Same pattern in animated/ folder with .gif extension

Icons:
- icons/{type_name}.png
- icons/mega_stone/{stone_name}.png
```

### 6.2 Data Validation Rules
```python
def validate_variant_data(df):
    """Ensure variant data integrity"""
    checks = {
        'base_pokemon_exists': lambda: all(df[df['variant_type'] == 'base']['base_pokemon_id'] == df[df['variant_type'] == 'base']['pokedex_number']),
        'sprites_exist': lambda: all(Path(p).exists() for p in df['sprite_path_static'] if pd.notna(p)),
        'unique_forms': lambda: not df.duplicated(subset=['base_pokemon_id', 'variant_type', 'form_name']).any(),
        'stats_valid': lambda: all(df['total_points'] == df[['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].sum(axis=1)),
    }
    return {name: check() for name, check in checks.items()}
```

### 6.3 Performance Considerations
```python
# Lazy loading for sprites
@st.cache_data(ttl=3600)
def load_sprite(sprite_path):
    """Cache sprite loading"""
    return Image.open(sprite_path)

# Pagination for large datasets
ITEMS_PER_PAGE = 50

# Virtualized scrolling for gallery
# Progressive loading for animations
```

---

## Phase 7: Success Criteria

✅ **Data Completeness**
- [ ] 1,025 base Pokemon entries
- [ ] 1,025 shiny variants documented
- [ ] All Mega evolutions (48) with correct stats
- [ ] All regional forms (57) with correct types
- [ ] All Gigantamax forms (32) with G-Max moves

✅ **Asset Coverage**
- [ ] 90%+ static sprites downloaded
- [ ] 75%+ animated sprites available
- [ ] All variant forms have distinct sprites
- [ ] Shiny variants for popular Pokemon (Gen 1-5)

✅ **Functionality**
- [ ] Variant selector works smoothly
- [ ] Shiny toggle functional
- [ ] Sprites display throughout app
- [ ] Performance: <2s page load
- [ ] No broken image links

✅ **User Experience**
- [ ] Intuitive variant navigation
- [ ] Responsive on mobile
- [ ] Smooth animations (when available)
- [ ] Clear visual distinctions between forms
- [ ] Helpful tooltips and descriptions

---

## Risk Mitigation

### High Risk: Sprite Availability
- **Issue**: Not all variant sprites publicly available
- **Mitigation**: 
  1. Fallback to base form sprite with badge
  2. Use PokeAPI dynamic loading
  3. Community-sourced placeholders for missing sprites

### Medium Risk: Data Consistency
- **Issue**: Conflicting stats from different sources
- **Mitigation**:
  1. Primary source: Bulbapedia
  2. Cross-reference: Serebii, PokemonDB
  3. Manual verification for discrepancies

### Medium Risk: Performance
- **Issue**: 2,200+ images slow page load
- **Mitigation**:
  1. Lazy loading
  2. Image compression (WebP format)
  3. CDN hosting (optional)
  4. Pagination/virtualization

### Low Risk: Maintenance
- **Issue**: New Pokemon/forms in future generations
- **Mitigation**:
  1. Modular design
  2. Automated ingestion scripts
  3. Version control
  4. Clear documentation

---

## Next Steps

**Immediate Actions:**
1. Review and approve this plan
2. Set up development branch
3. Begin Phase 1: Data Architecture
4. Create sprite download script
5. Test with Charizard family first

**Questions to Address:**
1. Should shiny variants be separate entries or toggle-based?
2. Include Terastal as actual variants or visual effect only?
3. Animated sprites: autoplay or click-to-animate?
4. Mobile strategy: show fewer sprites or compress more?

---

**Last Updated**: November 3, 2025
**Version**: 1.0

