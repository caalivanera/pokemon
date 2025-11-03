# 🧪 Testing Checklist - Pokemon Dashboard v5.0.0

## Pre-Testing Setup

- [ ] Ensure all sprite downloads are complete (check download_progress.json)
- [ ] Verify CSV loaded correctly: 1,130 entries in total
- [ ] Confirm app.py version shows 5.0.0
- [ ] Clear browser cache before testing
- [ ] Check all 12 tabs are visible

---

## 🌙 NEW FEATURE: Dark Mode Testing (v5.0.0)

### Dark Mode Toggle

- [ ] **Toggle Visibility**

  - Theme toggle appears in sidebar under "🌙 Theme"
  - Checkbox is clickable and responsive
- [ ] **Light to Dark Transition**

  - Click toggle to enable dark mode
  - Background changes to dark theme
  - Text remains readable (high contrast)
  - All cards/components update
  - Transition is smooth (no flashing)
- [ ] **Dark to Light Transition**

  - Click toggle to disable dark mode
  - Background changes to light theme
  - All elements revert to light styling
- [ ] **Persistence**

  - Enable dark mode
  - Refresh page
  - Dark mode setting persists
  - Same test for light mode

### Dark Mode UI Elements

- [ ] **Sidebar** - Proper dark styling
- [ ] **Cards** - Readable with dark background
- [ ] **Dataframes** - Proper contrast
- [ ] **Tabs** - Visible in dark mode
- [ ] **Buttons** - Hover effects work
- [ ] **Charts** - Legends readable
- [ ] **Inputs** - Form elements visible

---

## ⚡ NEW FEATURE: Type Calculator Testing (v5.0.0)

### Type Calculator Tab (Tab 9)

- [ ] **Tab Visibility**

  - "⚡ Type Calculator" tab appears
  - Tab loads without errors
- [ ] **Type Selection**

  - Attacking type dropdown works (18 types)
  - Primary defending type dropdown works
  - Secondary defending type dropdown works
  - "None" option available for secondary type
- [ ] **Damage Calculations**

  - [ ] **Super Effective (2x)**: Fire vs Grass = 2x
  - [ ] **Not Effective (0.5x)**: Fire vs Water = 0.5x
  - [ ] **No Effect (0x)**: Normal vs Ghost = 0x
  - [ ] **Neutral (1x)**: Fire vs Electric = 1x
  - [ ] **4x Damage**: Water vs Fire/Rock = 4x
  - [ ] **0.25x Damage**: Grass vs Fire/Steel = 0.25x
- [ ] **Coverage Analysis**

  - Offensive coverage list displays
  - Shows types hit super effectively
  - Defensive analysis displays
  - Shows weaknesses and resistances
- [ ] **Type Heatmap**

  - 18x18 heatmap renders
  - Color coding correct (red=effective, blue=not effective)
  - Hover shows multiplier values
  - Legend displays correctly

---

## 👥 NEW FEATURE: Team Builder Testing (v5.0.0)

### Team Builder Tab (Tab 10)

- [ ] **Tab Visibility**

  - "👥 Team Builder" tab appears
  - Tab loads without errors
- [ ] **Pokemon Selection**

  - Search bar filters Pokemon
  - Can type Pokemon name
  - Dropdown shows filtered results
  - Pokemon sprites display in results
- [ ] **Add/Remove Pokemon**

  - [ ] Add first Pokemon - Success message appears
  - [ ] Add second Pokemon - Team shows 2/6
  - [ ] Add six Pokemon - Team shows 6/6
  - [ ] Try adding 7th - Button disabled or error shown
  - [ ] Remove one Pokemon - Count updates
  - [ ] Clear team button works
- [ ] **Team Display**

  - Pokemon cards show correctly
  - Sprites display for each team member
  - Names and types visible
  - Remove button on each card works
- [ ] **Coverage Analysis**

  - Offensive coverage chart displays
  - Shows types team can hit
  - Defensive weaknesses shown
  - Resistances displayed
  - Coverage heatmap renders
