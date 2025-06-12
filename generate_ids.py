import csv
import os
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

TEMPLATE_IMAGE = "id_template.png"
CSV_FILE = "employees.csv"
PHOTO_FOLDER = "photos"
FINAL_PDF = "generated_ids.pdf"
TEXT_FONT = "verdana.ttf"
TEXT_SIZE = 18


base_template = Image.open(TEMPLATE_IMAGE)
canvas_width, canvas_height = base_template.size


pdf = FPDF(unit="pt", format=[canvas_width, canvas_height])
font = ImageFont.truetype(TEXT_FONT, TEXT_SIZE)


with open(CSV_FILE, newline='', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for employee in csv_reader:
        card = base_template.copy()
        drawer = ImageDraw.Draw(card)

        
        text_x = 20 #
        text_y = canvas_height - 40
        drawer.text((text_x, text_y), employee["name"], font=font, fill="white")

        
        image_path = os.path.join(PHOTO_FOLDER, employee["photo"])
        if os.path.exists(image_path):
            profile = Image.open(image_path).resize((100, 100))
            card.paste(profile, (canvas_width - 130, 20))

       
        temp_image = "temp_card.png"
        card.save(temp_image)

        pdf.add_page()
        pdf.image(temp_image, 0, 0)


pdf.output(FINAL_PDF)
print("All done! File saved as:", FINAL_PDF)
