import sys
import pandas as pd
sys.path.append('../DataGenerator')
import name_generator
import species_generator
import re

#sys.argv = ["","../DataGenerator/sample_patients.xlsx","./mod_patients.xlsx","-n","IPCStaff","-p","Pathogen"]
"""
args should be in this format
path/to/input/table path/to/output/table (-n|-name NameOfColumnWithNames)|(-p|-pathogen NameOfColumnWithPathogen)
example:
../DataGenerator/sample_patients.xlsx ./mod_patients.xlsx -n IPCStaff -p Pathogen]
"""

# In[ ]:

def clean_names(column):
    for i in range(len(column)):
        fraction = int((i/len(column)*100))
        if(fraction%5 == 0):
            print(str(fraction) + "%","names completed")
        temp = column.loc[i]
        names = find_names(column.loc[i])
        #print(column.loc[i],"<")
        for j in range(len(names)):
            curr = re.sub(r"Dr[.]? ","",names[j])
            #currformat = name_generator.detect_format(curr)
            names[j] = name_generator.convert_name(curr,"l, f m")
         #   print(column.loc[i],"<2")
        column.loc[i] = ";".join(names)#find_names(column.loc[i])
        #print(temp,"->",column.loc[i])
    print("names complete")
    return column

def find_names(names):
    names1 = re.findall(r"[a-zA-Z]+[.]?, ?(?:[a-zA-Z]+[.]? ?)+",names)
    for name in names1:
        names = names.replace(name,"")
    names2 = re.findall(r"[a-zA-Z]+[.]? (?:(?:[a-zA-Z]+[.]? )+)?[a-zA-Z]+[.]?",names)
    name_list = names1+names2
    return name_list


def search_species(string):
    newString = []
    for species in re.findall(r"[a-zA-Z]+. ?[a-zA-Z]+",string):
        newString.append(species_generator.search_species(species))
    return ";".join(newString)
      
def clean_pathogens(column):
    for i in range(len(column)):
        fraction = int((i/len(column)*100))
        if(fraction%5 == 0):
            print(str(fraction) + "%","pathogens completed")
        temp = column.loc[i]
        column.loc[i] = search_species(column.loc[i]) #local search species
        #print(temp,"->",column.loc[i])
    print("pathogens complete")
    return column
        
        
modes = [] #which modes we want for each column
columns = [] #which column we are cleaning
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
    print(mode)
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