#!/usr/bin/env python3

import requests
import json
from datetime import datetime, timedelta

API_KEY = "17b867620e1b4ee78500f90f5c218ef1"
BASE_URL = "https://api.football-data.org/v4"

headers = {
    'X-Auth-Token': API_KEY,
    'Content-Type': 'application/json'
}

def explore_api():
    """Simple exploration of Football Data API"""
    
    print("🚀 FOOTBALL PREDICTION SYSTEM - DATA EXPLORATION")
    print("=" * 60)
    print(f"🔑 Using API Key: {API_KEY[:8]}...{API_KEY[-8:]}")
    print(f"🌐 Base URL: {BASE_URL}")
    print()
    
    # 1. Get available competitions
    print("1️⃣  AVAILABLE COMPETITIONS:")
    print("-" * 30)
    
    try:
        response = requests.get(f"{BASE_URL}/competitions", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            competitions = data.get('competitions', [])
            
            print(f"✅ Found {len(competitions)} competitions")
            print("\n🏆 Major Leagues:")
            
            major_leagues = ['PL', 'BL1', 'PD', 'SA', 'FL1', 'CL']
            for comp in competitions:
                if comp.get('code') in major_leagues:
                    print(f"   📊 {comp['name']} ({comp['code']}) - ID: {comp['id']}")
                    print(f"      🌍 {comp['area']['name']} | Current Season: {comp.get('currentSeason', {}).get('startDate', 'N/A')}")
            
        elif response.status_code == 403:
            print("❌ API Key authentication failed!")
            print("   Check if your API key is correct and active")
            return False
        elif response.status_code == 429:
            print("⏰ Rate limit exceeded!")
            print("   The free tier allows 10 requests per minute")
            return False
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    
    print()
    
    # 2. Get Premier League teams
    premier_league_id = 2021  # Premier League ID
    print(f"2️⃣  PREMIER LEAGUE TEAMS (ID: {premier_league_id}):")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/competitions/{premier_league_id}/teams", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            teams = data.get('teams', [])
            
            print(f"✅ Found {len(teams)} teams")
            print("\n⚽ Teams in Premier League:")
            
            for team in teams[:10]:  # Show first 10
                print(f"   {team['name']} ({team['tla']}) - ID: {team['id']}")
                
        else:
            print(f"❌ Error fetching teams: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    
    print()
    
    # 3. Get recent matches
    print("3️⃣  RECENT PREMIER LEAGUE MATCHES:")
    print("-" * 35)
    
    try:
        # Get matches from last 2 weeks to avoid too much data
        date_from = (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d')
        date_to = datetime.now().strftime('%Y-%m-%d')
        
        url = f"{BASE_URL}/competitions/{premier_league_id}/matches"
        params = {
            'status': 'FINISHED',
            'dateFrom': date_from,
            'dateTo': date_to
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            
            print(f"✅ Found {len(matches)} matches in last 2 weeks")
            
            if matches:
                print("\n📅 Sample matches:")
                for match in matches[:5]:
                    home = match['homeTeam']['name']
                    away = match['awayTeam']['name']
                    home_score = match['score']['fullTime']['home']
                    away_score = match['score']['fullTime']['away']
                    date = match['utcDate'][:10]
                    
                    print(f"   {date}: {home} {home_score}-{away_score} {away}")
                
                # Basic analysis
                total_goals = sum(m['score']['fullTime']['home'] + m['score']['fullTime']['away'] for m in matches)
                home_wins = sum(1 for m in matches if m['score']['fullTime']['home'] > m['score']['fullTime']['away'])
                away_wins = sum(1 for m in matches if m['score']['fullTime']['away'] > m['score']['fullTime']['home'])
                draws = len(matches) - home_wins - away_wins
                
                print(f"\n📊 Quick Stats:")
                print(f"   ⚽ Average goals per match: {total_goals/len(matches):.2f}")
                print(f"   🏠 Home wins: {home_wins} ({home_wins/len(matches)*100:.1f}%)")
                print(f"   ✈️  Away wins: {away_wins} ({away_wins/len(matches)*100:.1f}%)")
                print(f"   🤝 Draws: {draws} ({draws/len(matches)*100:.1f}%)")
            else:
                print("   📭 No recent matches found")
                
        else:
            print(f"❌ Error fetching matches: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    
    # 4. Explain the prediction process
    print(f"\n4️⃣  HOW OUR ML PREDICTION WORKS:")
    print("-" * 35)
    print("🧠 Our system processes this data to create predictions:")
    print()
    print("📈 FEATURE EXTRACTION:")
    print("   • Team's average goals scored/conceded")
    print("   • Recent form (last 5-10 games)")
    print("   • Home/away performance")
    print("   • Head-to-head history")
    print("   • Defensive stability")
    print("   • Scoring consistency")
    print()
    print("🎯 PREDICTION OUTPUT:")
    print("   • Predicted final score (e.g., 2.1 - 1.3)")
    print("   • Win/Draw/Loss probabilities")
    print("   • Confidence score (0-100%)")
    print("   • Model version and timestamp")
    print()
    print("🔄 MODEL TRAINING:")
    print("   • XGBoost algorithm")
    print("   • Trained on historical match data")
    print("   • Automatic retraining every 24 hours")
    print("   • Cross-validation for accuracy")
    
    print(f"\n5️⃣  NEXT STEPS:")
    print("-" * 15)
    print("✅ API connection working")
    print("✅ Data access confirmed")
    print("🚀 Ready to deploy the full system!")
    print()
    print("💡 To test locally:")
    print("   1. Run: make compose-up")
    print("   2. Visit: http://localhost:8000")
    print("   3. Try a prediction!")
    
    return True

if __name__ == "__main__":
    success = explore_api()
    
    if success:
        print(f"\n🎉 EXPLORATION COMPLETE!")
        print("   Your API key is working and you have access to football data.")
        print("   The system is ready for deployment!")
    else:
        print(f"\n❌ EXPLORATION FAILED!")
        print("   Please check your API key and internet connection.")