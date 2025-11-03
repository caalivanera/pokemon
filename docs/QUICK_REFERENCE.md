# 🚀 Phase 5 Quick Reference Card

**Version**: 5.4.0  
**Last Updated**: December 2024

---

## 📊 Meta Analytics Dashboard (Tab 13)

### Access
```python
Navigate to: Tab 13 "📊 Meta Analytics"
```

### Features
- **Usage Trends**: Track Pokemon popularity over 6 months
- **Move Analysis**: Most used moves by type and popularity
- **Ability Stats**: Top abilities with usage counts
- **Tier Distribution**: Pokemon distribution across 8 tiers
- **Meta Insights**: AI-powered recommendations

### Tips
✅ Use date range filter for specific periods  
✅ Export data as CSV for external analysis  
✅ Check rising/falling Pokemon for meta shifts  
✅ Compare move usage across different tiers  

---

## ⚔️ Damage Calculator (Tab 14)

### Access
```python
Navigate to: Tab 14 "⚔️ Damage Calculator"
```

### How to Use
1. **Select Attacker**: Choose attacking Pokemon
2. **Select Defender**: Choose defending Pokemon
3. **Choose Move**: Pick attack move
4. **Set Modifiers**: Weather, items, abilities, stat boosts
5. **Calculate**: See damage range and KO predictions

### Formula
```
Damage = ((2 × Level / 5 + 2) × Power × A/D / 50 + 2) × Modifiers
```

### Modifiers
- **STAB**: 1.5× (Same Type Attack Bonus)
- **Critical**: 1.5× damage
- **Weather**: Sun/Rain boost Fire/Water
- **Items**: Life Orb (+30%), Choice Band (+50%)
- **Stat Boosts**: -6 to +6 stages

### Tips
✅ Check OHKO/2HKO predictions for team building  
✅ Test different items to optimize damage  
✅ Use stat boosts to simulate setup sweepers  
✅ Account for weather in team strategies  

---

## 🤖 Team Recommender (Tab 15)

### Access
```python
Navigate to: Tab 15 "🤖 Team Recommender"
```

### How to Build a Team
1. **Select Tier**: Choose competitive tier (OU, UU, etc.)
2. **Set Preferences**:
   - Role balance (Sweeper/Tank/Support)
   - Type coverage priority
   - Meta viability
3. **Add Seed Pokemon** (Optional): Build around favorites
4. **Generate**: AI creates optimized 6-Pokemon team
5. **Analyze**: Review type coverage and weaknesses
6. **Export**: Save as JSON or text

### Team Scoring
```
Score = (BST/10) + Type_Coverage(+50) + Weakness_Coverage(+30) + Usage(×5)
```

### Tips
✅ Use seed Pokemon to build around cores  
✅ Check type coverage chart for blind spots  
✅ Balance roles for versatile team  
✅ Consider meta picks for higher win rates  
✅ Export teams for external tools  

---

## 🎨 Image Optimizer (CLI Tool)

### Access
```bash
python scripts/optimize_images.py [directory] [options]
```

### Basic Usage
```bash
# Optimize all Pokemon sprites
python scripts/optimize_images.py assets --sprites-only

# Custom directory with options
python scripts/optimize_images.py path/to/images \
  --quality 90 \
  --workers 8 \
  --delete-originals
```

### Options
- `--quality [1-100]`: Output quality (default: 85)
- `--workers [N]`: Parallel threads (default: 4)
- `--delete-originals`: Remove original files
- `--sprites-only`: Process sprites directory only
- `--recursive`: Process subdirectories

### Expected Results
- **Size Reduction**: 50-70%
- **Processing Speed**: ~50 images/second
- **Format**: WebP (better compression)

### Tips
✅ Backup originals before using --delete-originals  
✅ Use quality 85-90 for best size/quality balance  
✅ More workers = faster processing (CPU dependent)  
✅ Test on small batch first  

---

## 📂 Data Requirements

