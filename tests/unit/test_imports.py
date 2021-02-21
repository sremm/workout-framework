from wof.import_workflows import polar


class TestPolarConversion:
    def test_data_without_heart_rate_entry(self):
        data = {
            "exportVersion": "1.3",
            "name": "Strength training",
            "startTime": "2020-11-30T15:40:16.000",
            "stopTime": "2020-11-30T17:05:42.238",
            "timeZoneOffset": 60,
            "distance": 0.0,
            "duration": "PT5126.238S",
            "kiloCalories": 945,
            "exercises": [
                {
                    "startTime": "2020-11-30T15:40:16.000",
                    "stopTime": "2020-11-30T17:05:42.238",
                    "timezoneOffset": 60,
                    "duration": "PT5126.238S",
                    "distance": 0.0,
                    "sport": "STRENGTH_TRAINING",
                    "kiloCalories": 945,
                    "samples": {},
                }
            ],
        }
        session = polar._convert_to_workout_session(data)
        assert session.heart_rate == None