- [ ] **Team Stats**

  - Average stats radar chart displays
  - HP, Attack, Defense, Sp.Atk, Sp.Def, Speed shown
  - Values accurate
- [ ] **Export Functionality**

  - Export button visible
  - Click exports JSON file
  - JSON contains team data

---

## 🔍 NEW FEATURE: Advanced Search Testing (v5.0.0)

### Pokemon Search Tab (Tab 2 - Enhanced)

- [ ] **Quick Search Bar**

  - Search bar appears at top
  - Type Pokemon name - instant filter
  - Type Pokemon number - instant filter
  - Clear search works
- [ ] **Advanced Filters Expander**

  - "🔧 Advanced Filters & Presets" expander visible
  - Click to expand - 4 tabs appear
  - Click to collapse - tabs hide

### Tab 1: Stats & BST

- [ ] BST range slider (min-max)
- [ ] HP range slider
- [ ] Attack range slider
- [ ] Speed range slider
- [ ] Results update in real-time

### Tab 2: Type & Ability

- [ ] Primary type filter dropdown
- [ ] Secondary type filter dropdown
- [ ] "Only Dual-Type" checkbox
- [ ] Ability search text input
- [ ] Ability type filter (All/Hidden/Single)

### Tab 3: Advanced

- [ ] Generation selector (Gen 1-9)
- [ ] Variant type multiselect
- [ ] Top N performers slider
- [ ] "Only Legendary/Mythical" checkbox

### Tab 4: Saved Filters (Presets)

- [ ] **Starter Pokemon Preset**

  - Click button
  - Shows all 27 starter Pokemon (9 gens × 3)
  - Bulbasaur, Charmander, Squirtle included
- [ ] **Pseudo-Legendaries Preset**

  - Click button
  - Shows Pokemon with BST=600
  - Dragonite, Tyranitar, Salamence included
- [ ] **Fast Attackers Preset**

  - Click button
  - Shows Speed 100+, Attack 100+
  - Results accurate
- [ ] **Tanks Preset**

  - Click button
  - Shows HP 100+, Def 80+, SpDef 80+
  - Snorlax, Blissey type Pokemon shown
- [ ] **Glass Cannons Preset**

  - Click button
  - Shows Attack 110+, Defense ≤70
  - Alakazam, Gengar type Pokemon shown

### Filter Summary

- [ ] Match count displays
- [ ] Percentage shown
- [ ] Updates with each filter change

---

## 📊 NEW FEATURE: Variant Statistics Testing (v5.0.0)

### Variant Statistics Tab (Tab 11)

- [ ] **Tab Visibility**

  - "📊 Variant Statistics" tab appears
  - Tab loads without errors
- [ ] **Overview Metrics**

  - Base Forms count displays
  - Variant Forms count displays
  - Total Forms displays (1,130)
  - Variant percentage shows

### Sub-Tab 1: Distribution

- [ ] Pie chart renders (variant types)
- [ ] Bar chart renders (variant counts)
- [ ] Breakdown table displays
- [ ] Percentages accurate

### Sub-Tab 2: Type Changes

- [ ] Type change list displays
- [ ] Shows Pokemon with type differences
- [ ] Base vs Variant types shown
- [ ] Frequency chart renders

### Sub-Tab 3: Stat Comparisons

- [ ] Pokemon selector works
- [ ] Multiple forms shown for selected Pokemon
- [ ] Stat comparison table displays
- [ ] Radar chart comparison renders
- [ ] Stat differences table accurate

### Sub-Tab 4: Mega Evolution

- [ ] Average stat boost chart displays
- [ ] BST distribution histogram renders
- [ ] Top 10 Mega Evolutions table shown
- [ ] Data accurate (Mega Rayquaza BST 780)

### Sub-Tab 5: Special Forms

- [ ] Regional forms pie chart
- [ ] Gigantamax forms list
- [ ] Other special forms tracked
- [ ] Counts accurate

---

## 🔥 Variant System Testing

### Base Functionality

- [ ] **App Loads Successfully**

  - Page loads in under 3 seconds
  - No error messages in console
  - All tabs render correctly
