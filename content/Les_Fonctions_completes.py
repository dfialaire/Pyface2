import pickle
from ipywidgets import widgets
import numpy
import matplotlib
from matplotlib.pyplot import *
from math import *
import  matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from PIL import ImageChops
import os
import sys, time
Lieu = os.getcwd()
##############################################################################
def Input_choix_Photo_Compare(change):
    global Photo_Compar_Base
    Photo_Compar_Base = change['new']
    print()
    print("Récupération du choix = ",Photo_Compar_Base)
    Reconnaissance_Faciale(Photo_Compar_Base)
###################################################################
""" Retourne une liste d'images jpeg dans un répertoire précis """
def get_imlist(path):
    imlist=[os.path.join(f) for f in os.listdir(Lieu) if (f.endswith(".jpg") or f.endswith(".png"))]
    return imlist
#########################################################
""" Charge une image dans une matrice avec le module pil """
def charg_image_pil(path,titre_image):
    path = '/drive/Portraits_a_analyser'
    os.chdir(path)
    pil_im = Image.open(titre_image)
    return pil_im
#########################################################
""" affiche une image  déjà matricielle 
         par matplotlib """
def affich_image_array_pil(Matrice_Name):
    image = numpy.array(Matrice_Name)
    gray()
    imshow(image)
    axis('off')
###################################################################
#""" affiche de multiples photos espacées sur une même ligne
#provenant d'un unique répertoire """
def Align_affich_photo_repertoir(path, Liste_Photos):
    imlist= Liste_Photos  # get_imlist(path)
    long_imlist=len(imlist)
    figure(figsize=(50,long_imlist))
    gray()
    for i in range(1, long_imlist):
        titre=imlist[i]
        titre2 = titre[0:-4]
        subplot(1,long_imlist,i+1)
        title(titre2 , fontsize="35")
        axis('off')
        matrice=charg_image_pil(path,titre)
        image = numpy.array(matrice)
        imshow(image)
###################################################################
#################################################################
def Align_Horizontal_Vignet(Liste_Photos):
    Lieu = os.getcwd()
    Lieu = Lieu + "/Portraits_a_analyser" # Transfo du code pour Pyface
    Align_affich_photo_repertoir(Lieu, Liste_Photos)
    Lieu = os.getcwd()
    show()
#############################################################################
def Position_lign(fichier,mode):
    os.chdir(Lieu+"/Travail_Brouillon")
    matrice = Image.open(fichier)
    matrice=matrice.convert('L')   ##x##
    tab_matrice=np.array(matrice)   ##x##
    list1=[]
    ##################################################
    largeur_image=matrice.size[0]   ##x##
    hauteur_image=matrice.size[1]   ##x##
    ###################################################
    if mode==1:
        for x in range(hauteur_image):
            val= tab_matrice[x][10]
            if val<100:
                listo=[x,val]
                list1.append(listo)
            else:
                z=1
    else:
        for y in range(largeur_image):
            val= tab_matrice[10][y]
            if val<100:
                listo=[y,val]
                list1.append(listo)
            else:
                z=1
    return list1
######################################################################
def lissage(list1):
    list4=[]
    long_list1=len(list1)
    for aa in range(long_list1-1):
        val=list1[aa+1][0]-list1[aa][0]
        if val==1:
            z=1
        else:
            list4.append(list1[aa][0])
    return list4
##########################################################################
def calcul_distance(list4):
    list5=[]
    list6=[]
    long_list4=len(list4)
    for i in range(1,long_list4-1):
        distance=list4[i+1]-list4[i]
        list5.append(distance)
    list5.sort()
    somme=sum(list5)
    long_list5=len(list5)
    mini=min(list5)
    for bb in range(long_list5):
        valo=list5[bb]
        vali=round(valo/mini,2)
        list6.append(vali)
    return list6,mini,somme
#############################################################################
###########################  Partie du code provenant d'un enseignant de l'académie
#################################  de Clermont Ferrand ** Merci à lui/elle
def quantite(tri1,tri2):
    # d=(tri1[0]-tri2[0])**2+(tri1[1]-tri2[1])**2+(tri1[2]-tri2[2])**2
    d=(tri1-tri2)**2
    return(d)
def contours(image,Nom4,seuil):
    (c,l)=image.size
    imagearrivee=Image.new('L',(c,l))
    for x in range(1,c-1):
        for y in range(1,l-1):
            p=image.getpixel((x,y))
            p1=image.getpixel((x-1,y-1))
            q1=quantite(p,p1)
            p2=image.getpixel((x-1,y))
            q2=quantite(p,p2)
            p3=image.getpixel((x-1,y+1))
            q3=quantite(p,p3)
            p4=image.getpixel((x,y-1))
            q4=quantite (p,p4)
            p5=image.getpixel((x,y+1))
            q5=quantite (p,p5)
            p6=image.getpixel((x+1,y-1))
            q6=quantite(p,p6)
            p7=image.getpixel((x+1,y))
            q7=quantite(p,p7)
            p8=image.getpixel((x+1,y+1))
            q8=quantite (p,p8)
            if q1+q2+q3+q4+q5+q6+q7+q8<seuil:
                imagearrivee.putpixel((x,y),(255))
            else :
                imagearrivee.putpixel((x,y),(0))
    imagearrivee.save(Nom4)
