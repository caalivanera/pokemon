"""
Fix Pokemon Legends: Z-A game availability data
Based on official Kalos Regional Pokedex from Bulbapedia
Total: 457 unique Pokemon species across three sub-dexes
"""

import json

# Official Kalos Regional Pokedex - 457 Pokemon total
# Source: https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_Kalos_Pokédex_number

KALOS_POKEDEX = {
    # Central Kalos Pokédex (153 Pokemon)
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28,
    29, 30, 31, 32, 33, 34, 39, 40, 41, 42, 43, 44, 45, 54, 55, 60, 61, 62, 63, 64, 65, 79, 80, 83, 84,
    85, 102, 103, 108, 118, 119, 129, 130, 143, 161, 162, 165, 166, 172, 182, 183, 184, 187, 188, 189,
    206, 235, 263, 264, 280, 281, 282, 283, 284, 290, 291, 292, 293, 294, 295, 298, 300, 301, 307, 308,
    311, 312, 313, 314, 315, 316, 317, 318, 319, 352, 358, 359, 399, 400, 406, 407, 412, 413, 414, 415,
    416, 417, 439, 441, 446, 447, 448, 453, 454, 475, 511, 512, 513, 514, 515, 516, 531, 543, 544, 545,
    559, 560, 580, 581, 587, 610, 611, 612, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661,
    662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681,
    682, 683, 684, 685, 686, 687, 719, 720, 721,
    
    # Coastal Kalos Pokédex (153 Pokemon)
    29, 30, 31, 32, 33, 34, 72, 73, 79, 80, 90, 91, 102, 103, 104, 105, 111, 112, 115, 116, 117, 120,
    121, 122, 127, 128, 131, 133, 134, 135, 136, 144, 145, 146, 170, 171, 179, 180, 181, 193, 196, 197,
    199, 202, 209, 210, 211, 222, 223, 224, 226, 228, 229, 230, 241, 276, 277, 278, 279, 296, 297, 299,
    302, 303, 309, 310, 320, 321, 325, 326, 335, 336, 337, 338, 341, 342, 366, 367, 368, 369, 370, 371,
    372, 373, 396, 397, 398, 417, 418, 419, 425, 426, 433, 434, 435, 438, 441, 443, 444, 445, 449, 450,
    458, 462, 464, 469, 470, 471, 476, 524, 525, 526, 527, 528, 538, 539, 551, 552, 553, 557, 558, 561,
    577, 578, 579, 589, 594, 597, 598, 616, 617, 619, 620, 622, 623, 688, 689, 690, 691, 692, 693, 694,
    695, 696, 697, 698, 699, 700, 701, 702, 703, 144, 145, 146,
    
    # Mountain Kalos Pokédex (151 Pokemon)
    21, 22, 23, 24, 27, 28, 50, 51, 60, 61, 62, 69, 70, 71, 74, 75, 76, 81, 82, 92, 93, 94, 95, 100,
    101, 108, 123, 132, 147, 148, 149, 150, 163, 164, 167, 168, 174, 185, 186, 194, 195, 198, 207, 213,
    215, 216, 217, 218, 219, 220, 221, 225, 227, 238, 246, 247, 248, 261, 262, 270, 271, 272, 304, 305,
    306, 324, 327, 328, 329, 330, 333, 334, 339, 340, 353, 354, 360, 418, 419, 430, 438, 443, 444, 445,
    451, 452, 455, 459, 460, 461, 472, 473, 479, 504, 505, 509, 510, 532, 533, 534, 550, 568, 569, 570,
    571, 574, 575, 576, 582, 583, 584, 588, 590, 591, 607, 608, 609, 613, 614, 615, 618, 621, 624, 625,
    631, 632, 633, 634, 635, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718,
}

def fix_legends_za_data():
    """Update comprehensive_game_data.json with correct Kalos Pokedex"""
    
    # Read the current data
    with open('data/enhanced/comprehensive_game_data.json', 'r', encoding='utf-8') as f:
        game_data = f.read()
        game_data = json.loads(game_data)
    
    print(f"📊 Total Pokemon in database: {len(game_data)}")
    print(f"✅ Official Kalos Pokedex: {len(KALOS_POKEDEX)} Pokemon")
    
    # Reset all legends-z-a tags first
    removed_count = 0
    for pokemon in game_data:
        games = pokemon.get('games', [])
        if 'legends-z-a' in games:
            games.remove('legends-z-a')
            removed_count += 1
    
    print(f"🔄 Removed old legends-z-a tags: {removed_count}")
    
    # Add legends-z-a tag only to Pokemon in the official Kalos Pokedex
    updated_count = 0
    for pokemon in game_data:
        dex_num = pokemon.get('pokedex_number', 0)
        games = pokemon.get('games', [])
        
        # Check if this Pokemon is in the official Kalos Pokedex
        if dex_num in KALOS_POKEDEX:
            if 'legends-z-a' not in games:
                games.append('legends-z-a')
                updated_count += 1
                pokemon['games'] = games
    
    # Save updated data
    with open('data/enhanced/comprehensive_game_data.json', 'w', encoding='utf-8') as f:
        json.dump(game_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Added legends-z-a to {updated_count} Pokemon")
    print(f"✅ Updated data/enhanced/comprehensive_game_data.json")
    print(f"\n📊 Summary:")
    print(f"   - Official Kalos Pokedex: {len(KALOS_POKEDEX)} Pokemon")
    print(f"   - Central Kalos: 153 Pokemon")
    print(f"   - Coastal Kalos: 153 Pokemon")
    print(f"   - Mountain Kalos: 151 Pokemon")
    print(f"   - Total unique species: 457 Pokemon")

if __name__ == '__main__':
    fix_legends_za_data()
