
from image_processing import generate_image


# Config
main_message= 'BUENOS DIAS'

#### MAIN PROGRAM

main_message_flag = False

# In case a new message is received as parameter, change it
if len(sys.argv) > 1:
    main_message = sys.argv[1]
    main_message_flag = True

rutas = generate_image(main_message, main_message_flag)

print("telegram-send --image "+rutas[0]+" --caption "+rutas[2])
#os.system("telegram-send --image "+rutas[0]+" --caption "+rutas[2])
print("telegram-send --image "+rutas[1]+" --caption "+rutas[2])
#os.system("telegram-send --image "+rutas[1]+" --caption "+rutas[2])