#############################################################################
#################################  verticale
def quantite_vert(tri1,tri2):
    d=((tri1-tri2)**2)
    return(d)
def contours_vert(image,Nom4,seuil):
    (c,l)=image.size
    imagearrivee=Image.new('L',(c,l))
    for x in range(1,c-1):
        for y in range(1,l-1):
            p=image.getpixel((x,y))
            p1=image.getpixel((x-1,y-1))
            q1=quantite_vert(p,p1)
            p2=image.getpixel((x-1,y))
            q2=quantite_vert(p,p2)
            p3=image.getpixel((x-1,y+1))
            q3=quantite_vert(p,p3)
            p4=image.getpixel((x,y-1))
            q4=quantite_vert (p,p4)
            p5=image.getpixel((x,y+1))
            q5=quantite_vert (p,p5)
            p6=image.getpixel((x+1,y-1))
            q6=quantite_vert(p,p6)
            p7=image.getpixel((x+1,y))
            q7=quantite_vert(p,p7)
            p8=image.getpixel((x+1,y+1))
            q8=quantite_vert (p,p8)
            #val=(8*p)- (p2+p7)
            if q1+q2+q3+q4+q5+q6+q7+q8<seuil:
                imagearrivee.putpixel((x,y),(255))
            else :
                imagearrivee.putpixel((x,y),(0))
    imagearrivee.save(Nom4)
#############################################################################
def  affich_image(Lien_image):
    from IPython.display import Image, display
    display(Image(filename=Lien_image))
#############################################################################
def Accolade_photo(a,b,mode):
    matrice_portrait = Image.open(a, "r")
    matrice_portrait= matrice_portrait.convert('L')
    tab_matrice_portrait = np.array(matrice_portrait)
    largeur_image_portrait=matrice_portrait.size[0]
    hauteur_image_portrait=matrice_portrait.size[1]
    #############################################################################
    matrice_portrait_inv = Image.open(b, "r")
    matrice_portrait_inv= matrice_portrait_inv.convert('L')
    tab_matrice_portrait_inv = np.array(matrice_portrait_inv)
    largeur_image_portrait_inv=matrice_portrait_inv.size[0]
    hauteur_image_portrait_inv=matrice_portrait_inv.size[1]
    #############################################################################
    if hauteur_image_portrait>hauteur_image_portrait_inv:
        xmax=hauteur_image_portrait
    else:
        xmax=hauteur_image_portrait_inv
    ######################################################################
    ymax=largeur_image_portrait_inv+largeur_image_portrait+4
    ######################################################################
    newmatrice = numpy.empty((xmax, ymax, 3), dtype = numpy.uint8)
    ######################################################################
    for x in range(hauteur_image_portrait):
        for y in range(largeur_image_portrait):
            newmatrice[x,y]=tab_matrice_portrait[x,y],tab_matrice_portrait[x,y],tab_matrice_portrait[x,y]
    ######################################################################
    for x in range(hauteur_image_portrait_inv):
        for y in range(largeur_image_portrait_inv):
            ypos=y+largeur_image_portrait+4
            newmatrice[x,ypos]=tab_matrice_portrait_inv[x,y],tab_matrice_portrait_inv[x,y],tab_matrice_portrait_inv[x,y]
    ######################################################################
    if mode==1:
        newmatrice_img = Image.fromarray(newmatrice)
        newmatrice_img.save("newmat.jpg", "JPEG")
    else:
        newmatrice_img = Image.fromarray(newmatrice)
        newmatrice_img.save("newmat_vert.jpg", "JPEG")
    return newmatrice_img       ##y##
