import pandas as pd
import openpyxl

# In[0] -- Importation des colonnes du fichier Excel dans des listes

data = pd.read_excel(r'C:\Users\Hoover48\Desktop\GIM2\PJT2A\EITM_FBSRiskSimulation\EITM_FBSRiskSimulation\FBSdatabase - Copie.xlsx', sheet_name='FMECA')

#Suppression des lignes duppliquées
filedata = data.drop_duplicates()
#print(filedata)

#Importation des colonnes dans des listes : Nature et ID
List_CausesN= filedata['Causes nature'].values.tolist()
List_CausesID= filedata['Causes ID'].values.tolist()
List_EffectsN= filedata['Effects nature'].values.tolist()
List_EffectsID= filedata['Effects ID'].values.tolist()

NbInfect = len(List_CausesN)

#Concaténation des listes pour faciliter les recherches et comparaison
List_Causes = []; List_Effects = []
for k in range(NbInfect):
    List_Causes.append(str(List_CausesN[k]) + ' ' + str(List_CausesID[k]))
    List_Effects.append(str(List_EffectsN[k]) + ' ' + str(List_EffectsID[k]))

#Inverser les listes pour partir du plus récemment infecté et remonter à l'origine
List_Causes.reverse()
List_Effects.reverse()

#In[1] -- Recherche des propagations (mode de défaillance)


def findpath():
    """
    Recherche la fonction le plus récemment infectée puis retourne la propagation liée (le "chemin" d'infection) dont la source est une fonction ou une structure"
    """

    ###Initialisation###
    e=0 #compteur à 0 pour balayer la liste dont les éléments causes et effets sont classés par ordre anti-chronologique
    cause = List_Causes[e] #première cause de défaillance
    path = [] #chemin de propagation "path"
    func_or_not = True #True si on cherche une fonction, c'est le cas pour le 1er élément recherché
    ElLeft = len(List_Causes) #nombre d'éléments restants "nb elements left = El Left"

    ###Recherche dans l'historique###
    while cause != 'Structure 0' and e!=ElLeft:
        eff=List_Effects[e] #effets causée par "cause"
        if eff.split()[0] == "Function" and cause.split()[0] != 'Function' and func_or_not: 
            '''effet est une fonction/cause n'est pas une fonction/on cherche une fonction'''
            firstfunct=e+1 #indice de la fonction la plus récemment infectée

            #ajout de l'effet puis de la cause associée (ordre antichronologique)#
            path.append(eff) 
            path.append(cause)

            #recherche des origines de la cause (=dernière fonction infectée)#
            ec = e #on part de l'indice de la fonction infectée

            #on recherche les origines de la cause en réitérant la recherche #
            while List_Effects[ec]!= cause and ec!=ElLeft: #cause devient effet : on recherche la cause de cet effet
                ec+=1

            #ajout de la nouvelle cause dans la liste path (chemin de propagation)
            cause=List_Causes[ec] 
            path.append(cause)
            e=ec
            func_or_not = False #nous ne cherchons plus une fonction : les opérations qui nous intéressent sont ci-dessous

        elif eff.split()[0] == "Function" and cause.split()[0] == 'Function' and func_or_not: 
            '''effet est une fonction & cause est une fonction & on cherche une fonction'''

            firstfunct=e+1
            path.append(eff)
            path.append(cause)
            del List_Causes[:firstfunct]
            del List_Effects[:firstfunct]
            return path
            func_or_not = True
            del path[:]

        elif eff == cause and eff.split()[0] !='Function' and not func_or_not and e!=ElLeft: 
            '''la cause est l'effet d'un autre élément& l'effet n'est une fonction& on ne cherche pas une fonction'''
            ec = e
            while List_Effects[ec]!= cause and ec!=NbInfect:
                ec+=1
            eff=List_Effects[ec]
            cause=List_Causes[ec]
            path.append(cause)
            e=ec

        else: 
            '''la cause n'est pas l'effet d'un autre élément, on passe'''
            e+=1
            if func_or_not :
                eff = List_Effects[e]
                cause = List_Causes[e]
    del List_Causes[:firstfunct]
    del List_Effects[:firstfunct]

    return path

def findallpath():
    """
    Recherche tous les chemins de propagation (find all path)
    """
    AllPath = [] #liste de toutes les propagations de défaillance
    lenght = len(List_Effects) #taille de la liste initiale de l'historique 
    lenmin = len(List_Effects)-1 #taille de liste tronquée finale (indice de la première fonction infectée)
    while List_Effects[lenmin].split()[0] !='Function' and lenmin >= 0 :
        lenmin -= 1
    lenmin+=1
    while len(List_Causes) >= lenght - lenmin +1 :
        AllPath.append(findpath())
    return AllPath


# In[3] -- Mise en forme du tableau

foundpath = findallpath() #liste de toutes les chemins de propagation de défaillance
print(pd.DataFrame(foundpath))

def formatting(foundpath):
    """ 
    Met en forme le tableau en mettant les comportements sur une colonne en fonction de la fonction"
    """
    nblinei = len(foundpath) #nombre de chemins (= nombre de ligne dans le tableau initial)
    nblinef = 0 #nombre de ligne dans le tableau final - à calculer
    for line in range(nblinei):
        '''Calcul du nombre de ligne final = le nombre de behavior dans tout le tableau'''
        nblinef += len(foundpath[line])-2

    for line in range(nblinef):
        '''Mettre les behavior sur chaque ligne'''

        if len(foundpath[line]) > 3:
            addpath = [foundpath[line][0]] #création d'une nouvelle ligne avec comme seul élément qu'est la fonction
            endpath = [foundpath[line][-1]] #liste contenant le dernier élément pour le rajouter
            col = 2 #indice de la colonne du tableau initial
            element = foundpath[line][col] #element se situant dans la ligne line et la colonne col
            nbcol=len(foundpath[line]) #nombre de colonne associée à la ligne line

            while (element.split()[0]!='Function' or element.split()[0]!='Structure') and col<=nbcol-2:
                addpath.append(foundpath[line].pop(col-1)) #ajouter d'un élément behavior
                foundpath = foundpath[:line] + [addpath+endpath] + foundpath[line:] #liste contenant fonction, behavior, cause
                addpath = addpath[:1] #réinitialisation de la liste avec le seul élément qu'est la fonction
                nbcol = len(foundpath[line]) #nombre d'élément associée à la ligne line
            nbline = len(foundpath)
    return foundpath

foundpath = formatting(foundpath) #tableau formatté
print(foundpath)

#In[4] -- Append in the Excel File



df = pd.DataFrame(foundpath) #mise en forme du tableau
dataexport = df.drop_duplicates() #suppression des éléments dupliqués
print(dataexport)

#path = "C:\Users\Hoover48\Desktop\GIM2\PJT2A\EITM_FBSRiskSimulation\EITM_FBSRiskSimulation\FBSdatabase - Copie.xlsx"

with pd.ExcelWriter('FMECA.xlsx') as writer:
    '''exportation du tableau dans un tableur Excel'''
    dataexport.to_excel(writer, sheet_name='FMECA')