- [ ] **Data Loading**

  - Overview shows "1,130 Total Pokemon"
  - Overview shows "Variant Forms" metric
  - No missing data warnings

### Variant Switcher (Pokemon Search Tab)

#### Pokemon with Multiple Forms

- [ ] **Charizard (#6) - 4 Forms**

  - [ ] 4 tabs appear: Base, Mega Charizard X, Mega Charizard Y, Gigantamax Charizard
  - [ ] Base: Fire/Flying, 534 BST
  - [ ] Mega X: Fire/Dragon (type change!), 634 BST, Tough Claws ability
  - [ ] Mega Y: Fire/Flying, 634 BST, Drought ability
  - [ ] Gigantamax: Shows "G-Max Wildfire" move
  - [ ] Info boxes display Mega stones: "Charizardite X", "Charizardite Y"
  - [ ] All sprites load correctly (no broken images)
- [ ] **Mewtwo (#150) - 3 Forms**

  - [ ] 3 tabs appear: Base, Mega Mewtwo X, Mega Mewtwo Y
  - [ ] Base: Psychic, 680 BST
  - [ ] Mega X: Psychic/Fighting (type change!), 780 BST
  - [ ] Mega Y: Psychic, 780 BST
  - [ ] Info boxes display Mega stones correctly
- [ ] **Venusaur (#3) - 3 Forms**

  - [ ] 3 tabs: Base, Mega Venusaur, Gigantamax Venusaur
  - [ ] Mega shows "Venusaurite" stone
  - [ ] Gigantamax shows "G-Max Vine Lash" move
- [ ] **Pikachu (#25) - 2 Forms**

  - [ ] 2 tabs: Base, Gigantamax Pikachu
  - [ ] Gigantamax shows "G-Max Volt Crash" move
- [ ] **Raichu (#26) - 2 Forms**

  - [ ] 2 tabs: Base, Alolan Raichu
  - [ ] Alolan: Electric/Psychic (type change!)
  - [ ] Both sprites load correctly

#### Regional Forms

- [ ] **Alolan Rattata (#19)**

  - [ ] Type changes from Normal to Dark/Normal
  - [ ] Regional form badge appears
- [ ] **Galarian Weezing (#110)**

  - [ ] Type changes from Poison to Poison/Fairy
  - [ ] Regional form badge appears
- [ ] **Alolan Marowak (#105)**

  - [ ] Type changes from Ground to Fire/Ghost
  - [ ] Ability changes to Cursed Body

#### Single Form Pokemon

- [ ] **Bulbasaur (#1)**
  - [ ] Only shows base form (no tabs)
  - [ ] Card displays normally

---

## ✨ Shiny Mode Testing

### Toggle Functionality

- [ ] **Shiny Toggle in Sidebar**
  - [ ] Toggle appears and is clickable
  - [ ] Default state is OFF (unchecked)
  - [ ] Toggle state persists during session

### Shiny Sprites

- [ ] **Enable Shiny Mode**

  - [ ] All sprites in gallery change to shiny versions
  - [ ] Shiny badge (✨) appears on all sprites
  - [ ] Pokemon Search shows shiny sprites when toggled
- [ ] **Disable Shiny Mode**

  - [ ] All sprites revert to normal versions
  - [ ] Shiny badges disappear
- [ ] **Test Specific Pokemon**

  - [ ] Charizard shiny (black body, red wings)
  - [ ] Gyarados shiny (red instead of blue)
  - [ ] Metagross shiny (silver instead of blue)
  - [ ] Umbreon shiny (blue rings instead of yellow)

---

## 🎨 Sprite Gallery Testing

### Visual Badges

- [ ] **Mega Evolution Badge (🔥)**

  - [ ] Appears on all Mega evolution sprites
  - [ ] Correct color/styling
- [ ] **Regional Form Badge (🌍)**

  - [ ] Appears on Alolan forms
  - [ ] Appears on Galarian forms
- [ ] **Gigantamax Badge (⚡)**

  - [ ] Appears on all 32 Gigantamax forms
- [ ] **Shiny Badge (✨)**

  - [ ] Appears when shiny mode is ON
  - [ ] Can combine with other badges (e.g., 🔥✨ for Shiny Mega)

### Gallery Display

- [ ] **Sprite Loading**

  - [ ] All base sprites load (1-1025)
  - [ ] Variant sprites load with correct suffixes
  - [ ] Fallback works for missing sprites
- [ ] **Form Names**

  - [ ] Base forms show Pokemon name only
  - [ ] Variants show form name (e.g., "Mega Charizard X")
- [ ] **Sprite Limit Slider**

  - [ ] Slider appears and works (60-1025)
  - [ ] Gallery updates when slider changes
  - [ ] Performance acceptable at max limit

---

## 🔍 Filtering System

### Variant Type Filter

- [ ] **Select "Base Forms Only"**

  - [ ] Shows 1,025 Pokemon
  - [ ] No Mega/Regional/Gigantamax forms appear
- [ ] **Select "Mega Evolution" Only**

  - [ ] Shows ~50 Mega forms
  - [ ] Includes Mega X and Mega Y forms
  - [ ] All have 🔥 badge
- [ ] **Select "Regional Forms" Only**

  - [ ] Shows ~25 forms (Alolan + Galarian)
  - [ ] All have 🌍 badge
- [ ] **Select "Gigantamax" Only**

  - [ ] Shows 32 forms
  - [ ] All have ⚡ badge
- [ ] **Multiple Selections**

  - [ ] Can select Base + Mega (shows both)
  - [ ] Can select all types (shows all 1,130)
  - [ ] Filter counts update correctly

### Combined Filters

- [ ] **Type + Variant Filters**

  - [ ] Fire type + Mega evolution = Mega Charizard X/Y, etc.
  - [ ] Electric type + Regional = Alolan Raichu
- [ ] **Type + Shiny**

  - [ ] Fire type with shiny mode shows shiny Fire Pokemon

---

## 📊 Statistics & Overview

### Metrics Display

- [ ] **Total Pokemon Count**

  - [ ] Shows 1,130 (or filtered count)
  - [ ] Updates with filters
- [ ] **Variant Forms Metric**

  - [ ] Shows 105 variant forms
  - [ ] Displayed prominently
- [ ] **Type Distribution**

  - [ ] Chart includes variant types correctly
  - [ ] Mega Charizard X counted as Fire/Dragon

### Charts & Visualizations

- [ ] **Type Chart**

  - [ ] All 18 types represented
  - [ ] Dual types counted correctly
- [ ] **Generation Chart**

  - [ ] All 9 generations shown
  - [ ] Variants assigned to correct gen

---

## 🎬 Animated Sprites (If Downloaded)

- [ ] **Enable Animated Sprites Checkbox**

  - [ ] Checkbox appears in sidebar
  - [ ] Default state is OFF
- [ ] **Animated GIFs Display**

  - [ ] GIFs load in gallery
  - [ ] GIFs animate smoothly
  - [ ] Fallback to static if GIF missing
- [ ] **Performance**

  - [ ] Page doesn't lag with animations
  - [ ] Lazy loading works correctly

---

## ⚡ Performance Testing

### Load Times

- [ ] **Initial Page Load**

  - [ ] < 3 seconds on good connection
  - [ ] Shows loading indicator
- [ ] **Gallery Rendering**

  - [ ] 60 sprites: < 1 second
  - [ ] 120 sprites: < 2 seconds
  - [ ] 1025 sprites: < 5 seconds
- [ ] **Filter Changes**

  - [ ] Instant or near-instant updates
  - [ ] No lag when toggling filters

### Caching

- [ ] **Data Caching**

  - [ ] CSV loads once (check with st.cache_data)
  - [ ] Subsequent page visits faster
- [ ] **Sprite Caching**

  - [ ] Browser caches sprites
  - [ ] Repeated views much faster

---

## 📱 Mobile Responsiveness

### Layout

- [ ] **Mobile View (< 768px)**

  - [ ] Sidebar collapses correctly
  - [ ] Sprites stack vertically
  - [ ] Tabs work on mobile
- [ ] **Tablet View (768px - 1024px)**

  - [ ] Grid layout adapts
  - [ ] Touch targets adequate

### Touch Interactions

- [ ] **Variant Tabs**

  - [ ] Swipe between tabs works
  - [ ] Tap to switch tabs responsive
- [ ] **Shiny Toggle**

  - [ ] Easy to tap/toggle

---

## 🌐 Browser Compatibility

### Desktop Browsers

- [ ] **Chrome**

  - [ ] All features work
  - [ ] Sprites load correctly
- [ ] **Firefox**

  - [ ] All features work
  - [ ] Sprites load correctly
- [ ] **Edge**

  - [ ] All features work
  - [ ] Sprites load correctly
- [ ] **Safari** (if available)

  - [ ] All features work
  - [ ] Sprites load correctly

---

## 🐛 Edge Cases & Error Handling

### Missing Data

- [ ] **Missing Sprite**

  - [ ] Fallback image or placeholder shows
  - [ ] No broken image icons
  - [ ] Error logged but app continues
- [ ] **Invalid Variant Type**

  - [ ] Defaults to base form
  - [ ] No crash

### Large Datasets

- [ ] **All 1,130 Forms**
  - [ ] Gallery handles full dataset
  - [ ] Scrolling smooth
  - [ ] Memory usage acceptable

### Concurrent Filters

- [ ] **Multiple Active Filters**
  - [ ] Type + Variant + Generation = correct results
  - [ ] No duplicate entries

---

## 🎯 Variant-Specific Tests

### Mega Evolution Tests

- [ ] **All 48 Mega Evolutions Display**
  - [ ] Check 10 random Megas load correctly
  - [ ] Stats increase from base form
  - [ ] Mega stone info displays

### Regional Form Tests

- [ ] **Type Changes Work**
  - [ ] Alolan forms show new types
  - [ ] Galarian forms show new types

### Gigantamax Tests

- [ ] **G-Max Moves Display**
  - [ ] All 32 Gigantamax forms show signature move
  - [ ] Move names correct (e.g., "G-Max Wildfire")

---

## 📚 Documentation Verification

- [ ] **VARIANT_SYSTEM_GUIDE.md**

  - [ ] Accessible and readable
  - [ ] Instructions accurate
- [ ] **IMPLEMENTATION_PLAN.md**

  - [ ] Technical details correct
  - [ ] Data structure documented

---

## 🚀 Deployment Testing

### Streamlit Cloud

- [ ] **App Deploys Successfully**

  - [ ] No deployment errors
  - [ ] All files uploaded
- [ ] **Live App Functional**

  - [ ] All features work in production
  - [ ] Sprites load from assets folder
- [ ] **Performance on Cloud**

  - [ ] Load times acceptable
  - [ ] No timeout errors

---

## ✅ Final Sign-Off

### Critical Features

- [ ] Variant switcher works for all multi-form Pokemon
- [ ] Shiny mode toggles correctly
- [ ] All sprites load (or fallback gracefully)
- [ ] No critical errors in console
- [ ] Performance acceptable (< 3s initial load)

### Nice-to-Have Features

- [ ] Animated sprites work
- [ ] Mobile responsive
- [ ] All 1,130 entries display correctly

### Known Issues (Document Any)

- Issue 1: _____________________________________
- Issue 2: _____________________________________
- Issue 3: _____________________________________

---

## 📊 Test Results Summary

**Date Tested:** _____________
**Tester:** _____________
**Browser:** _____________
**Device:** _____________

**Total Tests:** _____
**Passed:** _____
**Failed:** _____
**Blocked:** _____

**Overall Status:** ⬜ PASS | ⬜ FAIL | ⬜ NEEDS REVIEW

**Notes:**

---

---

---

---

## 🎉 Post-Testing Actions

- [ ] Document all bugs found
- [ ] Create GitHub issues for bugs
- [ ] Update VARIANT_SYSTEM_GUIDE.md with findings
- [ ] Share results with team
- [ ] Plan optimization if needed