#############################################################################
###########################################################################
def Lign_verticale(Photo_initiale):
    mode=2
    Deb_Photo_initiale=""
    long_Photo_initiale=len(Photo_initiale)
    for a in range(long_Photo_initiale-4):
        Deb_Photo_initiale=Deb_Photo_initiale+Photo_initiale[a]
    os.chdir(Lieu+"/Portraits_a_analyser")
    matrice = Image.open(Photo_initiale, "r")
    matrice=matrice.convert('L') ##x##
    ##################################################
    os.chdir(Lieu+"/Travail_Brouillon")
  #######################################################
    largeur_image=matrice.size[0] ##x##
    hauteur_image_vert=largeur_image
    hauteur_image=matrice.size[1] ##x##
  #######################################################
    Rotatematrice = numpy.empty((largeur_image,hauteur_image, 3), dtype = numpy.uint8)
    #print("Rotatematrice.shape=",Rotatematrice.shape)
    tab_matrice=np.array(matrice)
    for x in range(hauteur_image):
        for y in range(largeur_image):

            Rotatematrice[largeur_image-1-y,x]=tab_matrice[x,y],tab_matrice[x,y],tab_matrice[x,y]
    Rotatematrice_img=Image.fromarray(Rotatematrice)##x##
    Rotatematrice_img=Rotatematrice_img.convert('L')
    Rotatematrice_img.save("photo_retourn.jpg", "JPEG")##x##
    #########################################################
    tab_moy_vertical=np.zeros((largeur_image,1),dtype='i')
    for x in range(largeur_image):
        somme=0
        for y in range(hauteur_image):    ##x##
            val=Rotatematrice_img.getpixel((y,x))    ##x##
            somme=somme+val    ##x##
        moyenne=somme/hauteur_image    ##x##
        tab_moy_vertical[x][0]=moyenne    ##x##
    #######################################################
    newmatrice_vert = numpy.empty((hauteur_image, largeur_image, 3), dtype = numpy.uint8)
    newmatrice_vert = np.array(matrice)    ##x##
    ############################################
    Newmatrice_vert_img=Image.fromarray(newmatrice_vert)##x##
    Newmatrice_vert_img.save("base_pour_Verticale.jpg", "JPEG")    ##x##
    #####################################################
    newImg = numpy.empty((largeur_image,hauteur_image, 3), dtype = numpy.uint8)
    for x in range(largeur_image):
        for y in range(hauteur_image):
            newImg[x,y]=[tab_moy_vertical[x][0],tab_moy_vertical[x][0],tab_moy_vertical[x][0]]
    newImg_img=Image.fromarray(newImg)##x##
    newImg_img.save("barres verticales.jpg", "JPEG")    ##x##
    po_clai=newImg*2
    po_clai_img=Image.fromarray(po_clai)    ##x##
    po_clai_img.save("po_clai.jpg", "JPEG")    ##x##
    ##############################################
    Nom1=Deb_Photo_initiale+"_matrice_Vert.jpg"    ##x##
    newmatrice_vert_img=Image.fromarray(newmatrice_vert)    ##x##
    newmatrice_vert_img.save(Nom1, "JPEG")    ##x##
    #######################################################
    Nom2=Deb_Photo_initiale+"_matrice_barre_Vert.jpg"    ##x##
    Rotatematrice_img=Rotatematrice_img.convert('L')    ##x##
    im_size = Rotatematrice_img.size    ##x##
    portrait_barr = Image.new('L', im_size)
    po_clai_img=po_clai_img.convert('L')    ##x##
    portrait_barr = ImageChops.blend(Rotatematrice_img, po_clai_img, 0.6)    ##x##
    tab_portrait_barr = np.array (portrait_barr)    ##x##
############################################################
    portrait_barr_retourn = numpy.empty((hauteur_image,largeur_image, 3), dtype = numpy.uint8)
    for x in range(hauteur_image):
        for y in range(largeur_image):
            portrait_barr_retourn[x][y]=tab_portrait_barr[largeur_image-1-y][x]    ##x##
######################################################################
    portrait_barr_retourn_img=Image.fromarray(portrait_barr_retourn)    ##x##
    portrait_barr_retourn_img.save(Nom2, "JPEG")    ##x##
    Nom3=Deb_Photo_initiale+"_barre_Vert.jpg"    ##x##
############################################################
    po_clai_retourn = numpy.empty((hauteur_image,largeur_image, 3), dtype = numpy.uint8)
    for x in range(hauteur_image):
        for y in range(largeur_image):
            po_clai_retourn[x][y]=po_clai[largeur_image-1-y][x]
    po_clai_retourn_img=Image.fromarray(po_clai_retourn)    ##x##
    po_clai_retourn_img.save("po_clai_retourn_img.jpg", "JPEG")
######################################################################
    po_clai_retourn_img=Image.fromarray(po_clai_retourn)    ##x##
    po_clai_retourn_img.save(Nom3, "JPEG")    ##x##
    ###############################
    Nom4_vert=Deb_Photo_initiale+"_ligne_Vert.jpg"    ##x##
    im=Image.open(Nom3)
    im=im.convert('L')    ##x##
    seuil_vertical=76 # modif 76
    contours_vert(im,Nom4_vert,seuil_vertical)
    ########################
    NewNom4 = Image.open(Nom4_vert)
    im_size = newmatrice_vert.shape    ##x##
    portrait_lignes = Image.new('L', im_size)
    newmatrice_vert_img=Image.fromarray(newmatrice_vert)    ##x##
    newmatrice_vert_img=newmatrice_vert_img.convert('L')    ##x##
    NewNom4=NewNom4.convert('L')    ##x##
    portrait_lignes = ImageChops.blend(newmatrice_vert_img, NewNom4, 0.5)    ##x##
    Nom5_vert=Deb_Photo_initiale+"_ligne_seule_Vert.jpg"    ##x##
    portrait_lignes.save(Nom5_vert, "JPEG")    ##x##
    ##############################
    a=Nom1
    b=Nom2
    Accolade_photo(a,b,mode)
    #################################################
    a="newmat_vert.jpg"    ##x##
    b=Nom3
    Accolade_photo(a,b,mode)
    #######################################"
    a="newmat_vert.jpg"    ##x##
    b=Nom4_vert
    Accolade_photo(a,b,mode)
    #################################################
    a="newmat_vert.jpg"    ##x##
    b=Nom5_vert
    newmatrice_vert_img=Accolade_photo(a,b,mode)
    #######################################"
    return Nom4_vert,Nom5_vert,newmatrice_vert_img,hauteur_image_vert
