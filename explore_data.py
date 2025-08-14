#!/usr/bin/env python3

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
import pandas as pd

API_KEY = "17b867620e1b4ee78500f90f5c218ef1"
BASE_URL = "https://api.football-data.org/v4"

headers = {
    'X-Auth-Token': API_KEY,
    'Content-Type': 'application/json'
}

async def explore_api():
    """Explore the Football Data API to understand available data"""
    
    print("🚀 Exploring Football Data API...")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        
        # 1. Get available competitions
        print("\n1️⃣  AVAILABLE COMPETITIONS:")
        print("-" * 30)
        
        try:
            async with session.get(f"{BASE_URL}/competitions", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    competitions = data.get('competitions', [])
                    
                    for comp in competitions[:10]:  # Show first 10
                        print(f"📊 {comp['name']} ({comp['code']}) - ID: {comp['id']}")
                        print(f"   🌍 {comp['area']['name']} | Season: {comp.get('currentSeason', {}).get('startDate', 'N/A')}")
                        print()
                else:
                    print(f"❌ Error: {response.status} - {await response.text()}")
                    return
        except Exception as e:
            print(f"❌ Error fetching competitions: {e}")
            return
        
        # 2. Get Premier League details (ID: 2021)
        premier_league_id = 2021
        print(f"\n2️⃣  PREMIER LEAGUE TEAMS (ID: {premier_league_id}):")
        print("-" * 40)
        
        try:
            async with session.get(f"{BASE_URL}/competitions/{premier_league_id}/teams", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    teams = data.get('teams', [])
                    
                    for team in teams:
                        print(f"⚽ {team['name']} ({team['tla']}) - ID: {team['id']}")
                        print(f"   🏟️  Founded: {team.get('founded', 'N/A')} | Venue: {team.get('venue', 'N/A')}")
                        print()
                else:
                    print(f"❌ Error: {response.status}")
        except Exception as e:
            print(f"❌ Error fetching teams: {e}")
        
        # 3. Get recent Premier League matches
        print(f"\n3️⃣  RECENT PREMIER LEAGUE MATCHES:")
        print("-" * 35)
        
        date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        date_to = datetime.now().strftime('%Y-%m-%d')
        
        try:
            url = f"{BASE_URL}/competitions/{premier_league_id}/matches"
            params = {
                'status': 'FINISHED',
                'dateFrom': date_from,
                'dateTo': date_to
            }
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    matches = data.get('matches', [])
                    
                    print(f"Found {len(matches)} matches in last 30 days")
                    print()
                    
                    for match in matches[:5]:  # Show first 5
                        home = match['homeTeam']['name']
                        away = match['awayTeam']['name']
                        home_score = match['score']['fullTime']['home']
                        away_score = match['score']['fullTime']['away']
                        date = match['utcDate'][:10]
                        
                        print(f"📅 {date}: {home} {home_score}-{away_score} {away}")
                    
                    # Convert to DataFrame for analysis
                    if matches:
                        print(f"\n4️⃣  DATA ANALYSIS SAMPLE:")
                        print("-" * 25)
                        
                        df_data = []
                        for match in matches:
                            df_data.append({
                                'date': match['utcDate'][:10],
                                'home_team': match['homeTeam']['name'],
                                'away_team': match['awayTeam']['name'],
                                'home_score': match['score']['fullTime']['home'],
                                'away_score': match['score']['fullTime']['away'],
                                'total_goals': match['score']['fullTime']['home'] + match['score']['fullTime']['away']
                            })
                        
                        df = pd.DataFrame(df_data)
                        
                        print(f"🔢 Total matches: {len(df)}")
                        print(f"⚽ Average goals per match: {df['total_goals'].mean():.2f}")
                        print(f"🏠 Home wins: {len(df[df['home_score'] > df['away_score']])} ({len(df[df['home_score'] > df['away_score']])/len(df)*100:.1f}%)")
                        print(f"✈️  Away wins: {len(df[df['away_score'] > df['home_score']])} ({len(df[df['away_score'] > df['home_score']])/len(df)*100:.1f}%)")
                        print(f"🤝 Draws: {len(df[df['home_score'] == df['away_score']])} ({len(df[df['home_score'] == df['away_score']])/len(df)*100:.1f}%)")
                        
                        print(f"\n📊 Top scoring teams:")
                        home_goals = df.groupby('home_team')['home_score'].sum()
                        away_goals = df.groupby('away_team')['away_score'].sum()
                        total_goals = (home_goals + away_goals).fillna(0).sort_values(ascending=False)
                        
                        for team, goals in total_goals.head(5).items():
                            print(f"   {team}: {goals} goals")
                        
                else:
                    print(f"❌ Error: {response.status}")
        except Exception as e:
            print(f"❌ Error fetching matches: {e}")
        
        # 5. Show API rate limits
        print(f"\n5️⃣  API USAGE INFO:")
        print("-" * 20)
        print("🔑 Your API key allows:")
        print("   • 10 requests per minute")
        print("   • Access to major European leagues")
        print("   • Historical match data")
        print("   • Current season standings")
        print("   • Team and player information")

async def test_prediction_features():
    """Test the feature extraction that our ML model will use"""
    
    print(f"\n6️⃣  FEATURE EXTRACTION TEST:")
    print("-" * 30)
    
    # This simulates what our ML service does
    from app.data.football_api_client import FootballAPIClient
    from app.data.team_stats import TeamStatsService
    
    api_client = FootballAPIClient()
    stats_service = TeamStatsService()
    
    print("🧠 Testing feature extraction for: Arsenal vs Chelsea")
    
    try:
        # Get team features (using mock data for now since we need historical data)
        arsenal_features = await stats_service.get_team_features("Arsenal")
        chelsea_features = await stats_service.get_team_features("Chelsea")
        
        print(f"\n📈 Arsenal Features:")
        for key, value in arsenal_features.items():
            if isinstance(value, float):
                print(f"   {key}: {value:.3f}")
            else:
                print(f"   {key}: {value}")
        
        print(f"\n📉 Chelsea Features:")
        for key, value in chelsea_features.items():
            if isinstance(value, float):
                print(f"   {key}: {value:.3f}")
            else:
                print(f"   {key}: {value}")
        
        print(f"\n🎯 These features feed into our XGBoost model to predict:")
        print("   • Final score (home_score, away_score)")
        print("   • Win/Draw/Loss probabilities")
        print("   • Confidence score")
        
    except Exception as e:
        print(f"❌ Feature extraction error: {e}")

if __name__ == "__main__":
    print("🔍 FOOTBALL PREDICTION SYSTEM - DATA EXPLORATION")
    print("=" * 60)
    print(f"🔑 Using API Key: {API_KEY[:8]}...{API_KEY[-8:]}")
    print(f"🌐 Base URL: {BASE_URL}")
    
    asyncio.run(explore_api())
    asyncio.run(test_prediction_features())