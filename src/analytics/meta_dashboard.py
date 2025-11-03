"""
Enhanced Meta Analytics Dashboard
Provides comprehensive competitive Pokemon analysis
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np

class MetaAnalyticsDashboard:
    """Comprehensive analytics for competitive Pokemon meta"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.load_data()
    
    def load_data(self):
        """Load all competitive data sources"""
        try:
            self.tier_data = pd.read_csv(self.data_dir / "competitive" / "tier_data.csv")
            self.usage_stats = pd.read_csv(self.data_dir / "competitive" / "usage_stats.csv")
            self.move_usage = pd.read_csv(self.data_dir / "competitive" / "move_usage.csv")
            self.ability_usage = pd.read_csv(self.data_dir / "competitive" / "ability_usage.csv")
            self.pokemon_data = pd.read_csv(self.data_dir / "pokemon.csv")
            print("✅ All data loaded successfully")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def render_dashboard(self):
        """Main dashboard rendering function"""
        st.title("📊 Competitive Meta Analytics Dashboard")
        st.markdown("*Comprehensive analysis of competitive Pokemon data*")
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Usage Trends",
            "⚔️ Move Analysis", 
            "✨ Ability Stats",
            "🏆 Tier Distribution",
            "📊 Meta Insights"
        ])
        
        with tab1:
            self.render_usage_trends()
        
        with tab2:
            self.render_move_analysis()
        
        with tab3:
            self.render_ability_stats()
        
        with tab4:
            self.render_tier_distribution()
        
        with tab5:
            self.render_meta_insights()
    
    def render_usage_trends(self):
        """Visualize usage trends over time"""
        st.header("📈 Pokemon Usage Trends")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            available_months = sorted(self.usage_stats['month'].unique())
            selected_months = st.multiselect(
                "Select Months",
                available_months,
                default=available_months
            )
        
        with col2:
            top_n = st.slider("Show Top N Pokemon", 5, 20, 10)
        
        # Filter data
        filtered_usage = self.usage_stats[
            self.usage_stats['month'].isin(selected_months)
        ]
        
        # Get top Pokemon by average usage
        top_pokemon = (
            filtered_usage.groupby('pokemon')['usage_percent']
            .mean()
            .sort_values(ascending=False)
            .head(top_n)
            .index.tolist()
        )
        
        # Plot usage trends
        trend_data = filtered_usage[filtered_usage['pokemon'].isin(top_pokemon)]
        
        fig = px.line(
            trend_data,
            x='month',
            y='usage_percent',
            color='pokemon',
            title=f'Top {top_n} Pokemon Usage Trends',
            labels={'usage_percent': 'Usage %', 'month': 'Month'},
            markers=True
        )
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Usage statistics table
        st.subheader("📊 Usage Statistics")
        
        usage_summary = (
            filtered_usage.groupby('pokemon')
            .agg({
                'usage_percent': ['mean', 'min', 'max', 'std'],
                'rank': 'mean'
            })
            .round(2)
        )
        usage_summary.columns = ['Avg Usage %', 'Min %', 'Max %', 'Std Dev', 'Avg Rank']
        usage_summary = usage_summary.sort_values('Avg Usage %', ascending=False).head(20)
        
        st.dataframe(usage_summary, use_container_width=True)
        
        # Rising and falling Pokemon
        st.subheader("📈 Rising & Falling Pokemon")
        
        if len(selected_months) >= 2:
            rising, falling = self.calculate_trends(filtered_usage)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🚀 Rising Stars**")
                for pokemon, change in rising[:5]:
                    st.metric(pokemon, f"+{change:.1f}%", delta=f"+{change:.1f}%")
            
            with col2:
                st.markdown("**📉 Falling Titans**")
                for pokemon, change in falling[:5]:
                    st.metric(pokemon, f"{change:.1f}%", delta=f"{change:.1f}%")
    
    def calculate_trends(self, usage_data: pd.DataFrame) -> Tuple[List, List]:
        """Calculate rising and falling Pokemon"""
        months = sorted(usage_data['month'].unique())
        if len(months) < 2:
            return [], []
        
        first_month = months[0]
        last_month = months[-1]
        
        first_data = usage_data[usage_data['month'] == first_month].set_index('pokemon')
        last_data = usage_data[usage_data['month'] == last_month].set_index('pokemon')
        
        # Calculate change
        common_pokemon = first_data.index.intersection(last_data.index)
        changes = []
        
        for pokemon in common_pokemon:
            change = last_data.loc[pokemon, 'usage_percent'] - first_data.loc[pokemon, 'usage_percent']
            changes.append((pokemon, change))
        
        changes.sort(key=lambda x: x[1], reverse=True)
        
        rising = [c for c in changes if c[1] > 0][:10]
        falling = [c for c in changes if c[1] < 0][-10:]
        
        return rising, falling
    
    def render_move_analysis(self):
        """Analyze move usage patterns"""
        st.header("⚔️ Move Usage Analysis")
        
        # Move popularity
        st.subheader("Most Popular Moves")
        
        move_popularity = (
            self.move_usage.groupby('move')
            .agg({
                'usage_count': 'sum',
                'pokemon': 'count'
            })
            .rename(columns={'pokemon': 'pokemon_count'})
            .sort_values('usage_count', ascending=False)
            .head(20)
        )
        
        fig = px.bar(
            move_popularity.reset_index(),
            x='move',
            y='usage_count',
            title='Top 20 Most Used Moves',
            labels={'usage_count': 'Total Usage', 'move': 'Move'},
            color='usage_count',
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Move type distribution
        st.subheader("Move Type Distribution")
        
        if 'move_type' in self.move_usage.columns:
            type_dist = self.move_usage.groupby('move_type')['usage_count'].sum().sort_values(ascending=False)
            
            fig = px.pie(
                values=type_dist.values,
                names=type_dist.index,
                title='Move Usage by Type'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Move category analysis
        st.subheader("📊 Move Statistics Table")
        
        move_stats = (
            self.move_usage.groupby('move')
            .agg({
                'usage_count': 'sum',
                'pokemon': lambda x: ', '.join(x.unique()[:5])
            })
            .rename(columns={'pokemon': 'Used By (Top 5)'})
            .sort_values('usage_count', ascending=False)
            .head(30)
        )
        
        st.dataframe(move_stats, use_container_width=True)
    
    def render_ability_stats(self):
        """Analyze ability usage"""
        st.header("✨ Ability Usage Statistics")
        
        # Ability popularity
        ability_popularity = (
            self.ability_usage.groupby('ability')
            .agg({
                'usage_count': 'sum',
                'pokemon': 'count'
            })
            .rename(columns={'pokemon': 'unique_pokemon'})
            .sort_values('usage_count', ascending=False)
            .head(20)
        )
        
        fig = px.bar(
            ability_popularity.reset_index(),
            x='ability',
            y='usage_count',
            title='Top 20 Most Used Abilities',
            labels={'usage_count': 'Usage Count', 'ability': 'Ability'},
            color='usage_count',
            color_continuous_scale='plasma'
        )
        
        fig.update_layout(height=400, showlegend=False)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Ability statistics table
        st.subheader("📊 Detailed Ability Stats")
        
        ability_details = (
            self.ability_usage.groupby('ability')
            .agg({
                'usage_count': 'sum',
                'pokemon': lambda x: ', '.join(x.unique()[:5])
            })
            .rename(columns={'pokemon': 'Pokemon (Top 5)', 'usage_count': 'Total Usage'})
            .sort_values('Total Usage', ascending=False)
        )
        
        st.dataframe(ability_details, use_container_width=True)
    
    def render_tier_distribution(self):
        """Visualize tier distribution"""
        st.header("🏆 Tier Distribution Analysis")
        
        # Tier counts
        tier_counts = self.tier_data['tier'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                values=tier_counts.values,
                names=tier_counts.index,
                title='Pokemon Distribution by Tier'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                x=tier_counts.index,
                y=tier_counts.values,
                title='Pokemon Count by Tier',
                labels={'x': 'Tier', 'y': 'Count'},
                color=tier_counts.values,
                color_continuous_scale='reds'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Average stats by tier
        st.subheader("📊 Average Stats by Tier")
        
        # Merge with Pokemon data for stats
        tier_with_stats = self.tier_data.merge(
            self.pokemon_data[['name', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 'total_points']],
            left_on='pokemon',
            right_on='name',
            how='left'
        )
        
        stat_cols = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 'total_points']
        avg_stats = tier_with_stats.groupby('tier')[stat_cols].mean().round(1)
        
        st.dataframe(avg_stats, use_container_width=True)
        
        # Radar chart for tier comparison
        st.subheader("🎯 Tier Stats Comparison (Radar)")
        
        selected_tiers = st.multiselect(
            "Select Tiers to Compare",
            tier_counts.index.tolist(),
            default=tier_counts.index.tolist()[:3]
        )
        
        if selected_tiers:
            fig = go.Figure()
            
            for tier in selected_tiers:
                tier_stats = avg_stats.loc[tier, ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']]
                
                fig.add_trace(go.Scatterpolar(
                    r=tier_stats.values,
                    theta=['HP', 'Attack', 'Defense', 'Sp.Atk', 'Sp.Def', 'Speed'],
                    fill='toself',
                    name=tier
                ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 120])),
                showlegend=True,
                title="Average Stats by Tier"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def render_meta_insights(self):
        """Generate meta insights and recommendations"""
        st.header("📊 Meta Insights & Recommendations")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_pokemon = len(self.tier_data)
            st.metric("Total Ranked Pokemon", total_pokemon)
        
        with col2:
            total_moves = len(self.move_usage['move'].unique())
            st.metric("Unique Moves Used", total_moves)
        
        with col3:
            total_abilities = len(self.ability_usage['ability'].unique())
            st.metric("Unique Abilities", total_abilities)
        
        with col4:
            avg_usage = self.usage_stats['usage_percent'].mean()
            st.metric("Avg Usage %", f"{avg_usage:.2f}%")
        
        st.divider()
        
        # Meta analysis
        st.subheader("🎯 Current Meta Analysis")
        
        # Most dominant Pokemon
        st.markdown("**👑 Most Dominant Pokemon (Highest Average Usage)**")
        top_pokemon = (
            self.usage_stats.groupby('pokemon')['usage_percent']
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )
        
        for idx, (pokemon, usage) in enumerate(top_pokemon.items(), 1):
            st.write(f"{idx}. **{pokemon}** - {usage:.2f}% average usage")
        
        st.divider()
        
        # Type coverage recommendations
        st.subheader("⚔️ Type Coverage Insights")
        
        # Merge tier data with Pokemon data for type analysis
        tier_with_types = self.tier_data.merge(
            self.pokemon_data[['name', 'type_1', 'type_2']],
            left_on='pokemon',
            right_on='name',
            how='left'
        )
        
        # Count types
        type_counts = {}
        for _, row in tier_with_types.iterrows():
            type_counts[row['type_1']] = type_counts.get(row['type_1'], 0) + 1
            if pd.notna(row['type_2']):
                type_counts[row['type_2']] = type_counts.get(row['type_2'], 0) + 1
        
        type_df = pd.DataFrame(list(type_counts.items()), columns=['Type', 'Count']).sort_values('Count', ascending=False)
        
        fig = px.bar(
            type_df,
            x='Type',
            y='Count',
            title='Type Distribution in Competitive Play',
            color='Count',
            color_continuous_scale='blues'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Recommendations
        st.subheader("💡 Meta Recommendations")
        
        st.markdown("""
        **Based on current data analysis:**
        
        1. **Focus on Top Tiers**: OU and Uber tiers contain the most used Pokemon
        2. **Coverage Moves**: The most popular moves provide excellent type coverage
        3. **Ability Synergy**: Top abilities often synergize with common team compositions
        4. **Balanced Teams**: Consider both offensive and defensive capabilities
        5. **Meta Adaptation**: Monitor usage trends to adapt your team
        """)
        
        # Export options
        st.divider()
        st.subheader("📥 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export Full Analysis"):
                st.info("Analysis export feature - coming soon!")
        
        with col2:
            if st.button("📈 Generate Report"):
                st.info("Report generation feature - coming soon!")


def main():
    """Main function for standalone testing"""
    st.set_page_config(page_title="Meta Analytics", layout="wide", page_icon="📊")
    
    dashboard = MetaAnalyticsDashboard()
    dashboard.render_dashboard()


if __name__ == "__main__":
    main()
