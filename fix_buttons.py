#!/usr/bin/env python3
"""Fix gallery button keys to avoid duplicates"""

with open('src/core/app_premium.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the gallery loop to use unique button keys
old_code = """    for row in rows:
        cols = st.columns(cols_per_row)
        for idx, (_, pokemon) in enumerate(row.iterrows()):
            with cols[idx]:
                sprite_url = pokemon.get('sprite_url_hq', get_pokemon_sprite_url(
                    int(pokemon['pokedex_number']),
                    str(pokemon['name']),
                    high_quality=True
                ))
                st.markdown(create_pokemon_card_html(pokemon, sprite_url), unsafe_allow_html=True)
                if st.button(f"View Details", key=f"btn_{pokemon['pokedex_number']}", use_container_width=True):"""

new_code = """    for row_idx, row in enumerate(rows):
        cols = st.columns(cols_per_row)
        for col_idx, (pokemon_idx, pokemon) in enumerate(row.iterrows()):
            with cols[col_idx]:
                sprite_url = pokemon.get('sprite_url_hq', get_pokemon_sprite_url(
                    int(pokemon['pokedex_number']),
                    str(pokemon['name']),
                    high_quality=True
                ))
                st.markdown(create_pokemon_card_html(pokemon, sprite_url), unsafe_allow_html=True)
                if st.button(f"View Details", key=f"btn_gallery_{row_idx}_{col_idx}_{pokemon_idx}", use_container_width=True):"""

content = content.replace(old_code, new_code)

with open('src/core/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed gallery button keys successfully!")
