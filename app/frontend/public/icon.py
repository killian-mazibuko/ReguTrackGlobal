from PIL import Image

# Load the PNG you just saved
img = Image.open("icon.png")

# Professional ICOs usually contain these standard sizes
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (255, 255)]

# Save as .ico
img.save("favicon.ico", sizes=icon_sizes)

print("ReguTrack Global icon created successfully!")