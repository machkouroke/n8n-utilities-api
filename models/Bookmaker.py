from pprint import pprint

from pydantic import BaseModel


class Outcome(BaseModel):
    value: str
    odd: float


class Bets(BaseModel):
    name: str
    values: list[Outcome]


class Bookmaker(BaseModel):
    name: str
    bets: list[Bets]

    @staticmethod
    def to_bookmaker(data: dict) -> 'Bookmaker':
        name = data["name"]
        bets = []
        for bet in data["bets"]:
            bet_name = bet["name"]
            if data["name"] == 'Unibet' or bet_name == 'Match Winner':
                bet_outcome = []

                for odd in bet["values"]:
                    bet_outcome.append(Outcome(value=odd["value"], odd=float(odd["odd"])))
                bets.append(Bets(name=bet_name, values=bet_outcome))

        return Bookmaker(name=name, bets=bets)

    @staticmethod
    def filter_without_unibet(data: list[dict]):
        bookmakers_list = [Bookmaker.to_bookmaker(bookmaker) for bookmaker in data]
        return bookmakers_list if 'Unibet' in [bookmaker.name for bookmaker in bookmakers_list] else []


if __name__ == '__main__':
    books = [{
        "id": 2,
        "name": "Marathonbet",
        "bets": [
            {
                "id": 1,
                "name": "Match Winner",
                "values": [
                    {
                        "value": "Home",
                        "odd": "1.73"
                    },
                    {
                        "value": "Draw",
                        "odd": "3.80"
                    },
                    {
                        "value": "Away",
                        "odd": "4.95"
                    }
                ]
            },
            {
                "id": 3,
                "name": "Second Half Winner",
                "values": [
                    {
                        "value": "Home",
                        "odd": "2.07"
                    },
                    {
                        "value": "Draw",
                        "odd": "2.52"
                    },
                    {
                        "value": "Away",
                        "odd": "4.85"
                    }
                ]
            },
            {
                "id": 4,
                "name": "Asian Handicap",
                "values": [
                    {
                        "value": "Home -1.25",
                        "odd": "2.71"
                    },
                    {
                        "value": "Away -1.25",
                        "odd": "1.44"
                    },
                    {
                        "value": "Home -1",
                        "odd": "2.34"
                    },
                    {
                        "value": "Away -1",
                        "odd": "1.60"
                    },
                    {
                        "value": "Home -0.75",
                        "odd": "1.92"
                    },
                    {
                        "value": "Away -0.75",
                        "odd": "1.85"
                    },
                    {
                        "value": "Home -0.25",
                        "odd": "1.48"
                    },
                    {
                        "value": "Away -0.25",
                        "odd": "2.54"
                    },
                    {
                        "value": "Home +0",
                        "odd": "1.26"
                    },
                    {
                        "value": "Away +0",
                        "odd": "3.56"
                    },
                    {
                        "value": "Home +0.25",
                        "odd": "1.19"
                    },
                    {
                        "value": "Away +0.25",
                        "odd": "4.15"
                    },
                    {
                        "value": "Home +0.75",
                        "odd": "1.07"
                    },
                    {
                        "value": "Away +0.75",
                        "odd": "6.50"
                    },
                    {
                        "value": "Home -2",
                        "odd": "5.70"
                    },
                    {
                        "value": "Away -2",
                        "odd": "1.10"
                    },
                    {
                        "value": "Home -1.75",
                        "odd": "3.90"
                    },
                    {
                        "value": "Away -1.75",
                        "odd": "1.22"
                    },
                    {
                        "value": "Home -1.5",
                        "odd": "3.10"
                    },
                    {
                        "value": "Away -1.5",
                        "odd": "1.34"
                    },
                    {
                        "value": "Home -2.5",
                        "odd": "6.65"
                    },
                    {
                        "value": "Away -2.5",
                        "odd": "1.06"
                    },
                    {
                        "value": "Home -2.25",
                        "odd": "6.20"
                    },
                    {
                        "value": "Away -2.25",
                        "odd": "1.08"
                    },
                    {
                        "value": "Home -2.75",
                        "odd": "9.10"
                    },
                    {
                        "value": "Away -2.75",
                        "odd": "1.01"
                    }
                ]
            },
            {
                "id": 5,
                "name": "Goals Over/Under",
                "values": [
                    {
                        "value": "Over 1.5",
                        "odd": "1.30"
                    },
                    {
                        "value": "Under 1.5",
                        "odd": "3.28"
                    },
                    {
                        "value": "Over 1.75",
                        "odd": "1.38"
                    },
                    {
                        "value": "Under 1.75",
                        "odd": "2.91"
                    },
                    {
                        "value": "Over 2.0",
                        "odd": "1.50"
                    },
                    {
                        "value": "Under 2.0",
                        "odd": "2.52"
                    },
                    {
                        "value": "Over 2.25",
                        "odd": "1.76"
                    },
                    {
                        "value": "Under 2.25",
                        "odd": "2.05"
                    },
                    {
                        "value": "Over 2.5",
                        "odd": "2.03"
                    },
                    {
                        "value": "Under 2.5",
                        "odd": "1.81"
                    },
                    {
                        "value": "Over 2.75",
                        "odd": "2.31"
                    },
                    {
                        "value": "Under 2.75",
                        "odd": "1.60"
                    },
                    {
                        "value": "Over 3.5",
                        "odd": "3.56"
                    },
                    {
                        "value": "Under 3.5",
                        "odd": "1.26"
                    },
                    {
                        "value": "Over 0.5",
                        "odd": "1.00"
                    },
                    {
                        "value": "Under 0.5",
                        "odd": "10.25"
                    },
                    {
                        "value": "Over 0.75",
                        "odd": "1.01"
                    },
                    {
                        "value": "Under 0.75",
                        "odd": "9.80"
                    },
                    {
                        "value": "Over 1.0",
                        "odd": "1.03"
                    },
                    {
                        "value": "Under 1.0",
                        "odd": "8.90"
                    },
                    {
                        "value": "Over 1.25",
                        "odd": "1.16"
                    },
                    {
                        "value": "Under 1.25",
                        "odd": "4.60"
                    },
                    {
                        "value": "Over 3.0",
                        "odd": "2.88"
                    },
                    {
                        "value": "Under 3.0",
                        "odd": "1.40"
                    },
                    {
                        "value": "Over 4.5",
                        "odd": "7.30"
                    },
                    {
                        "value": "Under 4.5",
                        "odd": "1.04"
                    },
                    {
                        "value": "Over 3.25",
                        "odd": "3.22"
                    },
                    {
                        "value": "Under 3.25",
                        "odd": "1.32"
                    },
                    {
                        "value": "Over 3.75",
                        "odd": "4.55"
                    },
                    {
                        "value": "Under 3.75",
                        "odd": "1.16"
                    },
                    {
                        "value": "Over 4.0",
                        "odd": "6.50"
                    },
                    {
                        "value": "Under 4.0",
                        "odd": "1.07"
                    },
                    {
                        "value": "Over 4.25",
                        "odd": "6.90"
                    },
                    {
                        "value": "Under 4.25",
                        "odd": "1.06"
                    }
                ]
            },
            {
                "id": 6,
                "name": "Goals Over/Under First Half",
                "values": [
                    {
                        "value": "Over 1.5",
                        "odd": "3.04"
                    },
                    {
                        "value": "Under 1.5",
                        "odd": "1.37"
                    },
                    {
                        "value": "Over 2.0",
                        "odd": "6.90"
                    },
                    {
                        "value": "Under 2.0",
                        "odd": "1.09"
                    },
                    {
                        "value": "Over 2.5",
                        "odd": "8.60"
                    },
                    {
                        "value": "Under 2.5",
                        "odd": "1.06"
                    },
                    {
                        "value": "Over 0.5",
                        "odd": "1.41"
                    },
                    {
                        "value": "Under 0.5",
                        "odd": "2.85"
                    },
                    {
                        "value": "Over 1.0",
                        "odd": "1.93"
                    },
                    {
                        "value": "Under 1.0",
                        "odd": "1.85"
                    }
                ]
            },
            {
                "id": 26,
                "name": "Goals Over/Under - Second Half",
                "values": [
                    {
                        "value": "Over 1.5",
                        "odd": "2.22"
                    },
                    {
                        "value": "Under 1.5",
                        "odd": "1.64"
                    },
                    {
                        "value": "Over 2.0",
                        "odd": "3.94"
                    },
                    {
                        "value": "Under 2.0",
                        "odd": "1.24"
                    },
                    {
                        "value": "Over 2.5",
                        "odd": "5.25"
                    },
                    {
                        "value": "Under 2.5",
                        "odd": "1.15"
                    },
                    {
                        "value": "Over 0.5",
                        "odd": "1.25"
                    },
                    {
                        "value": "Under 0.5",
                        "odd": "3.84"
                    },
                    {
                        "value": "Over 1.0",
                        "odd": "1.49"
                    },
                    {
                        "value": "Under 1.0",
                        "odd": "2.57"
                    }
                ]
            },
            {
                "id": 7,
                "name": "HT/FT Double",
                "values": [
                    {
                        "value": "Home/Draw",
                        "odd": "17.25"
                    },
                    {
                        "value": "Home/Away",
                        "odd": "56.00"
                    },
                    {
                        "value": "Draw/Away",
                        "odd": "10.50"
                    },
                    {
                        "value": "Draw/Draw",
                        "odd": "5.30"
                    },
                    {
                        "value": "Home/Home",
                        "odd": "2.48"
                    },
                    {
                        "value": "Draw/Home",
                        "odd": "4.35"
                    },
                    {
                        "value": "Away/Home",
                        "odd": "29.00"
                    },
                    {
                        "value": "Away/Draw",
                        "odd": "17.75"
                    },
                    {
                        "value": "Away/Away",
                        "odd": "8.30"
                    }
                ]
            },
            {
                "id": 8,
                "name": "Both Teams Score",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "1.89"
                    },
                    {
                        "value": "No",
                        "odd": "1.81"
                    }
                ]
            },
            {
                "id": 29,
                "name": "Win to Nil - Home",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "2.76"
                    },
                    {
                        "value": "No",
                        "odd": "1.39"
                    }
                ]
            },
            {
                "id": 30,
                "name": "Win to Nil - Away",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "8.20"
                    },
                    {
                        "value": "No",
                        "odd": "1.04"
                    }
                ]
            },
            {
                "id": 10,
                "name": "Exact Score",
                "values": [
                    {
                        "value": "1:0",
                        "odd": "5.65"
                    },
                    {
                        "value": "2:0",
                        "odd": "7.20"
                    },
                    {
                        "value": "2:1",
                        "odd": "7.60"
                    },
                    {
                        "value": "3:0",
                        "odd": "12.75"
                    },
                    {
                        "value": "3:1",
                        "odd": "14.25"
                    },
                    {
                        "value": "3:2",
                        "odd": "29.00"
                    },
                    {
                        "value": "4:0",
                        "odd": "30.00"
                    },
                    {
                        "value": "4:1",
                        "odd": "33.00"
                    },
                    {
                        "value": "0:0",
                        "odd": "11.50"
                    },
                    {
                        "value": "1:1",
                        "odd": "6.20"
                    },
                    {
                        "value": "2:2",
                        "odd": "16.25"
                    },
                    {
                        "value": "0:1",
                        "odd": "11.25"
                    },
                    {
                        "value": "0:2",
                        "odd": "26.00"
                    },
                    {
                        "value": "0:3",
                        "odd": "76.00"
                    },
                    {
                        "value": "1:2",
                        "odd": "14.50"
                    },
                    {
                        "value": "1:3",
                        "odd": "48.00"
                    },
                    {
                        "value": "2:3",
                        "odd": "53.00"
                    },
                    {
                        "value": "3:3",
                        "odd": "83.00"
                    },
                    {
                        "value": "4:2",
                        "odd": "67.00"
                    },
                    {
                        "value": "5:0",
                        "odd": "78.00"
                    },
                    {
                        "value": "5:1",
                        "odd": "86.00"
                    }
                ]
            },
            {
                "id": 12,
                "name": "Double Chance",
                "values": [
                    {
                        "value": "Home/Draw",
                        "odd": "1.19"
                    },
                    {
                        "value": "Home/Away",
                        "odd": "1.28"
                    },
                    {
                        "value": "Draw/Away",
                        "odd": "2.15"
                    }
                ]
            },
            {
                "id": 13,
                "name": "First Half Winner",
                "values": [
                    {
                        "value": "Home",
                        "odd": "2.30"
                    },
                    {
                        "value": "Draw",
                        "odd": "2.15"
                    },
                    {
                        "value": "Away",
                        "odd": "5.35"
                    }
                ]
            },
            {
                "id": 14,
                "name": "Team To Score First",
                "values": [
                    {
                        "value": "Home",
                        "odd": "1.53"
                    },
                    {
                        "value": "Draw",
                        "odd": "11.50"
                    },
                    {
                        "value": "Away",
                        "odd": "2.89"
                    }
                ]
            },
            {
                "id": 15,
                "name": "Team To Score Last",
                "values": [
                    {
                        "value": "Home",
                        "odd": "1.54"
                    },
                    {
                        "value": "Draw",
                        "odd": "11.50"
                    },
                    {
                        "value": "Away",
                        "odd": "2.86"
                    }
                ]
            },
            {
                "id": 16,
                "name": "Total - Home",
                "values": [
                    {
                        "value": "Over 1.5",
                        "odd": "1.91"
                    },
                    {
                        "value": "Under 1.5",
                        "odd": "1.89"
                    },
                    {
                        "value": "Over 2.5",
                        "odd": "3.94"
                    },
                    {
                        "value": "Under 2.5",
                        "odd": "1.25"
                    },
                    {
                        "value": "Over 3.5",
                        "odd": "10.25"
                    },
                    {
                        "value": "Under 3.5",
                        "odd": "1.05"
                    },
                    {
                        "value": "Over 1",
                        "odd": "1.31"
                    },
                    {
                        "value": "Under 1",
                        "odd": "3.44"
                    },
                    {
                        "value": "Over 2",
                        "odd": "2.95"
                    },
                    {
                        "value": "Under 2",
                        "odd": "1.40"
                    },
                    {
                        "value": "Over 3",
                        "odd": "8.90"
                    },
                    {
                        "value": "Under 3",
                        "odd": "1.06"
                    }
                ]
            },
            {
                "id": 17,
                "name": "Total - Away",
                "values": [
                    {
                        "value": "Over 1.5",
                        "odd": "4.15"
                    },
                    {
                        "value": "Under 1.5",
                        "odd": "1.23"
                    },
                    {
                        "value": "Over 2.5",
                        "odd": "14.50"
                    },
                    {
                        "value": "Under 2.5",
                        "odd": "1.01"
                    },
                    {
                        "value": "Over 1",
                        "odd": "2.65"
                    },
                    {
                        "value": "Under 1",
                        "odd": "1.48"
                    },
                    {
                        "value": "Over 2",
                        "odd": "12.50"
                    },
                    {
                        "value": "Under 2",
                        "odd": "1.03"
                    },
                    {
                        "value": "Over 0.5",
                        "odd": "1.57"
                    },
                    {
                        "value": "Under 0.5",
                        "odd": "2.25"
                    }
                ]
            },
            {
                "id": 19,
                "name": "Asian Handicap First Half",
                "values": [
                    {
                        "value": "Home -1",
                        "odd": "5.40"
                    },
                    {
                        "value": "Away -1",
                        "odd": "1.12"
                    },
                    {
                        "value": "Home +0",
                        "odd": "1.34"
                    },
                    {
                        "value": "Away +0",
                        "odd": "2.98"
                    },
                    {
                        "value": "Home -1.5",
                        "odd": "7.30"
                    },
                    {
                        "value": "Away -1.5",
                        "odd": "1.06"
                    }
                ]
            },
            {
                "id": 20,
                "name": "Double Chance - First Half",
                "values": [
                    {
                        "value": "Home/Draw",
                        "odd": "1.11"
                    },
                    {
                        "value": "Home/Away",
                        "odd": "1.61"
                    },
                    {
                        "value": "Draw/Away",
                        "odd": "1.54"
                    }
                ]
            },
            {
                "id": 33,
                "name": "Double Chance - Second Half",
                "values": [
                    {
                        "value": "Home/Draw",
                        "odd": "1.14"
                    },
                    {
                        "value": "Home/Away",
                        "odd": "1.45"
                    },
                    {
                        "value": "Draw/Away",
                        "odd": "1.66"
                    }
                ]
            },
            {
                "id": 34,
                "name": "Both Teams Score - First Half",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "5.20"
                    },
                    {
                        "value": "No",
                        "odd": "1.13"
                    }
                ]
            },
            {
                "id": 35,
                "name": "Both Teams To Score - Second Half",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "3.72"
                    },
                    {
                        "value": "No",
                        "odd": "1.23"
                    }
                ]
            },
            {
                "id": 21,
                "name": "Odd/Even",
                "values": [
                    {
                        "value": "Odd",
                        "odd": "1.85"
                    },
                    {
                        "value": "Even",
                        "odd": "1.85"
                    }
                ]
            },
            {
                "id": 22,
                "name": "Odd/Even - First Half",
                "values": [
                    {
                        "value": "Odd",
                        "odd": "2.06"
                    },
                    {
                        "value": "Even",
                        "odd": "1.68"
                    }
                ]
            },
            {
                "id": 37,
                "name": "Home win both halves",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "4.80"
                    },
                    {
                        "value": "No",
                        "odd": "1.15"
                    }
                ]
            },
            {
                "id": 25,
                "name": "Result/Total Goals",
                "values": [
                    {
                        "value": "Draw/Over 1.5",
                        "odd": "5.15"
                    },
                    {
                        "value": "Away/Over 1.5",
                        "odd": "7.00"
                    },
                    {
                        "value": "Home/Over 1.5",
                        "odd": "2.17"
                    },
                    {
                        "value": "Home/Under 1.5",
                        "odd": "6.70"
                    },
                    {
                        "value": "Draw/Under 1.5",
                        "odd": "11.50"
                    },
                    {
                        "value": "Away/Under 1.5",
                        "odd": "12.00"
                    },
                    {
                        "value": "Home/Over 2.5",
                        "odd": "2.84"
                    },
                    {
                        "value": "Away/Over 2.5",
                        "odd": "8.90"
                    },
                    {
                        "value": "Home/Under 2.5",
                        "odd": "3.82"
                    },
                    {
                        "value": "Draw/Under 2.5",
                        "odd": "4.60"
                    },
                    {
                        "value": "Away/Under 2.5",
                        "odd": "9.10"
                    },
                    {
                        "value": "Home/Over 3.5",
                        "odd": "5.50"
                    },
                    {
                        "value": "Home/Under 3.5",
                        "odd": "2.34"
                    },
                    {
                        "value": "Draw/Under 3.5",
                        "odd": "4.60"
                    },
                    {
                        "value": "Away/Under 3.5",
                        "odd": "5.75"
                    },
                    {
                        "value": "Home/Over 4.5",
                        "odd": "9.90"
                    },
                    {
                        "value": "Home/Under 4.5",
                        "odd": "1.96"
                    },
                    {
                        "value": "Draw/Under 4.5",
                        "odd": "3.72"
                    },
                    {
                        "value": "Away/Under 4.5",
                        "odd": "5.25"
                    },
                    {
                        "value": "Away/Under 5.5",
                        "odd": "4.85"
                    }
                ]
            },
            {
                "id": 43,
                "name": "Home Team Score a Goal",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "1.14"
                    },
                    {
                        "value": "No",
                        "odd": "4.90"
                    }
                ]
            },
            {
                "id": 44,
                "name": "Away Team Score a Goal",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "1.57"
                    },
                    {
                        "value": "No",
                        "odd": "2.25"
                    }
                ]
            },
            {
                "id": 55,
                "name": "Corners 1x2",
                "values": [
                    {
                        "value": "Home",
                        "odd": "1.42"
                    },
                    {
                        "value": "Draw",
                        "odd": "9.10"
                    },
                    {
                        "value": "Away",
                        "odd": "3.66"
                    }
                ]
            },
            {
                "id": 45,
                "name": "Corners Over Under",
                "values": [
                    {
                        "value": "Over 8.5",
                        "odd": "1.65"
                    },
                    {
                        "value": "Under 8.5",
                        "odd": "2.05"
                    },
                    {
                        "value": "Over 9.5",
                        "odd": "2.12"
                    },
                    {
                        "value": "Under 9.5",
                        "odd": "1.64"
                    },
                    {
                        "value": "Over 10.5",
                        "odd": "2.79"
                    },
                    {
                        "value": "Under 10.5",
                        "odd": "1.36"
                    },
                    {
                        "value": "Over 7.5",
                        "odd": "1.34"
                    },
                    {
                        "value": "Under 7.5",
                        "odd": "2.78"
                    },
                    {
                        "value": "Over 5.5",
                        "odd": "1.05"
                    },
                    {
                        "value": "Under 5.5",
                        "odd": "6.55"
                    },
                    {
                        "value": "Over 11.5",
                        "odd": "3.88"
                    },
                    {
                        "value": "Under 11.5",
                        "odd": "1.18"
                    },
                    {
                        "value": "Over 12.5",
                        "odd": "5.55"
                    },
                    {
                        "value": "Under 12.5",
                        "odd": "1.08"
                    },
                    {
                        "value": "Over 6.5",
                        "odd": "1.16"
                    },
                    {
                        "value": "Under 6.5",
                        "odd": "4.15"
                    },
                    {
                        "value": "Over 13.5",
                        "odd": "8.10"
                    },
                    {
                        "value": "Under 13.5",
                        "odd": "1.02"
                    }
                ]
            },
            {
                "id": 104,
                "name": "Asian Handicap (2nd Half)",
                "values": [
                    {
                        "value": "Home -1",
                        "odd": "3.92"
                    },
                    {
                        "value": "Away -1",
                        "odd": "1.21"
                    },
                    {
                        "value": "Home +0",
                        "odd": "1.33"
                    },
                    {
                        "value": "Away +0",
                        "odd": "3.04"
                    },
                    {
                        "value": "Home -1.5",
                        "odd": "5.40"
                    },
                    {
                        "value": "Away -1.5",
                        "odd": "1.12"
                    }
                ]
            },
            {
                "id": 105,
                "name": "Home Team Total Goals(1st Half)",
                "values": [
                    {
                        "value": "Over 1.5",
                        "odd": "5.45"
                    },
                    {
                        "value": "Under 1.5",
                        "odd": "1.11"
                    },
                    {
                        "value": "Over 1",
                        "odd": "3.48"
                    },
                    {
                        "value": "Under 1",
                        "odd": "1.26"
                    },
                    {
                        "value": "Over 0.5",
                        "odd": "1.77"
                    },
                    {
                        "value": "Under 0.5",
                        "odd": "1.94"
                    }
                ]
            },
            {
                "id": 106,
                "name": "Away Team Total Goals(1st Half)",
                "values": [
                    {
                        "value": "Over 1",
                        "odd": "10.75"
                    },
                    {
                        "value": "Under 1",
                        "odd": "1.01"
                    },
                    {
                        "value": "Over 0.5",
                        "odd": "2.80"
                    },
                    {
                        "value": "Under 0.5",
                        "odd": "1.38"
                    }
                ]
            },
            {
                "id": 107,
                "name": "Home Team Total Goals(2nd Half)",
                "values": [
                    {
                        "value": "Over 1.5",
                        "odd": "3.72"
                    },
                    {
                        "value": "Under 1.5",
                        "odd": "1.23"
                    },
                    {
                        "value": "Over 1",
                        "odd": "2.41"
                    },
                    {
                        "value": "Under 1",
                        "odd": "1.50"
                    },
                    {
                        "value": "Over 2",
                        "odd": "10.25"
                    },
                    {
                        "value": "Under 2",
                        "odd": "1.02"
                    }
                ]
            },
            {
                "id": 108,
                "name": "Away Team Total Goals(2nd Half)",
                "values": [
                    {
                        "value": "Over 1.5",
                        "odd": "9.60"
                    },
                    {
                        "value": "Under 1.5",
                        "odd": "1.02"
                    },
                    {
                        "value": "Over 1",
                        "odd": "6.85"
                    },
                    {
                        "value": "Under 1",
                        "odd": "1.07"
                    },
                    {
                        "value": "Over 0.5",
                        "odd": "2.33"
                    },
                    {
                        "value": "Under 0.5",
                        "odd": "1.53"
                    }
                ]
            },
            {
                "id": 63,
                "name": "Odd/Even - Second Half",
                "values": [
                    {
                        "value": "Odd",
                        "odd": "1.95"
                    },
                    {
                        "value": "Even",
                        "odd": "1.76"
                    }
                ]
            },
            {
                "id": 110,
                "name": "Scoring Draw",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "5.15"
                    },
                    {
                        "value": "No",
                        "odd": "1.13"
                    }
                ]
            },
            {
                "id": 111,
                "name": "Home team will score in both halves",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "2.84"
                    },
                    {
                        "value": "No",
                        "odd": "1.37"
                    }
                ]
            },
            {
                "id": 112,
                "name": "Away team will score in both halves",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "6.90"
                    },
                    {
                        "value": "No",
                        "odd": "1.07"
                    }
                ]
            },
            {
                "id": 184,
                "name": "To Score in Both Halves",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "1.80"
                    },
                    {
                        "value": "No",
                        "odd": "1.90"
                    }
                ]
            },
            {
                "id": 56,
                "name": "Corners Asian Handicap",
                "values": [
                    {
                        "value": "Home -1",
                        "odd": "1.47"
                    },
                    {
                        "value": "Away -1",
                        "odd": "2.39"
                    },
                    {
                        "value": "Home +0",
                        "odd": "1.27"
                    },
                    {
                        "value": "Away +0",
                        "odd": "3.14"
                    },
                    {
                        "value": "Home -3",
                        "odd": "2.34"
                    },
                    {
                        "value": "Away -3",
                        "odd": "1.49"
                    },
                    {
                        "value": "Home -2",
                        "odd": "1.82"
                    },
                    {
                        "value": "Away -2",
                        "odd": "1.88"
                    },
                    {
                        "value": "Home -1.5",
                        "odd": "1.64"
                    },
                    {
                        "value": "Away -1.5",
                        "odd": "2.10"
                    },
                    {
                        "value": "Home -2.5",
                        "odd": "2.02"
                    },
                    {
                        "value": "Away -2.5",
                        "odd": "1.69"
                    },
                    {
                        "value": "Home -3.5",
                        "odd": "2.59"
                    },
                    {
                        "value": "Away -3.5",
                        "odd": "1.39"
                    }
                ]
            },
            {
                "id": 57,
                "name": "Home Corners Over/Under",
                "values": [
                    {
                        "value": "Over 5.0",
                        "odd": "1.65"
                    },
                    {
                        "value": "Under 5.0",
                        "odd": "2.11"
                    },
                    {
                        "value": "Over 5.5",
                        "odd": "1.92"
                    },
                    {
                        "value": "Under 5.5",
                        "odd": "1.79"
                    },
                    {
                        "value": "Over 6.0",
                        "odd": "2.32"
                    },
                    {
                        "value": "Under 6.0",
                        "odd": "1.54"
                    }
                ]
            },
            {
                "id": 58,
                "name": "Away Corners Over/Under",
                "values": [
                    {
                        "value": "Over 3.5",
                        "odd": "1.95"
                    },
                    {
                        "value": "Under 3.5",
                        "odd": "1.76"
                    },
                    {
                        "value": "Over 3.0",
                        "odd": "1.58"
                    },
                    {
                        "value": "Under 3.0",
                        "odd": "2.23"
                    },
                    {
                        "value": "Over 4.0",
                        "odd": "2.49"
                    },
                    {
                        "value": "Under 4.0",
                        "odd": "1.47"
                    }
                ]
            },
            {
                "id": 59,
                "name": "Own Goal",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "8.90"
                    },
                    {
                        "value": "No",
                        "odd": "1.03"
                    }
                ]
            },
            {
                "id": 85,
                "name": "Total Corners (3 way)",
                "values": [
                    {
                        "value": "Exactly 8",
                        "odd": "7.30"
                    },
                    {
                        "value": "Over 8",
                        "odd": "1.65"
                    },
                    {
                        "value": "Under 8",
                        "odd": "2.78"
                    },
                    {
                        "value": "Exactly 9",
                        "odd": "7.20"
                    },
                    {
                        "value": "Over 9",
                        "odd": "2.12"
                    },
                    {
                        "value": "Under 9",
                        "odd": "2.05"
                    },
                    {
                        "value": "Exactly 10",
                        "odd": "7.80"
                    },
                    {
                        "value": "Over 10",
                        "odd": "2.79"
                    },
                    {
                        "value": "Under 10",
                        "odd": "1.64"
                    },
                    {
                        "value": "Exactly 11",
                        "odd": "7.60"
                    },
                    {
                        "value": "Over 11",
                        "odd": "3.88"
                    },
                    {
                        "value": "Under 11",
                        "odd": "1.36"
                    }
                ]
            },
            {
                "id": 136,
                "name": "1x2 - 15 minutes",
                "values": [
                    {
                        "value": "Home",
                        "odd": "5.15"
                    },
                    {
                        "value": "Draw",
                        "odd": "1.25"
                    },
                    {
                        "value": "Away",
                        "odd": "10.75"
                    }
                ]
            },
            {
                "id": 137,
                "name": "1x2 - 60 minutes",
                "values": [
                    {
                        "value": "Home",
                        "odd": "2.03"
                    },
                    {
                        "value": "Draw",
                        "odd": "2.57"
                    },
                    {
                        "value": "Away",
                        "odd": "4.85"
                    }
                ]
            },
            {
                "id": 138,
                "name": "1x2 - 75 minutes",
                "values": [
                    {
                        "value": "Home",
                        "odd": "1.84"
                    },
                    {
                        "value": "Draw",
                        "odd": "3.02"
                    },
                    {
                        "value": "Away",
                        "odd": "4.70"
                    }
                ]
            },
            {
                "id": 139,
                "name": "1x2 - 30 minutes",
                "values": [
                    {
                        "value": "Home",
                        "odd": "3.05"
                    },
                    {
                        "value": "Draw",
                        "odd": "1.65"
                    },
                    {
                        "value": "Away",
                        "odd": "6.50"
                    }
                ]
            },
            {
                "id": 77,
                "name": "Total Corners (1st Half)",
                "values": [
                    {
                        "value": "Exactly 4",
                        "odd": "4.90"
                    },
                    {
                        "value": "Over 4",
                        "odd": "1.67"
                    },
                    {
                        "value": "Under 4",
                        "odd": "2.08"
                    },
                    {
                        "value": "Over 5",
                        "odd": "2.62"
                    },
                    {
                        "value": "Under 5",
                        "odd": "1.43"
                    },
                    {
                        "value": "Over 4.5",
                        "odd": "2.03"
                    },
                    {
                        "value": "Under 4.5",
                        "odd": "1.70"
                    }
                ]
            },
            {
                "id": 87,
                "name": "Total ShotOnGoal",
                "values": [
                    {
                        "value": "Over 8.5",
                        "odd": "2.58"
                    },
                    {
                        "value": "Under 8.5",
                        "odd": "1.44"
                    },
                    {
                        "value": "Over 7.5",
                        "odd": "1.90"
                    },
                    {
                        "value": "Under 7.5",
                        "odd": "1.80"
                    },
                    {
                        "value": "Over 6.5",
                        "odd": "1.49"
                    },
                    {
                        "value": "Under 6.5",
                        "odd": "2.44"
                    }
                ]
            },
            {
                "id": 150,
                "name": "Home Team Yellow Cards",
                "values": [
                    {
                        "value": "Over 1.5",
                        "odd": "1.41"
                    },
                    {
                        "value": "Under 1.5",
                        "odd": "2.69"
                    },
                    {
                        "value": "Over 2.5",
                        "odd": "2.27"
                    },
                    {
                        "value": "Under 2.5",
                        "odd": "1.56"
                    },
                    {
                        "value": "Over 2",
                        "odd": "1.70"
                    },
                    {
                        "value": "Under 2",
                        "odd": "2.03"
                    }
                ]
            },
            {
                "id": 151,
                "name": "Away Team Yellow Cards",
                "values": [
                    {
                        "value": "Over 2.5",
                        "odd": "2.11"
                    },
                    {
                        "value": "Under 2.5",
                        "odd": "1.65"
                    },
                    {
                        "value": "Over 2",
                        "odd": "1.59"
                    },
                    {
                        "value": "Under 2",
                        "odd": "2.21"
                    },
                    {
                        "value": "Over 3",
                        "odd": "3.14"
                    },
                    {
                        "value": "Under 3",
                        "odd": "1.31"
                    }
                ]
            },
            {
                "id": 152,
                "name": "Yellow Asian Handicap",
                "values": [
                    {
                        "value": "Home -1",
                        "odd": "3.48"
                    },
                    {
                        "value": "Away -1",
                        "odd": "1.24"
                    },
                    {
                        "value": "Home +0",
                        "odd": "1.95"
                    },
                    {
                        "value": "Away +0",
                        "odd": "1.76"
                    },
                    {
                        "value": "Home -2",
                        "odd": "6.40"
                    },
                    {
                        "value": "Away -2",
                        "odd": "1.05"
                    },
                    {
                        "value": "Home +1",
                        "odd": "1.32"
                    },
                    {
                        "value": "Away +1",
                        "odd": "2.98"
                    },
                    {
                        "value": "Home +2",
                        "odd": "1.08"
                    },
                    {
                        "value": "Away +2",
                        "odd": "5.45"
                    },
                    {
                        "value": "Home -1.5",
                        "odd": "3.98"
                    },
                    {
                        "value": "Away -1.5",
                        "odd": "1.17"
                    },
                    {
                        "value": "Home +1.5",
                        "odd": "1.22"
                    },
                    {
                        "value": "Away +1.5",
                        "odd": "3.48"
                    }
                ]
            },
            {
                "id": 153,
                "name": "Yellow Over/Under",
                "values": [
                    {
                        "value": "Over 2.5",
                        "odd": "1.11"
                    },
                    {
                        "value": "Under 2.5",
                        "odd": "5.00"
                    },
                    {
                        "value": "Over 3.5",
                        "odd": "1.35"
                    },
                    {
                        "value": "Under 3.5",
                        "odd": "2.79"
                    },
                    {
                        "value": "Over 3.0",
                        "odd": "1.14"
                    },
                    {
                        "value": "Under 3.0",
                        "odd": "4.35"
                    },
                    {
                        "value": "Over 4.5",
                        "odd": "1.83"
                    },
                    {
                        "value": "Under 4.5",
                        "odd": "1.87"
                    },
                    {
                        "value": "Over 4.0",
                        "odd": "1.51"
                    },
                    {
                        "value": "Under 4.0",
                        "odd": "2.35"
                    },
                    {
                        "value": "Over 5.0",
                        "odd": "2.22"
                    },
                    {
                        "value": "Under 5.0",
                        "odd": "1.57"
                    },
                    {
                        "value": "Over 5.5",
                        "odd": "2.60"
                    },
                    {
                        "value": "Under 5.5",
                        "odd": "1.40"
                    },
                    {
                        "value": "Over 6.5",
                        "odd": "4.10"
                    },
                    {
                        "value": "Under 6.5",
                        "odd": "1.16"
                    },
                    {
                        "value": "Over 6.0",
                        "odd": "3.58"
                    },
                    {
                        "value": "Under 6.0",
                        "odd": "1.21"
                    }
                ]
            },
            {
                "id": 86,
                "name": "RCARD",
                "values": [
                    {
                        "value": "Yes",
                        "odd": "3.95"
                    },
                    {
                        "value": "No",
                        "odd": "1.25"
                    }
                ]
            }
        ]
    },
        {
            "id": 16,
            "name": "Unibet",
            "bets": [
                {
                    "id": 1,
                    "name": "Match Winner",
                    "values": [
                        {
                            "value": "Home",
                            "odd": "1.72"
                        },
                        {
                            "value": "Draw",
                            "odd": "3.60"
                        },
                        {
                            "value": "Away",
                            "odd": "4.80"
                        }
                    ]
                },
                {
                    "id": 2,
                    "name": "Home/Away",
                    "values": [
                        {
                            "value": "Home",
                            "odd": "1.29"
                        },
                        {
                            "value": "Away",
                            "odd": "3.45"
                        }
                    ]
                },
                {
                    "id": 3,
                    "name": "Second Half Winner",
                    "values": [
                        {
                            "value": "Home",
                            "odd": "2.12"
                        },
                        {
                            "value": "Draw",
                            "odd": "2.55"
                        },
                        {
                            "value": "Away",
                            "odd": "4.60"
                        }
                    ]
                },
                {
                    "id": 5,
                    "name": "Goals Over/Under",
                    "values": [
                        {
                            "value": "Over 1.5",
                            "odd": "1.30"
                        },
                        {
                            "value": "Under 1.5",
                            "odd": "3.35"
                        },
                        {
                            "value": "Over 1.75",
                            "odd": "1.42"
                        },
                        {
                            "value": "Under 1.75",
                            "odd": "2.88"
                        },
                        {
                            "value": "Over 2.0",
                            "odd": "1.54"
                        },
                        {
                            "value": "Under 2.0",
                            "odd": "2.45"
                        },
                        {
                            "value": "Over 2.25",
                            "odd": "1.79"
                        },
                        {
                            "value": "Under 2.25",
                            "odd": "2.00"
                        },
                        {
                            "value": "Over 2.5",
                            "odd": "2.05"
                        },
                        {
                            "value": "Under 2.5",
                            "odd": "1.76"
                        },
                        {
                            "value": "Over 2.75",
                            "odd": "2.35"
                        },
                        {
                            "value": "Under 2.75",
                            "odd": "1.57"
                        },
                        {
                            "value": "Over 3.5",
                            "odd": "3.85"
                        },
                        {
                            "value": "Under 3.5",
                            "odd": "1.24"
                        },
                        {
                            "value": "Over 0.5",
                            "odd": "1.03"
                        },
                        {
                            "value": "Under 0.5",
                            "odd": "10.50"
                        },
                        {
                            "value": "Over 3.0",
                            "odd": "2.95"
                        },
                        {
                            "value": "Under 3.0",
                            "odd": "1.38"
                        },
                        {
                            "value": "Over 4.5",
                            "odd": "8.00"
                        },
                        {
                            "value": "Under 4.5",
                            "odd": "1.06"
                        },
                        {
                            "value": "Over 3.25",
                            "odd": "3.35"
                        },
                        {
                            "value": "Under 3.25",
                            "odd": "1.30"
                        }
                    ]
                },
                {
                    "id": 6,
                    "name": "Goals Over/Under First Half",
                    "values": [
                        {
                            "value": "Over 1.5",
                            "odd": "3.00"
                        },
                        {
                            "value": "Under 1.5",
                            "odd": "1.38"
                        },
                        {
                            "value": "Over 1.75",
                            "odd": "3.90"
                        },
                        {
                            "value": "Under 1.75",
                            "odd": "1.24"
                        },
                        {
                            "value": "Over 2.0",
                            "odd": "6.50"
                        },
                        {
                            "value": "Under 2.0",
                            "odd": "1.10"
                        },
                        {
                            "value": "Over 2.5",
                            "odd": "6.75"
                        },
                        {
                            "value": "Under 2.5",
                            "odd": "1.06"
                        },
                        {
                            "value": "Over 0.5",
                            "odd": "1.41"
                        },
                        {
                            "value": "Under 0.5",
                            "odd": "2.65"
                        },
                        {
                            "value": "Over 0.75",
                            "odd": "1.58"
                        },
                        {
                            "value": "Under 0.75",
                            "odd": "2.32"
                        },
                        {
                            "value": "Over 1.0",
                            "odd": "1.96"
                        },
                        {
                            "value": "Under 1.0",
                            "odd": "1.80"
                        },
                        {
                            "value": "Over 1.25",
                            "odd": "2.48"
                        },
                        {
                            "value": "Under 1.25",
                            "odd": "1.50"
                        }
                    ]
                },
                {
                    "id": 26,
                    "name": "Goals Over/Under - Second Half",
                    "values": [
                        {
                            "value": "Over 1.5",
                            "odd": "2.18"
                        },
                        {
                            "value": "Under 1.5",
                            "odd": "1.58"
                        },
                        {
                            "value": "Over 2.5",
                            "odd": "4.60"
                        },
                        {
                            "value": "Under 2.5",
                            "odd": "1.15"
                        },
                        {
                            "value": "Over 3.5",
                            "odd": "11.50"
                        },
                        {
                            "value": "Under 3.5",
                            "odd": "1.02"
                        },
                        {
                            "value": "Over 0.5",
                            "odd": "1.24"
                        },
                        {
                            "value": "Under 0.5",
                            "odd": "3.55"
                        }
                    ]
                },
                {
                    "id": 7,
                    "name": "HT/FT Double",
                    "values": [
                        {
                            "value": "Home/Draw",
                            "odd": "14.00"
                        },
                        {
                            "value": "Home/Away",
                            "odd": "51.00"
                        },
                        {
                            "value": "Draw/Away",
                            "odd": "9.50"
                        },
                        {
                            "value": "Draw/Draw",
                            "odd": "5.10"
                        },
                        {
                            "value": "Home/Home",
                            "odd": "2.70"
                        },
                        {
                            "value": "Draw/Home",
                            "odd": "4.30"
                        },
                        {
                            "value": "Away/Home",
                            "odd": "23.00"
                        },
                        {
                            "value": "Away/Draw",
                            "odd": "15.00"
                        },
                        {
                            "value": "Away/Away",
                            "odd": "7.50"
                        }
                    ]
                },
                {
                    "id": 8,
                    "name": "Both Teams Score",
                    "values": [
                        {
                            "value": "Yes",
                            "odd": "1.94"
                        },
                        {
                            "value": "No",
                            "odd": "1.80"
                        }
                    ]
                },
                {
                    "id": 9,
                    "name": "Handicap Result",
                    "values": [
                        {
                            "value": "Home -1",
                            "odd": "3.15"
                        },
                        {
                            "value": "Away -1",
                            "odd": "2.06"
                        },
                        {
                            "value": "Draw -1",
                            "odd": "3.35"
                        },
                        {
                            "value": "Home -2",
                            "odd": "7.00"
                        },
                        {
                            "value": "Draw -2",
                            "odd": "5.10"
                        },
                        {
                            "value": "Away -2",
                            "odd": "1.33"
                        }
                    ]
                },
                {
                    "id": 10,
                    "name": "Exact Score",
                    "values": [
                        {
                            "value": "1:0",
                            "odd": "6.10"
                        },
                        {
                            "value": "2:0",
                            "odd": "7.00"
                        },
                        {
                            "value": "2:1",
                            "odd": "7.50"
                        },
                        {
                            "value": "3:0",
                            "odd": "12.50"
                        },
                        {
                            "value": "3:1",
                            "odd": "14.00"
                        },
                        {
                            "value": "3:2",
                            "odd": "26.00"
                        },
                        {
                            "value": "4:0",
                            "odd": "30.00"
                        },
                        {
                            "value": "4:1",
                            "odd": "36.00"
                        },
                        {
                            "value": "0:0",
                            "odd": "9.50"
                        },
                        {
                            "value": "1:1",
                            "odd": "6.40"
                        },
                        {
                            "value": "2:2",
                            "odd": "16.00"
                        },
                        {
                            "value": "0:1",
                            "odd": "11.50"
                        },
                        {
                            "value": "0:2",
                            "odd": "23.00"
                        },
                        {
                            "value": "0:3",
                            "odd": "67.00"
                        },
                        {
                            "value": "1:2",
                            "odd": "14.00"
                        },
                        {
                            "value": "1:3",
                            "odd": "46.00"
                        },
                        {
                            "value": "2:3",
                            "odd": "51.00"
                        },
                        {
                            "value": "3:3",
                            "odd": "81.00"
                        },
                        {
                            "value": "1:4",
                            "odd": "181.00"
                        },
                        {
                            "value": "2:4",
                            "odd": "226.00"
                        },
                        {
                            "value": "4:2",
                            "odd": "56.00"
                        },
                        {
                            "value": "5:0",
                            "odd": "81.00"
                        },
                        {
                            "value": "5:1",
                            "odd": "111.00"
                        },
                        {
                            "value": "5:2",
                            "odd": "201.00"
                        },
                        {
                            "value": "6:0",
                            "odd": "226.00"
                        },
                        {
                            "value": "4:3",
                            "odd": "226.00"
                        }
                    ]
                },
                {
                    "id": 31,
                    "name": "Correct Score - First Half",
                    "values": [
                        {
                            "value": "1:0",
                            "odd": "3.50"
                        },
                        {
                            "value": "2:0",
                            "odd": "9.00"
                        },
                        {
                            "value": "2:1",
                            "odd": "21.00"
                        },
                        {
                            "value": "3:0",
                            "odd": "31.00"
                        },
                        {
                            "value": "3:1",
                            "odd": "81.00"
                        },
                        {
                            "value": "4:0",
                            "odd": "201.00"
                        },
                        {
                            "value": "0:0",
                            "odd": "2.70"
                        },
                        {
                            "value": "1:1",
                            "odd": "8.00"
                        },
                        {
                            "value": "2:2",
                            "odd": "91.00"
                        },
                        {
                            "value": "0:1",
                            "odd": "6.40"
                        },
                        {
                            "value": "0:2",
                            "odd": "26.00"
                        },
                        {
                            "value": "0:3",
                            "odd": "151.00"
                        },
                        {
                            "value": "1:2",
                            "odd": "36.00"
                        },
                        {
                            "value": "1:3",
                            "odd": "251.00"
                        }
                    ]
                },
                {
                    "id": 12,
                    "name": "Double Chance",
                    "values": [
                        {
                            "value": "Home/Draw",
                            "odd": "1.18"
                        },
                        {
                            "value": "Home/Away",
                            "odd": "1.28"
                        },
                        {
                            "value": "Draw/Away",
                            "odd": "2.04"
                        }
                    ]
                },
                {
                    "id": 13,
                    "name": "First Half Winner",
                    "values": [
                        {
                            "value": "Home",
                            "odd": "2.35"
                        },
                        {
                            "value": "Draw",
                            "odd": "2.17"
                        },
                        {
                            "value": "Away",
                            "odd": "5.00"
                        }
                    ]
                },
                {
                    "id": 16,
                    "name": "Total - Home",
                    "values": [
                        {
                            "value": "Over 1.5",
                            "odd": "1.90"
                        },
                        {
                            "value": "Under 1.5",
                            "odd": "1.80"
                        },
                        {
                            "value": "Over 2.5",
                            "odd": "3.90"
                        },
                        {
                            "value": "Under 2.5",
                            "odd": "1.21"
                        },
                        {
                            "value": "Over 3.5",
                            "odd": "8.50"
                        },
                        {
                            "value": "Under 3.5",
                            "odd": "1.04"
                        },
                        {
                            "value": "Over 0.5",
                            "odd": "1.17"
                        },
                        {
                            "value": "Under 0.5",
                            "odd": "4.35"
                        }
                    ]
                },
                {
                    "id": 17,
                    "name": "Total - Away",
                    "values": [
                        {
                            "value": "Over 1.5",
                            "odd": "3.80"
                        },
                        {
                            "value": "Under 1.5",
                            "odd": "1.22"
                        },
                        {
                            "value": "Over 2.5",
                            "odd": "9.50"
                        },
                        {
                            "value": "Under 2.5",
                            "odd": "1.03"
                        },
                        {
                            "value": "Over 0.5",
                            "odd": "1.58"
                        },
                        {
                            "value": "Under 0.5",
                            "odd": "2.18"
                        }
                    ]
                },
                {
                    "id": 20,
                    "name": "Double Chance - First Half",
                    "values": [
                        {
                            "value": "Home/Draw",
                            "odd": "1.13"
                        },
                        {
                            "value": "Home/Away",
                            "odd": "1.60"
                        },
                        {
                            "value": "Draw/Away",
                            "odd": "1.50"
                        }
                    ]
                },
                {
                    "id": 55,
                    "name": "Corners 1x2",
                    "values": [
                        {
                            "value": "Home",
                            "odd": "1.49"
                        },
                        {
                            "value": "Draw",
                            "odd": "7.00"
                        },
                        {
                            "value": "Away",
                            "odd": "2.90"
                        }
                    ]
                },
                {
                    "id": 45,
                    "name": "Corners Over Under",
                    "values": [
                        {
                            "value": "Over 8.5",
                            "odd": "1.58"
                        },
                        {
                            "value": "Under 8.5",
                            "odd": "2.18"
                        },
                        {
                            "value": "Over 9.5",
                            "odd": "1.95"
                        },
                        {
                            "value": "Under 9.5",
                            "odd": "1.75"
                        },
                        {
                            "value": "Over 10.5",
                            "odd": "2.48"
                        },
                        {
                            "value": "Under 10.5",
                            "odd": "1.46"
                        },
                        {
                            "value": "Over 4.5",
                            "odd": "1.01"
                        },
                        {
                            "value": "Under 4.5",
                            "odd": "9.50"
                        },
                        {
                            "value": "Over 7.5",
                            "odd": "1.34"
                        },
                        {
                            "value": "Under 7.5",
                            "odd": "2.90"
                        },
                        {
                            "value": "Over 5.5",
                            "odd": "1.08"
                        },
                        {
                            "value": "Under 5.5",
                            "odd": "6.10"
                        },
                        {
                            "value": "Over 11.5",
                            "odd": "3.20"
                        },
                        {
                            "value": "Under 11.5",
                            "odd": "1.29"
                        },
                        {
                            "value": "Over 12.5",
                            "odd": "4.30"
                        },
                        {
                            "value": "Under 12.5",
                            "odd": "1.17"
                        },
                        {
                            "value": "Over 6.5",
                            "odd": "1.19"
                        },
                        {
                            "value": "Under 6.5",
                            "odd": "4.10"
                        },
                        {
                            "value": "Over 13.5",
                            "odd": "5.60"
                        },
                        {
                            "value": "Under 13.5",
                            "odd": "1.10"
                        },
                        {
                            "value": "Over 14.5",
                            "odd": "7.00"
                        },
                        {
                            "value": "Under 14.5",
                            "odd": "1.05"
                        }
                    ]
                },
                {
                    "id": 105,
                    "name": "Home Team Total Goals(1st Half)",
                    "values": [
                        {
                            "value": "Over 1.5",
                            "odd": "4.90"
                        },
                        {
                            "value": "Under 1.5",
                            "odd": "1.13"
                        },
                        {
                            "value": "Over 0.5",
                            "odd": "1.79"
                        },
                        {
                            "value": "Under 0.5",
                            "odd": "1.91"
                        }
                    ]
                },
                {
                    "id": 106,
                    "name": "Away Team Total Goals(1st Half)",
                    "values": [
                        {
                            "value": "Over 1.5",
                            "odd": "10.00"
                        },
                        {
                            "value": "Under 1.5",
                            "odd": "1.03"
                        },
                        {
                            "value": "Over 0.5",
                            "odd": "2.75"
                        },
                        {
                            "value": "Under 0.5",
                            "odd": "1.38"
                        }
                    ]
                },
                {
                    "id": 109,
                    "name": "Draw No Bet (1st Half)",
                    "values": [
                        {
                            "value": "Home",
                            "odd": "1.36"
                        },
                        {
                            "value": "Away",
                            "odd": "2.90"
                        }
                    ]
                },
                {
                    "id": 182,
                    "name": "Draw No Bet (2nd Half)",
                    "values": [
                        {
                            "value": "Home",
                            "odd": "1.34"
                        },
                        {
                            "value": "Away",
                            "odd": "2.80"
                        }
                    ]
                },
                {
                    "id": 57,
                    "name": "Home Corners Over/Under",
                    "values": [
                        {
                            "value": "Over 3.5",
                            "odd": "1.26"
                        },
                        {
                            "value": "Under 3.5",
                            "odd": "3.40"
                        },
                        {
                            "value": "Over 8.5",
                            "odd": "4.80"
                        },
                        {
                            "value": "Under 8.5",
                            "odd": "1.14"
                        },
                        {
                            "value": "Over 4.5",
                            "odd": "1.53"
                        },
                        {
                            "value": "Under 4.5",
                            "odd": "2.30"
                        },
                        {
                            "value": "Over 7.5",
                            "odd": "3.45"
                        },
                        {
                            "value": "Under 7.5",
                            "odd": "1.25"
                        },
                        {
                            "value": "Over 5.5",
                            "odd": "1.96"
                        },
                        {
                            "value": "Under 5.5",
                            "odd": "1.73"
                        },
                        {
                            "value": "Over 6.5",
                            "odd": "2.55"
                        },
                        {
                            "value": "Under 6.5",
                            "odd": "1.44"
                        }
                    ]
                },
                {
                    "id": 58,
                    "name": "Away Corners Over/Under",
                    "values": [
                        {
                            "value": "Over 2.5",
                            "odd": "1.38"
                        },
                        {
                            "value": "Under 2.5",
                            "odd": "2.70"
                        },
                        {
                            "value": "Over 3.5",
                            "odd": "1.84"
                        },
                        {
                            "value": "Under 3.5",
                            "odd": "1.84"
                        },
                        {
                            "value": "Over 4.5",
                            "odd": "2.55"
                        },
                        {
                            "value": "Under 4.5",
                            "odd": "1.44"
                        },
                        {
                            "value": "Over 5.5",
                            "odd": "3.80"
                        },
                        {
                            "value": "Under 5.5",
                            "odd": "1.21"
                        },
                        {
                            "value": "Over 6.5",
                            "odd": "5.40"
                        },
                        {
                            "value": "Under 6.5",
                            "odd": "1.10"
                        }
                    ]
                },
                {
                    "id": 77,
                    "name": "Total Corners (1st Half)",
                    "values": [
                        {
                            "value": "Over 3.5",
                            "odd": "1.45"
                        },
                        {
                            "value": "Under 3.5",
                            "odd": "2.43"
                        },
                        {
                            "value": "Over 4.5",
                            "odd": "1.97"
                        },
                        {
                            "value": "Under 4.5",
                            "odd": "1.70"
                        },
                        {
                            "value": "Over 5.5",
                            "odd": "2.80"
                        },
                        {
                            "value": "Under 5.5",
                            "odd": "1.35"
                        }
                    ]
                },
                {
                    "id": 80,
                    "name": "Cards Over/Under",
                    "values": [
                        {
                            "value": "Over 2.5",
                            "odd": "1.11"
                        },
                        {
                            "value": "Under 2.5",
                            "odd": "5.10"
                        },
                        {
                            "value": "Over 3.5",
                            "odd": "1.33"
                        },
                        {
                            "value": "Under 3.5",
                            "odd": "2.95"
                        },
                        {
                            "value": "Over 4.5",
                            "odd": "1.71"
                        },
                        {
                            "value": "Under 4.5",
                            "odd": "2.00"
                        },
                        {
                            "value": "Over 7.5",
                            "odd": "4.60"
                        },
                        {
                            "value": "Under 7.5",
                            "odd": "1.15"
                        },
                        {
                            "value": "Over 5.5",
                            "odd": "2.30"
                        },
                        {
                            "value": "Under 5.5",
                            "odd": "1.54"
                        },
                        {
                            "value": "Over 6.5",
                            "odd": "3.20"
                        },
                        {
                            "value": "Under 6.5",
                            "odd": "1.28"
                        }
                    ]
                }
            ]
        }, ]
    pprint(Bookmaker.filter_without_unibet(books))
