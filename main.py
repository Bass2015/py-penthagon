from js import document
import math

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")
ctx.beginPath()
ctx.arc(100, 75, 50, 0, 2 * math.pi)
ctx.stroke()