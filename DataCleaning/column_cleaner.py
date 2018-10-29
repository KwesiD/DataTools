#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
import pandas as pd
sys.path.append('../DataGenerator')
import name_generator
import species_generator
sys.argv = ["","../DataGenerator/sample_patients.xlsx","./mod_patients.xlsx","-p","Pathogen"]


# In[ ]:


def search_species(string):
    newString = []
    for species in string.split(";"):
        newString.append(species_generator.search_species(species))
    return ";".join(newString)
      
def clean_pathogens(column):
    for i in range(len(column)):
        temp = column.loc[i]
        column.loc[i] = search_species(column.loc[i]) #local search species
        print(temp,"->",column.loc[i])
    return column
        
        
    


# In[ ]:


#
modes = []
columns = []
for i in range(len(sys.argv)):
    if(i == 0): #skip program name
        continue
    if(i == 1): #get infile name
        datafile = sys.argv[i]
        continue
    if(i == 2): #get outfile name
        outfile = sys.argv[i]
        continue
    if(sys.argv[i] in ["-p","-pathogen"] and sys.argv[i+1]):
        modes.append("pathogen")
        columns.append(sys.argv[i+1])
        i += 1
        continue
    if(sys.argv[i] in ["-n","-name"] and sys.argv[i+1]):
        modes.append("name")
        columns.append(sys.argv[i+1])
        i += 1
        continue

fileformat = datafile.split(".")[-1]
if(fileformat == "csv"):
    df = pd.read_csv(datafile)
elif(fileformat in ["xls","xlsx"]):
    df = pd.read_excel(datafile)

for mode,column in zip(modes,columns):
    if(mode == "pathogen"):
        df[column] = clean_pathogens(df[column])
    if(mode == "name"):
        df[column] = clean_names(df[column])


newfileformat = outfile.split(".")[-1]
if(newfileformat == "csv"):
    df.to_csv(outfile)
elif(newfileformat in ["xls","xlsx"]):
    writer = pd.ExcelWriter(outfile)
    df.to_excel(writer,"Sheet1")
    writer.save()