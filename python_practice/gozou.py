from PIL import Image
img = Image.open("sample.jpg")

width = img.size[0]
height = img.size[1]
print(f"画像の幅は{width}")
print(f"画像の高さは{height}")

resized_width = int(width * 2)
resized_height = int(height * 0.5)

resized_img = img.resize((resized_width, resized_height))
resized_img.save("resized.jpg")

rotated_img = img.rotate(90)
rotated_img.save("rotated.jpg")

grayscale_img = img.convert("L")
grayscale_img.save("grayscale.jpg")