import json
import RPi.GPIO as GPIO
import os
import pygame
from time import sleep


with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)
    print("Read successful")
print(data)

pin_go = 16
pin_stop = 26

# Configuration des broches GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_go, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Broche pour avancer à l'image suivante
GPIO.setup(pin_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Broche pour revenir à l'image précédente

# Chemin vers le répertoire contenant les images
chemin_images = "./slides"

# Liste des fichiers d'images présents dans le répertoire
images = sorted([f for f in os.listdir(chemin_images) if f.endswith(('.jpg'))])
print(images)

# Variable pour stocker l'index de l'image actuelle
image_actuelle = 0

# Initialisation de pygame
pygame.init()
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Affichage en plein écran

# Fonction pour afficher l'image actuelle
def afficher_image():
    chemin_image = os.path.join(chemin_images, images[image_actuelle])
    print("Affichage de l'image:", chemin_image)
    
    # Chargement et affichage de l'image
    image = pygame.image.load(chemin_image)
    image = pygame.transform.scale(image, (pygame.display.Info().current_w, pygame.display.Info().current_h))
    screen = pygame.display.get_surface()
    screen.blit(image, (0, 0))
    pygame.display.flip()

# Fonction pour passer à l'image suivante
def slide_next(channel):
    global image_actuelle
    if image_actuelle < len(images) - 1:
        image_actuelle += 1
    else:
        image_actuelle = 0
    afficher_image()

# Fonction pour revenir à l'image précédente
def slide_back(channel):
    global image_actuelle
    if image_actuelle > 0:
        image_actuelle -= 1
    else:
        image_actuelle = len(images) - 1
    afficher_image()

def killbaq(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        print("Arrêt du diaporama")
        GPIO.cleanup()
        pygame.quit()
        sys.exit()

# Ajout des gestionnaires d'événements pour les broches GPIO
GPIO.add_event_detect(pin_go, GPIO.FALLING, callback=slide_next, bouncetime=300)
GPIO.add_event_detect(pin_stop, GPIO.FALLING, callback=slide_back, bouncetime=300)

try:
    while True:
        for event in pygame.event.get():
            killbaq(event)
        sleep(0.1)

except KeyboardInterrupt:
    print("Arrêt du diaporama")
    GPIO.cleanup()
    pygame.quit()