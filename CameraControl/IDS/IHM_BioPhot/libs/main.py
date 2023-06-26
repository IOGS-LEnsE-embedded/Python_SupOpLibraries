# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:54:43 2023

@author: guillaume.chapelant
"""

# https://www.geeksforgeeks.org/radiobutton-in-tkinter-python/

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from pypylon import pylon
import platform
import dlp6500
import numpy
import os

root = tk.Tk()
root.geometry("650x400")
root.title("Interface DMD")


# DEFINITIONS DES FONCTIONS


def reset_b():
    global root
    global dlp

    dlp.stopsequence()

    for widget in root.winfo_children():
        widget.destroy()
    root = nouvelle_page()

def sortir():
    global root
    root.destroy()
    root.quit()


def acquisition():
    global root
    global tau
    global images_to_save_filename
    global dlp

    print('acquisition')

    os.chdir(images_to_save_filename)

    cam.Open()
    cam.ExposureTime = tau.get()
    cam.StartGrabbing()

    dlp.startsequence() # Synchronisation de la séquence avec la caméra

    for image in liste_images['values']:
        with cam.RetrieveResult(5000) as result:

            # Calling AttachGrabResultBuffer creates another reference to the
            # grab result buffer. This prevents the buffer's reuse for grabbing.
            img.AttachGrabResultBuffer(result)

            if platform.system() == 'Windows':
                # The JPEG format that is used here supports adjusting the image
                # quality (100 -> best quality, 0 -> poor quality).
                ipo = pylon.ImagePersistenceOptions()
                quality = 100
                ipo.SetQuality(quality)

                filename = str(os.path.splitext(os.path.basename(image))[0]) + "_fluorescence.jpeg"
                img.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)
            else:
                filename = str(os.path.splitext(os.path.basename(image))[0]) + "_fluorescence.png"
                img.Save(pylon.ImageFileFormat_Png, filename)

            # In order to make it possible to reuse the grab result for grabbing
            # again, we have to release the image (effectively emptying the
            # image object).
            img.Release()

    cam.StopGrabbing()
    cam.Close()


def Charger_images_fun():
    global root
    global dlp
    global tau
    print('Charger les images')

    images = []
    for image in liste_images['values']:
        images.append((numpy.asarray(Image.open(image))))

    dlp.stopsequence()

    dlp.changemode(3)

    exposure = [tau.get()] * len(images) # us
    dark_times = [1000000] * len(images) # us
    trigger_in = [False] * len(images)
    trigger_out = [1] * len(images)

    dlp.defsequence(images, exposure, trigger_in, dark_times, trigger_out, 0)

    images_chargees()


def explorateur():
    global root
    tk.Tk().withdraw()
    filename = filedialog.askopenfilenames(initialdir="/",
                                           title="Select a File",
                                           filetypes=(("Bitmap", "*.bmp*"), ("all files", "*.*")))
    liste_images['values'] = filename


def images_chargees():
    global root
    charger_images.configure(text='Images Chargées', font=('Bahnschrift', 9), fg="green")


def explorateur_image():
    global root
    global fichier
    global images_to_save_filename
    tk.Tk().withdraw()
    images_to_save_filename = filedialog.askdirectory()
    fichier.configure(text=images_to_save_filename, width=40)
    # text=""
    # for k in range(0,len(filename)-1):
    #      text=text+filename[k]+"\n"
    # nom_image.configure(text="Images ouvertes : \n\n"+text)


def nouvelle_page():
    global root
    global dlp
    global cam
    global camera_ok
    global DMD_ok
    global liste_images
    global charger_images
    global charger_fichier
    global fichier
    global tau
    global images_to_save_filename

    print('Nouvelle Page')

    #### FIN ###

    # Titres :

    Titre = tk.Label(root, text='INTERFACE DMD', font=('Bahnschrift', 20, 'bold'))

    # Labels :

    nom_image = tk.Label(root, text='IMAGES', font=('calibre', 10, 'bold'), fg="green")

    # Reglage temps d'intégration
    tau=tk.IntVar()
    cam.Open()
    scale=tk.Scale(root,variable=tau,from_=cam.ExposureTime.Min,to=cam.ExposureTime.Max/10,orient=tk.HORIZONTAL)
    cam.Close()

    # MESSAGES :

    camera_ok = tk.Label(root, text='Camera déconectée', bg="red", font=('Bahnschrift', 9))
    DMD_ok = tk.Label(root, text='DMD déconnecté', bg="red", font=('Bahnschrift', 9))
    fichier = tk.Label(root, text=' ', font=('Bahnschrift', 9, 'bold'))
    temps_int_mess=tk.Label(root,text="temps d'exposition en us", font=('Bahnschrift', 9))
    # Boutons :

    explorateur_bouton = tk.Button(root, text="Choisir les images", command=explorateur, font=('Bahnschrift', 9))
    sortie = tk.Button(root, text="Sortir", command=sortir)
    charger_images = tk.Button(root, text="Charger les images", command=Charger_images_fun, font=('Bahnschrift', 9))
    charger_fichier = tk.Button(root, text="Enregistrer les images", command=explorateur_image, font=('Bahnschrift', 9))
    reset_bouton = tk.Button(root, text="RESET", command=reset_b, fg="red", font=('Bahnschrift', 9, 'bold'))
    acq_bouton = tk.Button(root, text="LANCER", command=acquisition, fg="green", font=('Bahnschrift', 13, 'bold'))
    # IMAGES :

    n = tk.StringVar()
    liste_images = ttk.Combobox(root, width=40, textvariable=n)
    liste_images['values'] = ""

    # Tailles colonnes :

    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=0)
    root.columnconfigure(2, weight=0)

    # ESPACES

    esp0 = tk.Label(root, text="  ")
    esp1 = tk.Label(root, text="")
    esp2 = tk.Label(root, text="")
    esp3 = tk.Label(root, text="")
    esp4 = tk.Label(root, text="")
    esp5 = tk.Label(root, text="", font=('calibre', 5))
    esp6 = tk.Label(root, text="")
    esp7 = tk.Label(root, text="", font=('calibre', 5))

    # Placements
    esp0.grid(row=0, column=0, sticky='w')
    Titre.grid(row=1, column=0, columnspan=40)
    esp4.grid(row=2, column=1, sticky='w')

    explorateur_bouton.grid(row=3, column=2, sticky='w')
    esp1.grid(row=3, column=3, sticky='w')
    liste_images.grid(row=3, column=4)
    esp2.grid(row=3, column=5, sticky='w')
    charger_images.grid(row=3, column=6, sticky='w')

    esp3.grid(row=4, column=1, sticky='w')

    # nom_image.grid(row=2,column=2,sticky='w')
    temps_int_mess.grid(row=6, column=6, sticky='w')
    scale.grid(row=7, column=6, sticky='w')
    DMD_ok.grid(row=5, column=4, sticky='w')
    esp5.grid(row=6, column=1, sticky='w')
    camera_ok.grid(row=7, column=4, sticky='w')

    sortie.grid(row=12, column=8, sticky='w')
    reset_bouton.grid(row=13, column=8, sticky='w')
    esp6.grid(row=8, column=1, sticky='w')
    charger_fichier.grid(row=9, column=2, sticky='w')
    fichier.grid(row=9, column=4, sticky='w')
    acq_bouton.grid(row=11, column=6, sticky='w')
    esp7.grid(row=10, column=6, sticky='w')

    if dlp.connection_established():
        DMD_ok.configure(text='DMD connecté', bg="lightgreen")

    if cam is not None:
        camera_ok.configure(text='Camera connectée', bg="lightgreen")

    return root


dlp = dlp6500.dmd()

img = pylon.PylonImage()
tlf = pylon.TlFactory.GetInstance()
cam = pylon.InstantCamera(tlf.CreateFirstDevice())

root = nouvelle_page()

# Boucle infinie pour l'affichage
root.mainloop()
