from PIL import Image
import pytesseract


image = Image.open('images/x.jpg')

text = pytesseract.image_to_string(image)

print(text)
