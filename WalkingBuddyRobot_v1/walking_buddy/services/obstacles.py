class ObstacleService:
    distance_cm = 100

    @classmethod
    def set_distance(cls, value):
        cls.distance_cm = max(0, float(value))

    @classmethod
    def get_status(cls):
        safe = cls.distance_cm >= 30
        return {
            "safe": safe,
            "distance_cm": cls.distance_cm,
            "message": "Path clear" if safe else "Obstacle ahead"
        }
