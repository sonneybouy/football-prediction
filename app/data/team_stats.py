from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .football_api_client import FootballAPIClient

class TeamStatsService:
    def __init__(self):
        self.api_client = FootballAPIClient()
        self.cache = {}
    
    async def get_team_features(self, team_name: str) -> Dict:
        """Generate comprehensive features for a team"""
        if team_name in self.cache:
            return self.cache[team_name]
        
        # Get recent matches (last 10 games)
        recent_matches = await self._get_recent_matches(team_name, limit=10)
        
        # Calculate various statistics
        features = {
            'team': team_name,
            'avg_goals_scored': self._calculate_avg_goals_scored(recent_matches, team_name),
            'avg_goals_conceded': self._calculate_avg_goals_conceded(recent_matches, team_name),
            'home_advantage': self._calculate_home_advantage(recent_matches, team_name),
            'away_form': self._calculate_away_form(recent_matches, team_name),
            'recent_form': self._calculate_recent_form(recent_matches, team_name),
            'scoring_consistency': self._calculate_scoring_consistency(recent_matches, team_name),
            'defensive_stability': self._calculate_defensive_stability(recent_matches, team_name),
            'win_rate': self._calculate_win_rate(recent_matches, team_name),
            'draw_rate': self._calculate_draw_rate(recent_matches, team_name),
            'loss_rate': self._calculate_loss_rate(recent_matches, team_name),
            'goals_per_match_trend': self._calculate_goals_trend(recent_matches, team_name),
        }
        
        self.cache[team_name] = features
        return features
    
    async def _get_recent_matches(self, team_name: str, limit: int = 10) -> pd.DataFrame:
        """Mock function - in real implementation, query database or API"""
        # This is a placeholder - replace with actual data fetching
        mock_data = []
        for i in range(limit):
            is_home = i % 2 == 0
            mock_match = {
                'date': datetime.now() - timedelta(days=i*7),
                'home_team': team_name if is_home else f'Opponent_{i}',
                'away_team': f'Opponent_{i}' if is_home else team_name,
                'home_score': np.random.randint(0, 4),
                'away_score': np.random.randint(0, 4),
            }
            mock_data.append(mock_match)
        
        return pd.DataFrame(mock_data)
    
    def _calculate_avg_goals_scored(self, matches: pd.DataFrame, team: str) -> float:
        """Calculate average goals scored by team"""
        home_goals = matches[matches['home_team'] == team]['home_score'].mean()
        away_goals = matches[matches['away_team'] == team]['away_score'].mean()
        
        home_count = len(matches[matches['home_team'] == team])
        away_count = len(matches[matches['away_team'] == team])
        
        if home_count + away_count == 0:
            return 1.0
        
        total_goals = (home_goals * home_count + away_goals * away_count)
        return total_goals / (home_count + away_count)
    
    def _calculate_avg_goals_conceded(self, matches: pd.DataFrame, team: str) -> float:
        """Calculate average goals conceded by team"""
        home_conceded = matches[matches['home_team'] == team]['away_score'].mean()
        away_conceded = matches[matches['away_team'] == team]['home_score'].mean()
        
        home_count = len(matches[matches['home_team'] == team])
        away_count = len(matches[matches['away_team'] == team])
        
        if home_count + away_count == 0:
            return 1.0
        
        total_conceded = (home_conceded * home_count + away_conceded * away_count)
        return total_conceded / (home_count + away_count)
    
    def _calculate_home_advantage(self, matches: pd.DataFrame, team: str) -> float:
        """Calculate home performance advantage"""
        home_matches = matches[matches['home_team'] == team]
        if len(home_matches) == 0:
            return 0.0
        
        home_wins = len(home_matches[home_matches['home_score'] > home_matches['away_score']])
        return home_wins / len(home_matches)
    
    def _calculate_away_form(self, matches: pd.DataFrame, team: str) -> float:
        """Calculate away performance"""
        away_matches = matches[matches['away_team'] == team]
        if len(away_matches) == 0:
            return 0.0
        
        away_wins = len(away_matches[away_matches['away_score'] > away_matches['home_score']])
        return away_wins / len(away_matches)
    
    def _calculate_recent_form(self, matches: pd.DataFrame, team: str) -> float:
        """Calculate recent form (last 5 games weighted)"""
        recent_5 = matches.head(5)
        points = 0
        
        for _, match in recent_5.iterrows():
            if match['home_team'] == team:
                if match['home_score'] > match['away_score']:
                    points += 3
                elif match['home_score'] == match['away_score']:
                    points += 1
            else:  # away team
                if match['away_score'] > match['home_score']:
                    points += 3
                elif match['away_score'] == match['home_score']:
                    points += 1
        
        return points / 15.0  # Normalize to 0-1
    
    def _calculate_scoring_consistency(self, matches: pd.DataFrame, team: str) -> float:
        """Calculate scoring consistency (inverse of variance)"""
        goals_scored = []
        
        for _, match in matches.iterrows():
            if match['home_team'] == team:
                goals_scored.append(match['home_score'])
            else:
                goals_scored.append(match['away_score'])
        
        if len(goals_scored) == 0:
            return 0.5
        
        variance = np.var(goals_scored)
        return 1 / (1 + variance)  # Higher consistency = lower variance
    
    def _calculate_defensive_stability(self, matches: pd.DataFrame, team: str) -> float:
        """Calculate defensive stability (inverse of goals conceded variance)"""
        goals_conceded = []
        
        for _, match in matches.iterrows():
            if match['home_team'] == team:
                goals_conceded.append(match['away_score'])
            else:
                goals_conceded.append(match['home_score'])
        
        if len(goals_conceded) == 0:
            return 0.5
        
        variance = np.var(goals_conceded)
        return 1 / (1 + variance)
    
    def _calculate_win_rate(self, matches: pd.DataFrame, team: str) -> float:
        """Calculate win rate"""
        wins = 0
        total = 0
        
        for _, match in matches.iterrows():
            total += 1
            if match['home_team'] == team and match['home_score'] > match['away_score']:
                wins += 1
            elif match['away_team'] == team and match['away_score'] > match['home_score']:
                wins += 1
        
        return wins / total if total > 0 else 0.0
    
    def _calculate_draw_rate(self, matches: pd.DataFrame, team: str) -> float:
        """Calculate draw rate"""
        draws = 0
        total = 0
        
        for _, match in matches.iterrows():
            total += 1
            if match['home_score'] == match['away_score']:
                draws += 1
        
        return draws / total if total > 0 else 0.0
    
    def _calculate_loss_rate(self, matches: pd.DataFrame, team: str) -> float:
        """Calculate loss rate"""
        return 1.0 - self._calculate_win_rate(matches, team) - self._calculate_draw_rate(matches, team)
    
    def _calculate_goals_trend(self, matches: pd.DataFrame, team: str) -> float:
        """Calculate trend in goals per match over recent games"""
        goals_per_match = []
        
        for _, match in matches.iterrows():
            if match['home_team'] == team:
                goals_per_match.append(match['home_score'])
            else:
                goals_per_match.append(match['away_score'])
        
        if len(goals_per_match) < 2:
            return 0.0
        
        # Simple linear trend
        x = np.arange(len(goals_per_match))
        trend = np.polyfit(x, goals_per_match, 1)[0]
        return trend
    
    def get_head_to_head(self, team1: str, team2: str) -> Dict:
        """Get head-to-head statistics between two teams"""
        # Mock implementation - replace with actual data
        return {
            'home_wins': 3,
            'away_wins': 2,
            'draws': 1,
            'total_matches': 6,
            'avg_goals_team1': 1.5,
            'avg_goals_team2': 1.2
        }