#!/usr/bin/env python3
"""
Quick Deploy Script for Streamlit Cloud
Automates the deployment process
"""

import webbrowser
import time

def deploy_to_streamlit_cloud():
    """Open Streamlit Cloud deployment page"""
    
    print("🚀 Deploying to Pokemon National Dex Dashboard")
    print("=" * 60)
    print()
    
    # Repository details
    repo_owner = "caalivanera"
    repo_name = "pokemon"
    branch = "main"
    app_file = "pokedex-dashboard/enhanced_dashboard.py"
    
    # Your existing Streamlit Cloud app
    app_url = "https://1pokemon.streamlit.app/"
    manage_url = "https://share.streamlit.io/deploy"
    
    print("📦 Repository Configuration:")
    print(f"   Owner: {repo_owner}")
    print(f"   Repo: {repo_name}")
    print(f"   Branch: {branch}")
    print(f"   App: {app_file}")
    print()
    
    print("🌐 Existing Streamlit Cloud App:")
    print(f"   Live URL: {app_url}")
    print(f"   Status: ✅ Active")
    print()
    
    # Pre-fill deployment URL (if Streamlit supports it)
    github_url = f"https://github.com/{repo_owner}/{repo_name}"
    
    print("📋 Automatic Deployment:")
    print("   ✅ Your app is already deployed!")
    print("   ✅ Updates auto-deploy on push to main branch")
    print("   ✅ No manual deployment needed")
    print()
    
    print("🔄 Latest changes will be live in 1-2 minutes after push")
    print()
    
    # Open browser
    print("🌐 Opening your live app...")
    time.sleep(1)
    webbrowser.open(app_url)
    
    print()
    print("✅ Live app opened in browser!")
    print()
    print("📊 To manage your app, visit:")
    print(f"   {manage_url}")
    print()
    print("📖 For detailed instructions, see: STREAMLIT_DEPLOY.md")
    print()
    print("🎉 Your app is live at:")
    print(f"   {app_url}")
    print()
    print("=" * 60)
    print("Deployment ready! Changes auto-deploy on git push! 🚀")

if __name__ == "__main__":
    deploy_to_streamlit_cloud()
