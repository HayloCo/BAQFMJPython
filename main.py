import json
import RPi.GPIO as GPIO
import os
import pygame
import pygame.mixer

from time import sleep

pygame.mixer.init()



with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)
    print("Read successful")
print(data)
print(data["sound"])
pin_go = 16
pin_stop = 26
sound = pygame.mixer.Sound("/home/fmj/BAQPython/BAQFMJPython/buzz.wav")


# Configuration des broches GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_go, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Broche pour avancer à l'image suivante
GPIO.setup(pin_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Broche pour revenir à l'image précédente

# Chemin vers le répertoire contenant les images
chemin_images = "/home/fmj/BAQPython/BAQFMJPython/slides/"

# Liste des fichiers d'images présents dans le répertoire
images = [f for f in os.listdir(chemin_images) if f.endswith(('.jpg', '.png', '.jpeg','.JPG', '.PNG', '.JPEG'))]
images = sorted(images, key=lambda x: int(x.split('.')[0]))
print(images)

# Variable pour stocker l'index de l'image actuelle
actual_slide = 0

# Initialisation de pygame
pygame.init()
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Affichage en plein écran

image = pygame.image.load("/home/fmj/BAQPython/BAQFMJPython/start.png")
image = pygame.transform.scale(image, (pygame.display.Info().current_w, pygame.display.Info().current_h))
screen = pygame.display.get_surface()
screen.blit(image, (0, 0))
pygame.display.flip()


# Fonction pour afficher l'image actuelle
def show_slide():
    chemin_image = os.path.join(chemin_images, images[actual_slide])
    print("Affichage du slide:", chemin_image)
    if(data["sound"] == True):
        sound.play()
    
    # Chargement et affichage de l'image
    image = pygame.image.load(chemin_image)
    image = pygame.transform.scale(image, (pygame.display.Info().current_w, pygame.display.Info().current_h))
    screen = pygame.display.get_surface()
    screen.blit(image, (0, 0))
    pygame.display.flip()

# Fonction pour passer à l'image suivante
def slide_next(channel):
    global actual_slide
    if actual_slide < len(images) - 1:
        actual_slide += 1
    else:
        actual_slide = 0
    show_slide()

# Fonction pour revenir à l'image précédente
def slide_stop(channel):
    actual_slide = 0
    image = pygame.image.load("/home/fmj/BAQPython/BAQFMJPython/start.png")
    image = pygame.transform.scale(image, (pygame.display.Info().current_w, pygame.display.Info().current_h))
    screen = pygame.display.get_surface()
    screen.blit(image, (0, 0))
    pygame.display.flip()

def killbaq(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        print("Arrêt du diaporama")
        GPIO.cleanup()
        pygame.quit()
        sys.exit()

# Ajout des gestionnaires d'événements pour les broches GPIO
GPIO.add_event_detect(pin_go, GPIO.FALLING, callback=slide_next, bouncetime=300)
GPIO.add_event_detect(pin_stop, GPIO.FALLING, callback=slide_stop, bouncetime=300)

try:
    while True:
        for event in pygame.event.get():
            killbaq(event)
        sleep(0.1)

except KeyboardInterrupt:
    print("Arrêt du diaporama")
    GPIO.cleanup()
    pygame.quit()