###########################################################################
def Lign_horizont(Photo_initiale):
    mode=1
    Deb_Photo_initiale=""
    long_Photo_initiale=len(Photo_initiale)
    for a in range(long_Photo_initiale-4):
        Deb_Photo_initiale=Deb_Photo_initiale+Photo_initiale[a]
    os.chdir(Lieu+"/Portraits_a_analyser")
    matrice = Image.open(Photo_initiale, "r")
    matrice= matrice.convert('L')
    ##################################################
    os.chdir(Lieu+"/Travail_Brouillon")
    ##################################################
    largeur_image=matrice.size[0]
    hauteur_image=matrice.size[1]
    #########################################################
    tab_moy_horizon=np.zeros((hauteur_image,1),dtype='i')
    for y in range(hauteur_image):
        somme=0
        for x in range(largeur_image):
            val=matrice.getpixel((x,y))
            somme=somme+val
        moyenne=somme/largeur_image
        tab_moy_horizon[y][0]=moyenne
    #######################################################
    newmatrice = numpy.empty((hauteur_image, largeur_image, 3), dtype = numpy.uint8)
    newmatrice = np.array(matrice)
            ###########################
    newImg = numpy.empty((hauteur_image, largeur_image, 3), dtype = numpy.uint8)
    for x in range(hauteur_image):
        for y in range(largeur_image):
            newImg[x,y]=[tab_moy_horizon[x][0],tab_moy_horizon[x][0],tab_moy_horizon[x][0]]
    #####################################################
    po_clai=newImg*3
    po_clai_img = Image.fromarray(po_clai)
    ##############################################
    Nom1=Deb_Photo_initiale+"_matrice.jpeg"
    newmatrice_img = Image.fromarray(newmatrice) # Transformation du tableau en image PIL
    newmatrice_img.save(Nom1, "JPEG")
    #######################################################
    Nom2=Deb_Photo_initiale+"_matrice_barre.jpeg"
    im_size = newmatrice_img.size
    portrait_barr = Image.new('L', im_size)
    po_clai_img.save("po_clai_img.jpeg", "JPEG")
    im1=newmatrice_img
    im2=po_clai_img
    im1= im1.convert('L')
    im2= im2.convert('L')
    portrait_barr = ImageChops.blend(im1, im2, 0.55)
    portrait_barr.save(Nom2, "JPEG")
    Nom3=Deb_Photo_initiale+"_barre.jpg"
    im2.save(Nom3, "JPEG")
    ###############################
    Nom4=Deb_Photo_initiale+"_ligne.jpg"
    im=Image.open(Nom3)
    seuil_horizon=750 # modif 750
    contours(im,Nom4,seuil_horizon)
    ########################
    NewNom4 = Image.open(Nom4)
    im_size = newmatrice.shape
    portrait_lignes = Image.new('L', im_size)
    newmatrice_img = Image.fromarray(newmatrice)
    newmatrice_img=newmatrice_img.convert('L')
    NewNom4=NewNom4.convert('L')
    portrait_lignes = ImageChops.blend(newmatrice_img, NewNom4, 0.5)
    Nom5=Deb_Photo_initiale+"_ligne_seule.jpg"
    portrait_lignes.save(Nom5, "JPEG")
    ##############################
    a=Nom1
    b=Nom2
    Accolade_photo(a,b,mode)
    #################################################
    a="newmat.jpg"
    b=Nom3
    Accolade_photo(a,b,mode)
    #######################################"
    a="newmat.jpg"
    b=Nom4
    Accolade_photo(a,b,mode)
    #################################################
    a="newmat.jpg"
    b=Nom5
    newmatrice_img=Accolade_photo(a,b,mode)   ##y##
    #######################################"
    return Nom4,Nom5,newmatrice_img,hauteur_image     ##y##
