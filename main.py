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

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_go, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Broche pour avancer à l'image suivante
GPIO.setup(pin_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Broche pour revenir à l'image précédente

chemin_images = "/home/fmj/BAQPython/BAQFMJPython/slides/"

images = [f for f in os.listdir(chemin_images) if f.endswith(('.jpg', '.png', '.jpeg','.JPG', '.PNG', '.JPEG'))]
images = sorted(images, key=lambda x: int(x.split('.')[0]))
images.append("/home/fmj/BAQPython/BAQFMJPython/merci.png")
print(images)

actual_slide = 0

pygame.init()
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Affichage en plein écran

image = pygame.image.load("/home/fmj/BAQPython/BAQFMJPython/start.png")
image = pygame.transform.scale(image, (pygame.display.Info().current_w, pygame.display.Info().current_h))
screen = pygame.display.get_surface()
screen.blit(image, (0, 0))
pygame.display.flip()


def slide_next(channel):
    global actual_slide
    print(actual_slide)
    
    chemin_image = os.path.join(chemin_images, images[actual_slide])
    print("Affichage du slide:", chemin_image)
    if(data["sound"] == True and actual_slide == 0):
        sound.play()
    image = pygame.image.load(chemin_image)
    image = pygame.transform.scale(image, (pygame.display.Info().current_w, pygame.display.Info().current_h))
    screen = pygame.display.get_surface()
    screen.blit(image, (0, 0))
    pygame.display.flip()

    if actual_slide < len(images) - 1:
        actual_slide += 1
        print("Next slide")
    else:
        actual_slide = 0
        print("Stop slide")
        return


def slide_stop(channel):
    global actual_slide
    actual_slide = 0
    image = pygame.image.load("/home/fmj/BAQPython/BAQFMJPython/start.png")
    image = pygame.transform.scale(image, (pygame.display.Info().current_w, pygame.display.Info().current_h))
    screen = pygame.display.get_surface()
    screen.blit(image, (0, 0))
    pygame.display.flip()

def killbaq(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        print("Stopping the BAQ")
        GPIO.cleanup()
        pygame.quit()
        sys.exit()

GPIO.add_event_detect(pin_go, GPIO.FALLING, callback=slide_next, bouncetime=data["debounce"])
GPIO.add_event_detect(pin_stop, GPIO.FALLING, callback=slide_stop, bouncetime=data["debounce"])

try:
    while True:
        for event in pygame.event.get():
            killbaq(event)
        sleep(0.1)

except KeyboardInterrupt:
    print("Stopping the BAQ")
    GPIO.cleanup()
    pygame.quit()