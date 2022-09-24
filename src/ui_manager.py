from js import document
from constants import UI, SHIP_EXPLODED, CANVAS
from events import deboog

class UIManager():
    def __init__(self, players):
        self.heart = document.getElementById('heart')
        SHIP_EXPLODED.suscribe(self)
        self.players ={
            1: players[0],
            # 2: players[1],
        }
        # self.play_b = document.getElementById("play_b")
        # self.play_b.style.display = 'none'
       
    def render_ui(self):
        UI.clearRect(0,0, CANVAS.width, CANVAS.height)
        UI.drawImage(self.heart, 50, 50, self.heart.width/4, self.heart.height/4)

    def on_ship_exploded(self, ship):
        # lifes = self.players_ui[ship.player]['lifes']
        # self.players_ui[ship.player]['hearts'][lifes - 1].style.display = 'none'
        # if lifes > 1:
        #     self.players_ui[ship.player]['lifes'] -= 1
        self.render_ui()