######################################################################
def Analyse_une_nouvelle_photo_suite(change):
    ##
    choix = change['new']
    if choix == " _ ":
        rien = 1
    else:
    ####################################################################
        Photo_initiale= choix
        Nom4,Nom5,newmatrice_img,hauteur_image=Lign_horizont(Photo_initiale)   ##y##
        Nom4_vert,Nom5_vert,newmatrice_vert_img,hauteur_image_vert=Lign_verticale(Photo_initiale)   ##x##
        print("##############################################")
        print("\n     --> Voici le résultat des analyses graphiques :")
        affich_image("newmat.jpg")   ##x##
        affich_image("newmat_vert.jpg")   ##x##
        quest="o" 
        quest=quest.lower()
        if quest=="n":
            z=1
        else:
            os.chdir(Lieu+"/Base_de_Donnees")
            newmatrice_img.save(Nom4, "JPEG")   ##x##
            newmatrice_vert_img.save(Nom4_vert, "JPEG")   ##x##
            os.chdir(Lieu+"/Portraits_a_analyser")
            fichier=Nom4
            mode=1  # horizontal
            list1=Position_lign(fichier,mode)
            list4=lissage(list1)
            print("\n Liste des positions des lignes horizontales : ",list4)
            list6,mini,somme1=calcul_distance(list4)
            print("""  ==>  Voici la liste des distances (raccourcies par""",mini,""") entre les lignes horizontales :
                """,list6,"""
                : Cela constitue le matricule d'identification horizontal de cette photo.""")
            ######################################################################################
            fichier=Nom4_vert
            mode=2
            list1=Position_lign(fichier,mode)
            list4=lissage(list1)
            print("\n Liste des positions des lignes verticales : ",list4)
            list6_vert,mini_vert,somme1_vert=calcul_distance(list4)
            print("""  ==>  Voici la liste des distances (raccourcies par""",mini_vert,""") entre les lignes verticales :
                """,list6_vert,"""
                : Cela constitue le matricule d'identification vertical de cette photo.""")
    #######################################################################################################################"
    #####################""   Test s'il y a déjà un élément en base de donnée ?
            Presence_BD=0
            try:
                New_Baz_Donnees_Photos=[Photo_initiale,list6,Nom4,mini,hauteur_image,list6_vert,Nom4_vert,mini_vert,hauteur_image_vert]
                ###########################################
                Name_local_baz=Lieu+"/Base_de_Donnees/Baz_Analyz_Photos.pickle"
                pickle_in=open(Name_local_baz,"rb")
                Baz_Donnees_Photos_lu=pickle.load(pickle_in)
                pickle_in.close()
                Presence_BD=1
            except FileNotFoundError:
                Presence_BD=0
            if Presence_BD==0:
                ##########################################""
                  ##Enregistrement initial obligatoire lors du début de la base de donnée,
                  ##lignes à effacer ensuite pour ne commencer que par une lecture !
                ####################################################################
                Baz_Donnees_Photos_init=[[Photo_initiale,list6,Nom4,mini,hauteur_image,list6_vert,Nom4_vert,mini_vert,hauteur_image_vert]]
                Name_local_baz=Lieu+"/Base_de_Donnees/Baz_Analyz_Photos.pickle"
                pickle_out=open(Name_local_baz,"wb+")
                pickle.dump(Baz_Donnees_Photos_init,pickle_out)
                pickle_out.close()
                #####################################"""
            else:
                New_Baz_Donnees_Photos=[Photo_initiale,list6,Nom4,mini,hauteur_image,list6_vert,Nom4_vert,mini_vert,hauteur_image_vert]
                ###########################################
                Name_local_baz=Lieu+"/Base_de_Donnees/Baz_Analyz_Photos.pickle"
                pickle_in=open(Name_local_baz,"rb")
                Baz_Donnees_Photos_lu=pickle.load(pickle_in)
                pickle_in.close()
                Baz_Donnees_Photos_lu.append(New_Baz_Donnees_Photos)
                ############################################""
                pickle_out=open(Name_local_baz,"wb+")
                pickle.dump(Baz_Donnees_Photos_lu,pickle_out)
                pickle_out.close()
####################################################################
def Analyse_une_nouvelle_photo():
    os.chdir(Lieu+"/Portraits_a_analyser")
    list_fichiers=os.listdir('.')
    longueur_list_fichiers=len(list_fichiers)
    ###########################################
    print("\nVous souhaitez lancer l'analyse sur quelle photo..")
    # print("\n            * Choix N° 0 :  Quitter.")
    print()
    for l in range(longueur_list_fichiers):
        long_list_fichiers=len(list_fichiers[l])
        fin_nom_fichier_lu=list_fichiers[l][long_list_fichiers-4:long_list_fichiers]
        Deb_nom_fichier_lu=list_fichiers[l][0:2]
        if fin_nom_fichier_lu==".png" or fin_nom_fichier_lu==".jpg":
            if Deb_nom_fichier_lu!="~$":
                rien = 1
            else:
                z=1
        else:
            z=1
    print()
    ##
    list_fichiers = [" _ "] + list_fichiers
    Align_Horizontal_Vignet(list_fichiers)
    ####
    Choix_Photo=widgets.RadioButtons(
                options=list_fichiers,
        value=" _ ",
                layout={'width': 'max-content'}
            )
    Choix_Photo.observe(Analyse_une_nouvelle_photo_suite,names='value')
    ###########################################
    display(Choix_Photo) 
    ##################################################################"
