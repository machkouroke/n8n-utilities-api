import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from models.FootballAPI import MatchAPI
class TestMatchAPI(unittest.TestCase):
    @patch('requests.request')
    def test_summary(self, mock_request):
        # Mock response data
        mock_response_data = {
            'matches': [
                {
                    'utcDate': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%dT%H:%M:%S%z'),
                    'homeTeam': {'id': 1},
                    'awayTeam': {'id': 2},
                    'score': {'winner': 'HOME_TEAM' if i % 2 == 0 else 'AWAY_TEAM', 'fullTime': {'home': 2, 'away': 1}}
                } for i in range(10)
            ]
        }
        mock_request.return_value.json.return_value = mock_response_data

        result = MatchAPI.summary(teams_id='1', n=5)

        self.assertEqual(result.win.home, 3)
        self.assertEqual(result.win.away, 2)
        self.assertEqual(result.loss.home, 2)
        self.assertEqual(result.loss.away, 3)
        self.assertEqual(result.goal_scored.home, 6)
        self.assertEqual(result.goal_scored.away, 5)
        self.assertEqual(result.goal_conceded.home, 5)
        self.assertEqual(result.goal_conceded.away, 6)


if __name__ == '__main__':
    unittest.main()