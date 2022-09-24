from js import document
from constants import UI, SHIP_EXPLODED, CANVAS, STATE_CHANGED
from events import deboog

HEART_SPACING = 50
PLAYERS_SPACING = [50, CANVAS.width - 50]

class UIManager():
    def __init__(self, player):
        self.heart = document.getElementById('heart')
        STATE_CHANGED.suscribe(self)
        self.player = player
        self.render_ui()
        # self.play_b = document.getElementById("play_b")
        # self.play_b.style.display = 'none'
       
    def render_ui(self):
        UI.clearRect(0,0, CANVAS.width, CANVAS.height)
        self.render_hearts()

    def on_state_changed(self):
        self.render_ui()

    def render_hearts(self):
        for life in range(self.player.lifes):
            UI.drawImage(self.heart,
                        PLAYERS_SPACING[0],
                        HEART_SPACING * (life + 1),
                        self.heart.width/4,
                        self.heart.height/4)


