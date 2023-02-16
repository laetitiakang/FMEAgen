import pandas as pd
import openpyxl

# In[0] -- Importation des colonnes du fichier Excel dans des listes

data = pd.read_excel(r'C:\Users\Hoover48\Desktop\GIM2\PJT2A\EITM_FBSRiskSimulation\EITM_FBSRiskSimulation\FBSdatabase - Copie.xlsx', sheet_name='FMECA')

#Suppression des lignes duppliquées
filedata = data.drop_duplicates()
print(filedata)

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
    e=0
    cause = List_Causes[e]
    path = []
    func_or_not = True
    ElLeft = len(List_Causes)
    while cause != 'Structure 0' and e!=ElLeft:
        eff=List_Effects[e]
        if eff[:-2] == "Function" and cause[:-2] != 'Function' and func_or_not:
            print(cause,'not function')
            firstfunct=e+1
            path.append(eff)
            path.append(cause)
            ec = e
            while List_Effects[ec]!= cause and ec!=ElLeft:
                ec+=1
            cause=List_Causes[ec]
            path.append(cause)
            e=ec
            func_or_not = False
        elif eff[:-2] == "Function" and cause[:-2] == 'Function' and func_or_not:
            print(cause,'function')
            firstfunct=e+1
            path.append(eff)
            path.append(cause)
            del List_Causes[:firstfunct]
            del List_Effects[:firstfunct]
            return path
            func_or_not = True
            del path[:]
        elif eff == cause and eff[:-2] !='Function' and not func_or_not and e!=ElLeft:
            ec = e
            while List_Effects[ec]!= cause and ec!=NbInfect:
                ec+=1
            eff=List_Effects[ec]
            cause=List_Causes[ec]
            path.append(cause)
            e=ec
        #elif (eff == 'Structure 0' or cause == 'Structure 0') and eff[:-2] !='Function' and not func_or_not and e!=ElLeft:
        #    break
        else:
            e+=1
            if func_or_not :
                eff = List_Effects[e]
                cause = List_Causes[e]
    del List_Causes[:firstfunct]
    del List_Effects[:firstfunct]
    #print(List_Causes)
    #print(List_Effects)
    return path

def findallpath():
    AllPath = []
    lenght = len(List_Effects)
    lenmin = len(List_Effects)-1
    while List_Effects[lenmin][:-2] !='Function' and lenmin >= 0 :
        lenmin -= 1
    lenmin+=1
    while len(List_Causes) >= lenght - lenmin +1 :
        AllPath.append(findpath())
    return AllPath

#In[2] -- Append in the Excel File
foundpath = findallpath()
df = pd.DataFrame(foundpath)
print(df)

#path = "C:\Users\Hoover48\Desktop\GIM2\PJT2A\EITM_FBSRiskSimulation\EITM_FBSRiskSimulation\FBSdatabase - Copie.xlsx"

with pd.ExcelWriter('FMECA.xlsx') as writer:
    df.to_excel(writer, sheet_name='FMECA')



# %%
