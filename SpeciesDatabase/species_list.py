import re
"""
data from https://www.uniprot.org/docs/speclist
Takes species.txt file and extracts all valid (Genus species format) names under the scientific name (N) category
Creates a csv file from this info 
"""
species_text = open("../DataFiles/species.txt","r").read()
species_list = re.findall(r"N=[A-Z][a-z]+ [a-z]+\n",species_text)
for i in range(len(species_list)):
	species_list[i] = species_list[i].strip().replace("N=","").replace(" ",",")

species_list = set(species_list) #remove duplicates
output_table = open("../DataFiles/species_list.csv","w")
output_table.write("Genus,Species\n") #column headers
for species in species_list:
	output_table.write(species + "\n")
output_table.close()