### Meta Analytics
**Location**: `data/competitive/`

Required files:
- `tier_data.csv` - Pokemon tiers and rankings
- `usage_stats.csv` - Monthly usage statistics
- `move_usage.csv` - Move popularity data
- `ability_usage.csv` - Ability usage tracking

### Damage Calculator
**Location**: `data/`

Required files:
- `pokemon.csv` - Pokemon stats (HP, Attack, Defense, etc.)
- `moves/pokemon_movesets.json` - Move database

### Team Recommender
**Location**: `data/` and `data/competitive/`

Required files:
- `pokemon.csv` - Base Pokemon data
- `competitive/tier_data.csv` - Tier classifications
- `competitive/usage_stats.csv` - Meta rankings
- `moves/pokemon_movesets.json` - Available moves

---

## 🐛 Troubleshooting

### "Data file not found"
**Solution**: Ensure all CSV files exist in correct directories
```bash
# Check file structure
ls data/competitive/
ls data/moves/
```

### "Module not found"
**Solution**: Verify Python path and installations
```bash
pip install streamlit pandas plotly pillow
```

### "No data to display"
**Solution**: Check CSV files have data and correct format
```python
import pandas as pd
df = pd.read_csv('data/competitive/tier_data.csv')
print(df.head())
```

### Charts not rendering
**Solution**: Update Plotly
```bash
pip install --upgrade plotly
```

---

## ⌨️ Keyboard Shortcuts

### In Streamlit App
- `R` - Rerun app
- `C` - Clear cache
- `Q` - Toggle sidebar
- `S` - Toggle settings

### General Navigation
- `Ctrl + F` - Search within tab
- `Tab` - Navigate between inputs
- `Enter` - Submit forms

---

## 📊 Performance Tips

### For Best Performance

1. **Cache Data** ✅
   - Data loaded once per session
   - Cached with `@st.cache_data`

2. **Limit Results** ✅
   - Use filters to reduce data
   - Paginate large datasets

3. **Optimize Images** ✅
   - Run optimization script regularly
   - WebP reduces load times

4. **Close Unused Tabs** ✅
   - Each tab maintains state
   - Close to free memory

---

## 🔗 Quick Links

**Documentation**:
- [Phase 5 Implementation Guide](docs/guides/PHASE_5_IMPLEMENTATION.md)
- [Future Enhancements](docs/guides/FUTURE_ENHANCEMENTS.md)
- [Completion Report](docs/reports/PHASE_5_COMPLETION_REPORT.md)

**Testing**:
- [Test Suite](tests/test_phase5_features.py)

**Main Files**:
- [Main App](src/core/app.py)
- [Meta Dashboard](src/analytics/meta_dashboard.py)
- [Damage Calculator](src/analytics/damage_calculator.py)
- [Team Recommender](src/analytics/team_recommender.py)
- [Image Optimizer](scripts/optimize_images.py)

---

## 💡 Best Practices

### Meta Analysis
1. Check usage trends before team building
2. Identify rising threats early
3. Adapt to meta shifts
4. Export data for deeper analysis

### Damage Calculation
1. Account for all modifiers
2. Test multiple scenarios
3. Consider speed tiers
4. Plan for worst-case damage

### Team Building
1. Balance offensive and defensive types
2. Cover common threats in tier
3. Include at least one support Pokemon
4. Test team in damage calculator

### Image Optimization
1. Always backup originals first
2. Test quality settings on samples
3. Monitor file sizes
4. Verify images load correctly

---

## 📞 Support

**Issues?** Check:
1. [Troubleshooting section](#-troubleshooting)
2. [Implementation Guide](docs/guides/PHASE_5_IMPLEMENTATION.md)
3. [GitHub Issues](https://github.com/caalivanera/pokemon/issues)

**Questions?** Contact:
- GitHub: @caalivanera
- Repository: pokemon

---

**Quick Reference Card - v5.4.0**  
*Print this for quick access to Phase 5 features!*
