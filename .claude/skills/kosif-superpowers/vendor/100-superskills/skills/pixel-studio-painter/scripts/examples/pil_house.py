# What a typical AI writes for "draw a house at sunset with Python"
from PIL import Image, ImageDraw

W, H = 800, 600
img = Image.new("RGB", (W, H), "#87CEEB")
draw = ImageDraw.Draw(img)

# sky gradient
for y in range(H // 2 + 60):
    r = int(255 - y * 0.3); g = int(160 - y * 0.15); b = int(90 + y * 0.25)
    draw.line([(0, y), (W, y)], fill=(r, g, b))
# sun
draw.ellipse([520, 120, 640, 240], fill="#FFD54F")
# ground
draw.rectangle([0, 420, W, H], fill="#4CAF50")
# house body
draw.rectangle([220, 280, 480, 460], fill="#D7A86E", outline="#5D4037", width=4)
# roof
draw.polygon([(200, 290), (350, 170), (500, 290)], fill="#B23B3B", outline="#5D4037")
# door and windows
draw.rectangle([320, 360, 380, 460], fill="#6D4C41")
draw.rectangle([245, 315, 300, 365], fill="#FFF59D", outline="#5D4037", width=3)
draw.rectangle([400, 315, 455, 365], fill="#FFF59D", outline="#5D4037", width=3)
# tree
draw.rectangle([600, 360, 630, 460], fill="#795548")
draw.ellipse([555, 270, 675, 390], fill="#2E7D32")
draw.text((30, 30), "Sweet home", fill="white")
img.save("house.png")
img.show()
