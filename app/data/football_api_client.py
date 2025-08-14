import aiohttp
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd
from ..core.config import settings

class FootballAPIClient:
    def __init__(self):
        self.api_key = settings.football_api_key
        self.base_url = settings.football_api_url
        self.headers = {
            'X-Auth-Token': self.api_key,
            'Content-Type': 'application/json'
        }
    
    async def get_competitions(self) -> List[Dict]:
        """Fetch available competitions/leagues"""
        url = f"{self.base_url}/competitions"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                data = await response.json()
                return data.get('competitions', [])
    
    async def get_teams(self, competition_id: int) -> List[Dict]:
        """Fetch teams in a competition"""
        url = f"{self.base_url}/competitions/{competition_id}/teams"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                data = await response.json()
                return data.get('teams', [])
    
    async def get_matches(
        self, 
        competition_id: int,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        status: str = "FINISHED"
    ) -> List[Dict]:
        """Fetch matches for a competition"""
        url = f"{self.base_url}/competitions/{competition_id}/matches"
        params = {'status': status}
        
        if date_from:
            params['dateFrom'] = date_from.strftime('%Y-%m-%d')
        if date_to:
            params['dateTo'] = date_to.strftime('%Y-%m-%d')
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as response:
                data = await response.json()
                return data.get('matches', [])
    
    async def get_team_matches(
        self, 
        team_id: int,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Fetch matches for a specific team"""
        url = f"{self.base_url}/teams/{team_id}/matches"
        params = {'limit': limit, 'status': 'FINISHED'}
        
        if date_from:
            params['dateFrom'] = date_from.strftime('%Y-%m-%d')
        if date_to:
            params['dateTo'] = date_to.strftime('%Y-%m-%d')
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as response:
                data = await response.json()
                return data.get('matches', [])
    
    async def get_standings(self, competition_id: int) -> Dict:
        """Fetch current standings for a competition"""
        url = f"{self.base_url}/competitions/{competition_id}/standings"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                data = await response.json()
                return data
    
    def normalize_match_data(self, raw_matches: List[Dict]) -> pd.DataFrame:
        """Convert raw API match data to normalized DataFrame"""
        matches = []
        
        for match in raw_matches:
            normalized_match = {
                'id': match.get('id'),
                'date': match.get('utcDate'),
                'home_team': match.get('homeTeam', {}).get('name'),
                'away_team': match.get('awayTeam', {}).get('name'),
                'home_team_id': match.get('homeTeam', {}).get('id'),
                'away_team_id': match.get('awayTeam', {}).get('id'),
                'home_score': match.get('score', {}).get('fullTime', {}).get('home'),
                'away_score': match.get('score', {}).get('fullTime', {}).get('away'),
                'half_time_home': match.get('score', {}).get('halfTime', {}).get('home'),
                'half_time_away': match.get('score', {}).get('halfTime', {}).get('away'),
                'competition': match.get('competition', {}).get('name'),
                'season': match.get('season', {}).get('startDate'),
                'matchday': match.get('matchday'),
                'status': match.get('status'),
            }
            matches.append(normalized_match)
        
        df = pd.DataFrame(matches)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df = df.dropna(subset=['home_score', 'away_score'])
        
        return df