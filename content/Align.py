#!/usr/bin/env python
# coding: utf-8

# In[3]:


def Align_Horizontal_Vignet():
    import os
    from PIL import Image
    from pylab import *
    import matplotlib
    from matplotlib.pyplot import *
    import numpy
    import math
    #########################################################
    Lieu = os.getcwd()  ##  Permet d'obtenir le chemin du répertoire de travail actuel --> Placé dans Lieu
    Lieu = Lieu + "\Portraits_a_analyser" # Transfo du code pour Pyface
    #############################################################
    """ Retourne une liste d'images jpeg dans un répertoire précis """
    def get_imlist(path):
        imlist=[os.path.join(f) for f in os.listdir(Lieu) if f.endswith(".jpg")]
        return imlist

    #########################################################
    """ Charge une image dans une matrice avec le module pil """
    def charg_image_pil(path,titre_image):
        os.chdir(path)
        pil_im = Image.open(titre_image)
        return pil_im

    """ affiche une image  déjà matricielle 
             par matplotlib """
    def affich_image_array_pil(Matrice_Name):
        image = numpy.array(Matrice_Name)
        gray()
        # plot the image
        imshow(image)
        axis('off')

    ###################################################################
    #""" affiche de multiples photos espacées sur une même ligne
    #provenant d'un unique répertoire """
    def Align_affich_photo_repertoir(path):
        imlist=get_imlist(path)
        long_imlist=len(imlist)
        figure(figsize=(50,long_imlist))
        gray()
        for i in range(long_imlist):
            titre=imlist[i]
            subplot(1,long_imlist,i+1)
            title(titre)
            axis('off')
            matrice=charg_image_pil(path,titre)
            image = numpy.array(matrice)
            imshow(image)
    ###################################################################
    Align_affich_photo_repertoir(Lieu)
    show()