def Analyse_une_serie_de_photo_enrichissement_Base_de_donnees():
    os.chdir(Lieu+"/Portraits_a_analyser")
    list_fichiers=os.listdir('.')
    longueur_list_fichiers=len(list_fichiers)
    ###########################################
    for gg in range(longueur_list_fichiers):
        numero_texte=gg+1
    ####################################################################
        Photo_initiale=list_fichiers[numero_texte-1]
        Nom4,Nom5,newmatrice,hauteur_image=Lign_horizont(Photo_initiale)
        Nom4_vert,Nom5_vert,newmatrice_vert,hauteur_image_vert=Lign_verticale(Photo_initiale)
        print("##############################################")
        print("\n     --> Voici le résultat des analyses graphiques :")
        affich_image("newmat.jpg")
        affich_image("newmat_vert.jpg")
        quest="o" 
        quest=quest.lower()
        if quest=="n":
            z=1
        else:
            os.chdir(Lieu+"/Base_de_Donnees")
            newmatrice.save(Nom4, "JPEG")
            newmatrice_vert.save(Nom4_vert, "JPEG")
            os.chdir(Lieu+"/Portraits_a_analyser")
            fichier=Nom4
            mode=1  # horizontal
            list1=Position_lign(fichier,mode)
            list4=lissage(list1)
            print("\n Liste des positions des lignes horizontales : ",list4)
            list6,mini,somme1=calcul_distance(list4)
            print("""  ==>  Voici la liste des distances (raccourcies par""",mini,""") entre les lignes horizontales :
                """,list6,"""
                : Cela constitue le matricule d'identification horizontal de cette photo.""")
            ######################################################################################
            fichier=Nom4_vert
            mode=2
            list1=Position_lign(fichier,mode)
            list4=lissage(list1)
            print("\n Liste des positions des lignes verticales : ",list4)
            list6_vert,mini_vert,somme1_vert=calcul_distance(list4)
            print("""  ==>  Voici la liste des distances (raccourcies par""",mini_vert,""") entre les lignes verticales :
                """,list6_vert,"""
                : Cela constitue le matricule d'identification vertical de cette photo.""")
    #######################################################################################################################"
    #####################""   Test s'il y a déjà un élément en base de donnée ?
            Presence_BD=0
            try:
                New_Baz_Donnees_Photos=[Photo_initiale,list6,Nom4,mini,hauteur_image,list6_vert,Nom4_vert,mini_vert,hauteur_image_vert]
                ###########################################
                Name_local_baz=Lieu+"/Base_de_Donnees/Baz_Analyz_Photos.pickle"
                pickle_in=open(Name_local_baz,"rb")
                Baz_Donnees_Photos_lu=pickle.load(pickle_in)
                pickle_in.close()
                Presence_BD=1
            except FileNotFoundError:
                Presence_BD=0
            if Presence_BD==0:
                ##########################################""
                  ##Enregistrement initial obligatoire lors du début de la base de donnée,
                  ##lignes à effacer ensuite pour ne commencer que par une lecture !
                ####################################################################
                Baz_Donnees_Photos_init=[[Photo_initiale,list6,Nom4,mini,hauteur_image,list6_vert,Nom4_vert,mini_vert,hauteur_image_vert]]
                Name_local_baz=Lieu+"/Base_de_Donnees/Baz_Analyz_Photos.pickle"
                #pickle_out=open("C:/Users/dfial/Desktop/Travail_Python/Image/Photographie_Num/Py_Face/Base_de_Donnees/Baz_Analyz_Photos.pickle","wb+")
                pickle_out=open(Name_local_baz,"wb+")
                pickle.dump(Baz_Donnees_Photos_init,pickle_out)
                pickle_out.close()
                #####################################"""
            else:
                New_Baz_Donnees_Photos=[Photo_initiale,list6,Nom4,mini,hauteur_image,list6_vert,Nom4_vert,mini_vert,hauteur_image_vert]
                ###########################################
                Name_local_baz=Lieu+"/Base_de_Donnees/Baz_Analyz_Photos.pickle"
                #pickle_in=open("C:/Users/dfial/Desktop/Travail_Python/Image/Photographie_Num/Py_Face/Base_de_Donnees/Baz_Analyz_Photos.pickle","rb")
                pickle_in=open(Name_local_baz,"rb")
                Baz_Donnees_Photos_lu=pickle.load(pickle_in)
                pickle_in.close()
                Baz_Donnees_Photos_lu.append(New_Baz_Donnees_Photos)
                ############################################""
                Name_local_baz=Lieu+"/Base_de_Donnees/Baz_Analyz_Photos.pickle"
                pickle_out=open(Name_local_baz,"wb+")
                pickle.dump(Baz_Donnees_Photos_lu,pickle_out)
                pickle_out.close()
#####################################################
def Choix_Photo_de_base():
    os.chdir(Lieu)
    affich_image("Logo4.jpg")
    Name_local_baz=Lieu+"/Base_de_Donnees/Baz_Analyz_Photos.pickle"
    pickle_in=open(Name_local_baz,"rb")
    Baz_Donnees_Photos_lu=pickle.load(pickle_in)
    pickle_in.close()
    long_Baz_Donnees_Photos_lu=len(Baz_Donnees_Photos_lu)
    print()
    print("Baz_Donnees_Photos_lu = ",Baz_Donnees_Photos_lu)
    ################
    print("\n             ==> Voici les photos analysées présentes dans la base de données :")
    print()
    print("                      * Quitter :    -->   N°_0")
    print()
    Liste_Photos = [" _ "]
    for tt in range(long_Baz_Donnees_Photos_lu):
        Liste_Photos.append(  Baz_Donnees_Photos_lu[tt][0]   )
    Align_Horizontal_Vignet(Liste_Photos)
    ####
    Choix_Photo=widgets.RadioButtons(
                options=Liste_Photos,
        value=" _ ",
                layout={'width': 'max-content'}
            )
    Choix_Photo.observe(Input_choix_Photo_Compare,names='value')
    ###########################################
    display(Choix_Photo)            
################################
    print("\nCliquez sur l'identifiant de la photo qui sera comparée à toute votre base de donnée : ")
####################################
def Reconnaissance_Faciale(Photo_Compar_Base):   
    Name_local_baz=Lieu+"/Base_de_Donnees/Baz_Analyz_Photos.pickle"
    pickle_in=open(Name_local_baz,"rb")
    Baz_Donnees_Photos_lu=pickle.load(pickle_in)
    pickle_in.close()
    long_Baz_Donnees_Photos_lu=len(Baz_Donnees_Photos_lu)
    print()
    print("Dans Reconn : Baz_Donnees_Photos_lu = ",Baz_Donnees_Photos_lu)
    Liste_Photos = [" _ "]
    for tt in range(long_Baz_Donnees_Photos_lu):
        if Baz_Donnees_Photos_lu[tt][0] == Photo_Compar_Base:
            numer = tt + 1
    print("Dans Reconn : numer = ",numer)
    if int(numer) == 0:
        rien = 1
    else:
        try:
            numer=int(numer)
            if numer<1 or numer>(long_Baz_Donnees_Photos_lu):
                print("Désolé, ce N° de photo n'appartient pas à la base de données")
            else:
                matricule_comparaison=Baz_Donnees_Photos_lu[numer-1][1]
                matricule_comparaison_vert=Baz_Donnees_Photos_lu[numer-1][5]
