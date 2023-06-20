import json
import RPi.GPIO as GPIO
import os
import pygame
import pygame.mixer
from pygame.locals import *
from time import sleep

# Définition des pin GPIO

pin_go = 16
pin_stop = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_go, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Broche pour avancer à l'image suivante
GPIO.setup(pin_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Broche pour revenir à l'image précédente

# Initialisation de Pygame et Pygame Mixer (audio)
pygame.init()
pygame.mixer.init()
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Affichage en plein écran
sound = pygame.mixer.Sound("/home/fmj/BAQFMJPython/buzz.wav")

# Chargement du fichier de configuration
with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)
    print("Lecture du fichier de config OK")

# Initialisation des slides
chemin_images = "/home/fmj/BAQFMJPython/slides/"
images = [f for f in os.listdir(chemin_images) if f.endswith(('.jpg', '.png', '.jpeg','.JPG', '.PNG', '.JPEG'))]
images = sorted(images, key=lambda x: int(x.split('.')[0]))
actual_slide = 0

###
# Affichage de l'écran de démarrage

image = pygame.image.load("/home/fmj/BAQFMJPython/start.png")
image = pygame.transform.scale(image, (pygame.display.Info().current_w, pygame.display.Info().current_h))
screen = pygame.display.get_surface()
screen.blit(image, (0, 0))
pygame.display.flip()
