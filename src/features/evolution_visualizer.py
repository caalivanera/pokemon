"""
Evolution Chain Visualizer
Interactive visualization of Pokemon evolution chains
Version 1.0.0
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from typing import Dict, List, Tuple, Optional


# Evolution data - comprehensive mapping of evolution chains
# Format: pokemon_name: [(evolves_to, method, level/item/condition)]
EVOLUTION_CHAINS = {
    # Gen 1 Starters
    "bulbasaur": [("ivysaur", "level", 16)],
    "ivysaur": [("venusaur", "level", 32)],
    "charmander": [("charmeleon", "level", 16)],
    "charmeleon": [("charizard", "level", 36)],
    "squirtle": [("wartortle", "level", 16)],
    "wartortle": [("blastoise", "level", 36)],
    
    # Gen 1 Common
    "caterpie": [("metapod", "level", 7)],
    "metapod": [("butterfree", "level", 10)],
    "weedle": [("kakuna", "level", 7)],
    "kakuna": [("beedrill", "level", 10)],
    "pidgey": [("pidgeotto", "level", 18)],
    "pidgeotto": [("pidgeot", "level", 36)],
    "rattata": [("raticate", "level", 20)],
    "spearow": [("fearow", "level", 20)],
    "ekans": [("arbok", "level", 22)],
    "pikachu": [("raichu", "thunder stone", None)],
    "sandshrew": [("sandslash", "level", 22)],
    "nidoran-f": [("nidorina", "level", 16)],
    "nidorina": [("nidoqueen", "moon stone", None)],
    "nidoran-m": [("nidorino", "level", 16)],
    "nidorino": [("nidoking", "moon stone", None)],
    "clefairy": [("clefable", "moon stone", None)],
    "vulpix": [("ninetales", "fire stone", None)],
    "jigglypuff": [("wigglytuff", "moon stone", None)],
    "zubat": [("golbat", "level", 22)],
    "oddish": [("gloom", "level", 21)],
    "gloom": [("vileplume", "leaf stone", None), ("bellossom", "sun stone", None)],
    "paras": [("parasect", "level", 24)],
    "venonat": [("venomoth", "level", 31)],
    "diglett": [("dugtrio", "level", 26)],
    "meowth": [("persian", "level", 28)],
    "psyduck": [("golduck", "level", 33)],
    "mankey": [("primeape", "level", 28)],
    "growlithe": [("arcanine", "fire stone", None)],
    "poliwag": [("poliwhirl", "level", 25)],
    "poliwhirl": [("poliwrath", "water stone", None), ("politoed", "trade + kings rock", None)],
    "abra": [("kadabra", "level", 16)],
    "kadabra": [("alakazam", "trade", None)],
    "machop": [("machoke", "level", 28)],
    "machoke": [("machamp", "trade", None)],
    "bellsprout": [("weepinbell", "level", 21)],
    "weepinbell": [("victreebel", "leaf stone", None)],
    "tentacool": [("tentacruel", "level", 30)],
    "geodude": [("graveler", "level", 25)],
    "graveler": [("golem", "trade", None)],
    "ponyta": [("rapidash", "level", 40)],
    "slowpoke": [("slowbro", "level", 37), ("slowking", "trade + kings rock", None)],
    "magnemite": [("magneton", "level", 30)],
    "doduo": [("dodrio", "level", 31)],
    "seel": [("dewgong", "level", 34)],
    "grimer": [("muk", "level", 38)],
    "shellder": [("cloyster", "water stone", None)],
    "gastly": [("haunter", "level", 25)],
    "haunter": [("gengar", "trade", None)],
    "onix": [("steelix", "trade + metal coat", None)],
    "drowzee": [("hypno", "level", 26)],
    "krabby": [("kingler", "level", 28)],
    "voltorb": [("electrode", "level", 30)],
    "exeggcute": [("exeggutor", "leaf stone", None)],
    "cubone": [("marowak", "level", 28)],
    "koffing": [("weezing", "level", 35)],
    "rhyhorn": [("rhydon", "level", 42)],
    "horsea": [("seadra", "level", 32)],
    "goldeen": [("seaking", "level", 33)],
    "staryu": [("starmie", "water stone", None)],
    "magikarp": [("gyarados", "level", 20)],
    "eevee": [
        ("vaporeon", "water stone", None),
        ("jolteon", "thunder stone", None),
        ("flareon", "fire stone", None),
        ("espeon", "friendship (day)", None),
        ("umbreon", "friendship (night)", None),
        ("leafeon", "leaf stone", None),
        ("glaceon", "ice stone", None),
        ("sylveon", "friendship + fairy move", None)
    ],
    "omanyte": [("omastar", "level", 40)],
    "kabuto": [("kabutops", "level", 40)],
    "dratini": [("dragonair", "level", 30)],
    "dragonair": [("dragonite", "level", 55)],
    
    # Gen 2
    "chikorita": [("bayleef", "level", 16)],
    "bayleef": [("meganium", "level", 32)],
    "cyndaquil": [("quilava", "level", 14)],
    "quilava": [("typhlosion", "level", 36)],
    "totodile": [("croconaw", "level", 18)],
    "croconaw": [("feraligatr", "level", 30)],
    "sentret": [("furret", "level", 15)],
    "hoothoot": [("noctowl", "level", 20)],
    "ledyba": [("ledian", "level", 18)],
    "spinarak": [("ariados", "level", 22)],
    "chinchou": [("lanturn", "level", 27)],
    "pichu": [("pikachu", "friendship", None)],
    "cleffa": [("clefairy", "friendship", None)],
    "igglybuff": [("jigglypuff", "friendship", None)],
    "togepi": [("togetic", "friendship", None)],
    "togetic": [("togekiss", "shiny stone", None)],
    "natu": [("xatu", "level", 25)],
    "mareep": [("flaaffy", "level", 15)],
    "flaaffy": [("ampharos", "level", 30)],
    "marill": [("azumarill", "level", 18)],
    "sudowoodo": [("sudowoodo", "none", None)],
    "hoppip": [("skiploom", "level", 18)],
    "skiploom": [("jumpluff", "level", 27)],
    "aipom": [("ambipom", "level + double hit", 32)],
    "sunkern": [("sunflora", "sun stone", None)],
    "yanma": [("yanmega", "level + ancient power", 33)],
    "wooper": [("quagsire", "level", 20)],
    "murkrow": [("honchkrow", "dusk stone", None)],
    "misdreavus": [("mismagius", "dusk stone", None)],
    "gligar": [("gliscor", "level + razor fang (night)", None)],
    "snubbull": [("granbull", "level", 23)],
    "teddiursa": [("ursaring", "level", 30)],
    "slugma": [("magcargo", "level", 38)],
    "swinub": [("piloswine", "level", 33)],
    "piloswine": [("mamoswine", "level + ancient power", 33)],
    "remoraid": [("octillery", "level", 25)],
    "houndour": [("houndoom", "level", 24)],
    "phanpy": [("donphan", "level", 25)],
    "tyrogue": [
        ("hitmonlee", "level 20 (attack > defense)", 20),
        ("hitmonchan", "level 20 (defense > attack)", 20),
        ("hitmontop", "level 20 (attack = defense)", 20)
    ],
    "smoochum": [("jynx", "level", 30)],
    "elekid": [("electabuzz", "level", 30)],
    "electabuzz": [("electivire", "trade + electirizer", None)],
    "magby": [("magmar", "level", 30)],
    "magmar": [("magmortar", "trade + magmarizer", None)],
    "larvitar": [("pupitar", "level", 30)],
    "pupitar": [("tyranitar", "level", 55)],
    
    # Gen 3 Starters
    "treecko": [("grovyle", "level", 16)],
    "grovyle": [("sceptile", "level", 36)],
    "torchic": [("combusken", "level", 16)],
    "combusken": [("blaziken", "level", 36)],
    "mudkip": [("marshtomp", "level", 16)],
    "marshtomp": [("swampert", "level", 36)],
    
    # More can be added...
}


def get_evolution_chain(pokemon_name: str) -> Dict:
    """
    Get the full evolution chain for a Pokemon
    
    Args:
        pokemon_name: Pokemon name (lowercase)
        
    Returns:
        Dictionary with evolution chain data
    """
    # Find the base form
    base_form = pokemon_name.lower()
    
    # Check if this pokemon evolves FROM something
    for base, evolutions in EVOLUTION_CHAINS.items():
        for evolve_to, _, _ in evolutions:
            if evolve_to == base_form:
                base_form = base
                break
    
    # Build the chain from base
    chain = {"base": base_form, "evolutions": []}
    
    def build_chain_recursive(current_name, level=0):
        if current_name in EVOLUTION_CHAINS:
            for evolve_to, method, condition in EVOLUTION_CHAINS[current_name]:
                evolution_data = {
                    "name": evolve_to,
                    "method": method,
                    "condition": condition,
                    "level": level + 1,
                    "next": []
                }
                build_chain_recursive(evolve_to, level + 1)
                chain["evolutions"].append(evolution_data)
    
    build_chain_recursive(base_form)
    return chain


def create_evolution_graph(chain: Dict) -> go.Figure:
    """
    Create a Plotly graph visualization of evolution chain
    
    Args:
        chain: Evolution chain dictionary
        
    Returns:
        Plotly Figure object
    """
    G = nx.DiGraph()
    
    # Add base node
    base = chain["base"].title()
    G.add_node(base, level=0)
    
    # Add evolution nodes
    for evo in chain["evolutions"]:
        evo_name = evo["name"].title()
        method_text = evo["method"]
        if evo["condition"]:
            method_text += f" {evo['condition']}"
        
        G.add_node(evo_name, level=evo["level"])
        G.add_edge(base, evo_name, method=method_text)
    
    # Create layout
    pos = nx.spring_layout(G, seed=42, k=2)
    
    # Extract node positions
    node_x = []
    node_y = []
    node_text = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
    
    # Extract edge positions
    edge_x = []
    edge_y = []
    edge_text = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        # Get method text
        method = G.edges[edge].get("method", "")
        edge_text.append(method)
    
    # Create traces
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="top center",
        marker=dict(
            showscale=False,
            color='#22c55e',
            size=30,
            line=dict(width=2, color='white')))
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title='Evolution Chain',
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=0, l=0, r=0, t=40),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       height=400
                   ))
    
    return fig


def display_evolution_chain_tab(df: pd.DataFrame):
    """
    Display the evolution chain visualizer tab
    
    Args:
        df: Main Pokemon DataFrame
    """
    st.markdown("### 🔄 Evolution Chain Visualizer")
    st.caption("Explore Pokemon evolution chains with interactive graphs")
    
    # Pokemon selector
    pokemon_list = sorted(df['name'].str.lower().unique())
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_pokemon = st.selectbox(
            "Select a Pokemon",
            pokemon_list,
            format_func=lambda x: x.title(),
            key="evo_chain_selector"
        )
    
    with col2:
        show_graph = st.checkbox("Show Graph", value=True)
    
    if selected_pokemon:
        chain = get_evolution_chain(selected_pokemon)
        
        st.markdown("---")
        
        # Display evolution info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### Base Form: {chain['base'].title()}")
            
            if chain["evolutions"]:
                st.markdown("#### Evolution Path:")
                for evo in chain["evolutions"]:
                    method_text = evo["method"].title()
                    if evo["condition"]:
                        method_text += f" ({evo['condition']})"
                    st.markdown(f"- **{evo['name'].title()}** via {method_text}")
            else:
                st.info("This Pokemon does not evolve")
        
        with col2:
            if show_graph and chain["evolutions"]:
                fig = create_evolution_graph(chain)
                st.plotly_chart(fig, use_container_width=True)
        
        # Evolution details table
        if chain["evolutions"]:
            st.markdown("---")
            st.markdown("#### Evolution Methods")
            
            evo_data = []
            for evo in chain["evolutions"]:
                evo_data.append({
                    "Pokemon": evo["name"].title(),
                    "Method": evo["method"].title(),
                    "Condition": evo["condition"] if evo["condition"] else "—"
                })
            
            evo_df = pd.DataFrame(evo_data)
            st.dataframe(evo_df, use_container_width=True, hide_index=True)