##############################################################################################################################################################
##############################################################################################################################################################
                list8=[]
                for uu in range(long_Baz_Donnees_Photos_lu):
                    if numer-1==uu:
                        z=1
                    else:
                        list7=[]
                        matricule_BaseDonnée=Baz_Donnees_Photos_lu[uu][1]
                        long_matricule_BaseDonnée=len(matricule_BaseDonnée)
                        long_matricule_comparaison=len(matricule_comparaison)
                        avance2=0
                        aa=0
                        while aa!=long_matricule_comparaison:
                            while avance2!=long_matricule_BaseDonnée:
                                rapp1=matricule_comparaison[aa]/matricule_BaseDonnée[avance2]
                                if rapp1>0.999 and rapp1<1.001:
                                    list7.append(matricule_comparaison[aa])
                                    del matricule_BaseDonnée[avance2]
                                    long_matricule_BaseDonnée=len(matricule_BaseDonnée)
                                    avance2=long_matricule_BaseDonnée
                                else:
                                    avance2+=1
                            avance2=0
                            aa+=1
                        long_list7=len(list7)
                        somme=Baz_Donnees_Photos_lu[numer-1][3]*(sum(list7))
                        recouvr=round((somme/Baz_Donnees_Photos_lu[numer-1][4])*100,1)
                        listoc=[recouvr,Baz_Donnees_Photos_lu[uu][0],Baz_Donnees_Photos_lu[uu][1],Baz_Donnees_Photos_lu[uu][2]]
                        list8.append(listoc)
                list8.sort(reverse=True)
#############################################################################################################################################################
                list8_vert=[]
                for uu in range(long_Baz_Donnees_Photos_lu):
                    if numer-1==uu:
                        z=1
                    else:
                        list7_vert=[]
                        matricule_BaseDonnée_vert=Baz_Donnees_Photos_lu[uu][5]
                        long_matricule_BaseDonnée_vert=len(matricule_BaseDonnée_vert)
                        long_matricule_comparaison_vert=len(matricule_comparaison_vert)
                        avance2=0
                        aa=0
                        while aa!=long_matricule_comparaison_vert:
                            while avance2!=long_matricule_BaseDonnée_vert:
                                rapp1=matricule_comparaison_vert[aa]/matricule_BaseDonnée_vert[avance2]
                                if rapp1>0.999 and rapp1<1.001:
                                    list7_vert.append(matricule_comparaison_vert[aa])
                                    del matricule_BaseDonnée_vert[avance2]
                                    long_matricule_BaseDonnée_vert=len(matricule_BaseDonnée_vert)
                                    avance2=long_matricule_BaseDonnée_vert
                                else:
                                    avance2+=1
                            avance2=0
                            aa+=1
                        long_list7_vert=len(list7_vert)
                        somme_vert=Baz_Donnees_Photos_lu[numer-1][7]*(sum(list7_vert))
                        recouvr_vert=round((somme_vert/Baz_Donnees_Photos_lu[numer-1][8])*100,1)
                        listoc_vert=[recouvr_vert,Baz_Donnees_Photos_lu[uu][0],Baz_Donnees_Photos_lu[uu][5],Baz_Donnees_Photos_lu[uu][6]]
                        list8_vert.append(listoc_vert)
                list8_vert.sort(reverse=True)
##############################################################################################################################################################
                os.chdir(Lieu+"/Base_de_Donnees")
                print("\n        --> Voici la photo étudiée :")
                print("\n                  Titre : ",Baz_Donnees_Photos_lu[numer-1][0])
                affich_image(Baz_Donnees_Photos_lu[numer-1][2])
                affich_image(Baz_Donnees_Photos_lu[numer-1][6])
                print("\n****************************************************************************************************")
                print("\n****************************************************************************************************")
                print("          ==> Voici les résultats, du plus au moins ressemblant :")
                long_list8=len(list8)
                long_list8_vert=len(list8_vert)
                list9=[]
                for jkl in range(long_list8):
                    ego=0
                    for klm in range(long_list8_vert):
                        if list8[jkl][1]==list8_vert[klm][1]:
                            new_val=list8[jkl][0]+list8_vert[klm][0]
                            listic=[new_val,list8[jkl][1],list8[jkl][2],list8[jkl][3],list8_vert[klm][2],list8_vert[klm][3]]
                            list9.append(listic)
                            ego=1
                        else:
                            if klm==long_list8_vert-1:
                                if ego==0:
                                    listic=[list8[jkl][0],list8[jkl][1],list8[jkl][2],list8[jkl][3]]
                                    list9.append(listic)
                                else:
                                    z=1
                            else:
                                z=1
                for klm in range(long_list8_vert):
                    vu=0
                    for jkl in range(long_list8):
                        if list8_vert[klm][1]!=list8[jkl][1]:
                            if jkl==long_list8-1:
                                if vu==0:
                                    listic=[list8_vert[klm][0],list8_vert[klm][1],list8_vert[klm][2],list8_vert[klm][3]]
                                    list9.append(listic)
                                else:
                                    vu=0
                            else:
                                z=1
                        else:
                            z=1
                            vu=1
