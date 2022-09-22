from js import document
import constants

class UIManager():
    def __init__(self):
        constants.SHIP_EXPLODED.suscribe(self)
        self.play_b = document.getElementById("play_b")
        self.play_b.style.display = 'none'
        self.players_ui = {
            1: {
                'score': document.getElementById("score_p1"),
                'hearts': [
                    document.getElementById("heart1_0"),
                    document.getElementById("heart1_1"),
                    document.getElementById("heart1_2")
                ],
                'lifes': 3
            },
            2: {
                'score': document.getElementById("score_p2"),
                'hearts': [
                    document.getElementById("heart2_0"),
                    document.getElementById("heart2_1"),
                    document.getElementById("heart2_2")
                ],
                'lifes': 3
            }
        }
    
    def on_ship_exploded(self, ship):
        lifes = self.players_ui[ship.player]['lifes']
        self.players_ui[ship.player]['hearts'][lifes - 1].style.display = 'none'
        if lifes > 1:
            self.players_ui[ship.player]['lifes'] -= 1


