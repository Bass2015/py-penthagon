from js import document
from constants import UI, CANVAS, STATE_CHANGED
from events import deboog

HEART_SPACING = 50
PLAYERS_SPACING = [50, CANVAS.width - 50]
TITLE_SIZE = CANVAS.width*0.02
FONT = f'{TITLE_SIZE}px \"Arial Rounded\", sans-serif'
FONT_SC = f'{TITLE_SIZE/1.2}px \"Arial Rounded\", sans-serif'

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
        self.render_titles()
        self.render_scores()
        self.render_hearts()

    def on_state_changed(self):
        self.render_ui()

    def render_titles(self):
        UI.font = FONT
        UI.fillText("Player 1", PLAYERS_SPACING[0], 50)
        UI.fillText("Player 2", PLAYERS_SPACING[1] -60, 50)

    def render_scores(self):
        UI.font = FONT_SC
        UI.fillText(f"Score: {self.player.score}", PLAYERS_SPACING[0], 75)
        UI.fillText(f"Score: {self.player.score}", PLAYERS_SPACING[1] -60, 75)

    def render_hearts(self):
        for life in range(self.player.lifes):
            UI.drawImage(self.heart,
                        PLAYERS_SPACING[0],
                        HEART_SPACING * (life + 1) + 50,
                        self.heart.width/4,
                        self.heart.height/4)


