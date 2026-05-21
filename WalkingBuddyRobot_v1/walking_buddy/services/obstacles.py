class ObstacleService:
    def __init__(self):
        self.distance_cm = 100

    def get_status(self):

        if self.distance_cm < 30:
            return {
                "safe": False,
                "message": "Obstacle ahead"
            }

        return {
            "safe": True,
            "message": "Path clear"
        }

    def simulate_distance(self,value):
        self.distance_cm=value