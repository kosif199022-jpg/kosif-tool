# A typical mistake: a typo in a colour name
from PIL import Image, ImageDraw
img = Image.new("RGB", (600, 400), "white")
d = ImageDraw.Draw(img)
d.ellipse([200, 100, 400, 300], fill="bluee")
img.save("x.png")
