from asyncio import constants
from js import document
from constants import UI, CANVAS, STATE_CHANGED, GAME_ENDED, GAME_START
from events import deboog
import time

HEART_SPACING = 50
PLAYERS_SPACING = [50, CANVAS.width - 50]
TITLE_SIZE = CANVAS.width*0.02
FONT = f'{TITLE_SIZE}px \"Arial Rounded\", sans-serif'
FONT_SC = f'{TITLE_SIZE/1.2}px \"Arial Rounded\", sans-serif'

class UIManager():
    def __init__(self):
        self.heart = document.getElementById('heart')
        self.label = document.getElementById('ui-text')
        self.spalsh_sc = document.getElementById('ui')
        STATE_CHANGED.suscribe(self)
        GAME_ENDED.suscribe(self)
    
    def initialize(self, players):
        self.players = players
        self.render_ui()
        self.spalsh_sc.style.display = 'none'
        GAME_START.trigger()
       
    def render_ui(self):
        UI.clearRect(0,0, CANVAS.width, CANVAS.height)
        UI.fillStyle = 'White'
        self.render_titles()
        self.render_scores()
        self.render_hearts()

    def on_state_changed(self):
        self.render_ui()

    def on_game_ended(self, loser):
        if loser not in self.players:
            return
        UI.clearRect(0,0, CANVAS.width, CANVAS.height)
        winner = 1 if loser.player == 2 else 2
        score = self.players[winner-1].score
        score = score + 100 if loser.player == 1 else score
        self.label.innerHTML = f'The winner is Player {winner}<br/>Score: {score}'
        self.players.clear()
        self.spalsh_sc.style.display = 'block'

    def render_titles(self):
        UI.font = FONT
        UI.fillText("Player 1", PLAYERS_SPACING[0], 50)
        UI.fillText("Player 2", PLAYERS_SPACING[1] -60, 50)

    def render_scores(self):
        UI.font = FONT_SC
        UI.fillText(f"Score: {self.players[0].score}", PLAYERS_SPACING[0], 75)
        UI.fillText(f"Score: {self.players[1].score}", PLAYERS_SPACING[1] -60, 75)
        UI.fillText(f"Move: wasd", PLAYERS_SPACING[0]-20, CANVAS.height -80)
        UI.fillText(f"Fire: space", PLAYERS_SPACING[0]-20, CANVAS.height -40)  
        UI.fillText(f"Move: arrows", PLAYERS_SPACING[1] - 80, CANVAS.height -80)
        UI.fillText(f"Fire: enter", PLAYERS_SPACING[1] - 68, CANVAS.height -40)  

    def render_hearts(self):
        for i in range(len(self.players)):
            for life in range(self.players[i].lifes):
                UI.drawImage(self.heart,
                            PLAYERS_SPACING[i],
                            HEART_SPACING * (life + 1) + 50,
                            self.heart.width/4,
                            self.heart.height/4)