#####################################################################################################"
                list9.sort(reverse=True)
                long_list9=len(list9)
                for oo in range(long_list9):
                    print("\n                  **",list9[oo][0],"% de ressemblance : Titre : ",list9[oo][1])
                    affich_image(list9[oo][3])
                    try:
                        affich_image(list9[oo][5])
                    except IndexError:
                        z=1
                    print("\n****************************************************************************************************")
                print("                               --------> Fin de la comparaison avec la base de donnée. Tapez Entrée : ")
        except ValueError:
            print("Désolé, je n'ai pas compris.. ")
######################################################################################################################################################################################
def Input_choix_Gestion(change):
    Choix_gestion = change['new']
    if Choix_gestion == "1":
        Choix_gestion_1()
    elif Choix_gestion == "2":
        Choix_gestion_2()
###################################################################
def Visualiser_Base_de_donnees():
    os.chdir(Lieu)
    affich_image("Logo3.jpg")
    Choix_gestion_1()
###################################################################
def Choix_gestion_1():
    ###########################################""
    try:
        Name_local_baz=Lieu+"/Base_de_Donnees/Baz_Analyz_Photos.pickle"
        pickle_in=open(Name_local_baz,"rb")
        Baz_Donnees_Photos_lu=pickle.load(pickle_in)
        pickle_in.close()
        long_Baz_Donnees_Photos_lu=len(Baz_Donnees_Photos_lu)
        print("long_Baz_Donnees_Photos_lu=",long_Baz_Donnees_Photos_lu)
        print("\n             ==> Voici les photos analysées présentes dans la base de données :")
        for tt in range(long_Baz_Donnees_Photos_lu):
            print("\n                      * N°_",tt+1," :     Titre : ",Baz_Donnees_Photos_lu[tt][0])
            os.chdir(Lieu+"/Base_de_Donnees")
            Name_horizon=Baz_Donnees_Photos_lu[tt][2]
            affich_image(Name_horizon)
            Name_vertical=Baz_Donnees_Photos_lu[tt][6]
            affich_image(Name_vertical)
        os.chdir(Lieu)
    except FileNotFoundError:
        print("   **   Désolé..  La base de donnée est vide pour l'instant.")
################################################################
##############################################################################
def Input_choix_Donnees_Photo_Suprim(change):
    Num_photo_Donnee_suprim = change['new']
    Suprim_Donnee_photo_num(Num_photo_Donnee_suprim)
###################################################################
def Supprimer_element_Base_de_donnees():
    try:
        Name_local_baz=Lieu+"/Base_de_Donnees/Baz_Analyz_Photos.pickle"
        pickle_in=open(Name_local_baz,"rb")
        Baz_Donnees_Photos_lu=pickle.load(pickle_in)
        pickle_in.close()
        print("\n     ==> Vous souhaitez effacer les données de quelle photo ? ")
        print()
        long_Baz_Donnees_Photos_lu=len(Baz_Donnees_Photos_lu)
        List_num = [" _ "]
        for yy in range(long_Baz_Donnees_Photos_lu):
            print("                      * N°_",yy+1," :     Titre : ",Baz_Donnees_Photos_lu[yy][0])
            List_num.append(yy+1)
        print("\n                                                     Cliquer sur le N° de l'analyse de photo que vous souhaitez supprimer : ")
        
        Choix_num_suprim=widgets.RadioButtons(
                    options=List_num,
            value=" _ ",
                    layout={'width': 'max-content'}
                )
        Choix_num_suprim.observe(Input_choix_Donnees_Photo_Suprim,names='value')
        ###########################################
        display(Choix_num_suprim)
    except FileNotFoundError:
        print("   **   Désolé..  Un ou plusieurs fichiers nont pas été trouvé...")       
def Suprim_Donnee_photo_num(Num_photo_Donnee_suprim):
    question = Num_photo_Donnee_suprim
    Name_local_baz=Lieu+"/Base_de_Donnees/Baz_Analyz_Photos.pickle"
    pickle_in=open(Name_local_baz,"rb")
    Baz_Donnees_Photos_lu=pickle.load(pickle_in)
    pickle_in.close()
    long_Baz_Donnees_Photos_lu = len(Baz_Donnees_Photos_lu)
    print("Vous avez demandé à supprimer les données de la photo N°",question," : ",Baz_Donnees_Photos_lu[question-1][0])
    del Baz_Donnees_Photos_lu[question-1]
    try:
        if question<1 or question>long_Baz_Donnees_Photos_lu:
            print("\n Désolé, je n'ai pas compris... ")
        else:
            Name_local_baz = "/drive/Base_de_Donnees/Baz_Analyz_Photos.pickle"
            pickle_out=open(Name_local_baz,"wb+")
            pickle.dump(Baz_Donnees_Photos_lu,pickle_out)
            pickle_out.close()
            print("... ça y est, la donnée a été supprimée.")
    except ValueError:
        print("\n Désolé, je n'ai pas pu supprimer la photo...")
