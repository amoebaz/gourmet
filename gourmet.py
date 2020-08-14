import datetime
import random, os
from wand.image import Image
from wand.drawing import Drawing
from wand.display import display
from wand.color import *

# Make the image 1024px on the longest side
def adjust_width_height(i):
    img_width = i.width
    img_height = i.height
    max = (img_height, img_width)[img_width > img_height]
    percent = 1024 / max
    i.resize(int(percent * img_width), int(percent * img_height))

    return i            

# Format the date string
def date_string():
    str = ""
    now = datetime.datetime.now()
    day = now.strftime("%w")
    if day == "0":
        str += "Domingo "
    elif day == "1":
        str += "Lunes "
    elif day == "2":
        str += "Martes "
    elif day == "3":
        str += "Miercoles "
    elif day == "4":
        str += "Jueves "
    elif day == "5":
        str += "Viernes "
    elif day == "6":
        str += "Sábado "
    else: 
        str += "+++"

    str += now.strftime("%d de ")


    month = now.strftime("%-m")
    if month == "1":
        str += "Enero"
    elif month == "2":
        str += "Febrero"
    elif month == "3":
        str += "Marzo"
    elif month == "4":
        str += "Abril"
    elif month == "5":
        str += "Mayo"
    elif month == "6":
        str += "Junio"
    elif month == "7":
        str += "Julio"
    elif month == "8":
        str += "Agosto"
    elif month == "9":
        str += "Septiembre"
    elif month == "10":
        str += "Octubre"
    elif month == "11":
        str += "Noviembre"
    elif month == "12":
        str += "Diciembre"
    else:
        str += "??? de "

# Only if we want the year
#    str += now.strftime("%Y")

    return str


#### MAIN MODULE

# Randomly selects an image from the original dir
path = r"images_raw"
random_filename = random.choice([
    x for x in os.listdir(path)
    if os.path.isfile(os.path.join(path, x))
])

# Generate file string names
now = datetime.datetime.now()
filestringext = os.path.splitext("images/"+random_filename)
filestringname = now.strftime("%Y")+now.strftime("%m")+now.strftime("%d")
filestringextension = filestringext[1]
filestringfullname = now.strftime("%Y")+now.strftime("%m")+now.strftime("%d")+filestringext[1]


# Move selected image from original dir to the processed one using the date as filename
os.system("mv images_raw/"+random_filename+" images/"+filestringfullname)

# process image
with Image(filename="images/"+filestringfullname) as img:
    date_text = date_string()

    with img.clone() as i:
        with Drawing() as draw:
            i = adjust_width_height(i)
            draw.font_family = 'Arial' 
            draw.font_size = 60
            draw.text_antialias = True
            draw.fill_color = Color('WHITE')
            draw.stroke_color = Color('BLACK')
            draw.font_weight = 700
            str_hello = "BUENOS DÍAS"
            metrics = draw.get_font_metrics(i, str_hello, multiline=False)
            draw.text(int((i.width - metrics.text_width)/2), int((metrics.text_height + 20)), str_hello)
            draw.font_size = 40
            metrics = draw.get_font_metrics(i, date_text, multiline=False)
            draw.text(int((i.width - metrics.text_width)/2), int((i.height - metrics.text_height - 20)), date_text)

            i_retro = i.clone()
            draw(i)
#            i.save(filename='images/result/test.jpg')
            i.save(filename='images/'+filestringfullname)

#            with Image(width=100, height=100, pseudo="plasma:") as affinity:
#                i_retro.remap(affinity)
#            i.extent(width=i.width*2)
#            i.composite(i_retro, top=0, left=i_retro.width)


#            i_retro.posterize(levels=4, dither="riemersma")
            i_retro.quantize(number_colors=8, colorspace_type="srgb", treedepth=0, dither=False, measure_error=False)


            i_retro.statistic("median", width=10, height=10)
            i.extent(width=i.width*2)
            i.composite(i_retro, top=0, left=i_retro.width)




            percent = 10
            i_retro.sample(int(i_retro.width / percent), int(i_retro.height / percent))
            i_retro.sample(int(i_retro.width * percent), int(i_retro.height * percent))

            str_hello = "gourmet retro"
            draw.font_size = 30
            metrics = draw.get_font_metrics(i_retro, str_hello, multiline=False)
            draw.text(int((i_retro.width - metrics.text_width)/2), int((metrics.text_height + 100)), str_hello)
            draw(i_retro)

            i_retro.save(filename='images/'+filestringname+"_retro"+filestringextension )
            

            
        os.system("telegram-send --image images/"+filestringfullname+" --caption "+random_filename)
        os.system("telegram-send --image images/"+filestringname+"_retro"+filestringextension+" --caption "+random_filename)




##            draw.font = 'wandtests/assets/League_Gothic.otf'
##draw.font_size = 40
##draw.text(image.width / 2, image.height / 2, 'Hello, world!')
##draw(image)