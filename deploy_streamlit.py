#!/usr/bin/env python3
"""
Quick Deploy Script for Streamlit Cloud
Automates the deployment process
"""

import webbrowser
import time

def deploy_to_streamlit_cloud():
    """Open Streamlit Cloud deployment page"""
    
    print("🚀 Deploying Pokemon National Dex Dashboard to Streamlit Cloud")
    print("=" * 60)
    print()
    
    # Repository details
    repo_owner = "caalivanera"
    repo_name = "pokemon"
    branch = "main"
    app_file = "pokedex-dashboard/enhanced_dashboard.py"
    
    print("📦 Repository Configuration:")
    print(f"   Owner: {repo_owner}")
    print(f"   Repo: {repo_name}")
    print(f"   Branch: {branch}")
    print(f"   App: {app_file}")
    print()
    
    # Streamlit Cloud URLs
    streamlit_cloud_url = "https://share.streamlit.io/"
    
    # Pre-fill deployment URL (if Streamlit supports it)
    github_url = f"https://github.com/{repo_owner}/{repo_name}"
    
    print("🌐 Opening Streamlit Cloud Dashboard...")
    print(f"   URL: {streamlit_cloud_url}")
    print()
    
    print("📋 Deployment Steps:")
    print("   1. Sign in with GitHub")
    print("   2. Click 'New app'")
    print("   3. Enter repository details:")
    print(f"      - Repository: {github_url}")
    print(f"      - Branch: {branch}")
    print(f"      - Main file: {app_file}")
    print("   4. Click 'Deploy!'")
    print()
    
    print("⏱️  Expected deployment time: 2-3 minutes")
    print()
    
    # Open browser
    print("🌐 Opening browser...")
    time.sleep(1)
    webbrowser.open(streamlit_cloud_url)
    
    print()
    print("✅ Streamlit Cloud dashboard opened!")
    print()
    print("📖 For detailed instructions, see: STREAMLIT_DEPLOY.md")
    print()
    print("🎉 Your app will be available at:")
    print("   https://[your-subdomain].streamlit.app")
    print()
    print("=" * 60)
    print("Happy deploying! 🚀")

if __name__ == "__main__":
    deploy_to_streamlit_cloud()
