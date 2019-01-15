import re
"""
data from https://www.uniprot.org/docs/speclist
Takes species.txt file and extracts all valid (Genus species format) names under the scientific name (N) category
Creates a csv file from this info 
"""
species_text = open("../DataFiles/bacterial_taxonomy.tsv","r").read() 
species_list = re.findall(r"s__[A-Z][a-z]+ [a-z]+",species_text)
for i in range(len(species_list)):
	species_list[i] = species_list[i].strip().replace("s__","").replace(" ",",")

species_list = set(species_list) #remove duplicates
output_table = open("../DataFiles/species_list.csv","w")
output_table.write("Genus,Species\n") #column headers
for species in species_list:
	output_table.write(species + "\n")
output_table.write("Clostridium,difficile\n") #why this is not in the list? I have no idea
output_table.close()
