import sys
import string
from random import randint,choice
from nltk import edit_distance
"""
Generates a list of random species with optional noise
"""
charlist = string.ascii_letters
species_file = open("../DataFiles/species_list.csv").readlines()
species_list = []
species_short_names = []
species_dict = {}
"""
Adds noise (a few errant characters) to species name
"""
def noise(s):
	for i in range(len(s)):
		if(s[i] == " " or s[i] == "."): #skip whitespace and period
			continue
		if(randint(0,100) > 92): #arbitrary number 92
			s = s[:i] +  choice(charlist) + s[i + 1:]
	return s

"""
Gets the short name of a species (such as E. coli)
"""
def get_short_name(species):
	t1,t2 = species.split()
	t1 = t1[0].capitalize() + "."
	t2 = t2.lower()
	return t1 + " " + t2

"""
Places species in the correct format (Genus species, not Genus Species or genus species)
"""
def correct_format(species):
	if(any(s in species for s in ["MRSA","MSSA","mrsa","mssa"])):
		species = "Staphylococcus aureus"
	if(any(s in species.lower() for s in ["cdif","cdiff","c.dif","c.diff","c dif","c diff","c. dif","c. diff"])):
		species = "Clostridium difficile"
	if(species == None or species.strip() == ""):
		return ""
	t1,t2 = species.split()
	t1 = t1.capitalize()
	t2 = t2.lower()
	if("." not in t1 and len(t1) == 1):
		t1 += "."
	return t1 + " " + t2


def search_species(term,fullName=False):
	temp = term
	try:
		term = correct_format(term)
	except ValueError:
		print("-"*5,"Error in",temp,"-"*5)
		return ""
	# if(term == None):
	# 	print("-"*5,"Error in",temp,"-"*5)
	# 	return ""
	if(term in species_list):
		if("." in term and fullName):
			term = convert_format(term)
		return term
	elif(term in species_short_names):
		if("." in term and fullName):
			term = convert_format(term)
		return term
	else:
		term = search_by_distance(term)
		if("." in term and fullName):
			term = convert_format(term)
		return term

def search_by_distance(term):
	curr_genus = None
	curr_species = None
	curr_dist = sys.maxsize
	g,s = term.split()
	genus_list = list(species_dict.keys())#species_short_names if "." in term else species_list #if term is a short name, use short_names, else use regular list
	for genus in genus_list:
		dist = edit_distance(g,genus)
		if(dist < curr_dist):
			curr_dist = dist
			curr_genus = genus

	curr_dist = sys.maxsize
	for species in species_dict[curr_genus]:
		dist = edit_distance(s,species)
		if(dist < curr_dist):
			curr_dist = dist
			curr_species = species

	# for species in working_list:
	# 	dist = edit_distance(term,species)
	# 	if(dist < curr_dist):
	# 		curr_dist = dist
	# 		curr_species = species
	return curr_genus + " " + curr_species


def convert_format(term):
	term = search_species(term)
	if("." in term):
		return species_list[species_short_names.index(term)]
	else:
		return get_short_name(term)
"""
Generate list of "count" species. 
"""
def generate_species(count,hasNoise):	
	generated_list = []

	for i in range(count):
		curr = species_list[randint(0,len(species_list)-1)]
		curr = curr if randint(0,100) < 92 else get_short_name(curr)
		if(hasNoise):
			curr = noise(curr)
		generated_list.append(curr)
	generated_list.sort() #sort the list
	return generated_list

if __name__ == '__main__': #if we are running this from command line
	if(len(sys.argv) == 1):
		raise Exception("Please enter number of species to generate")

	count = int(sys.argv[1])

	hasNoise = False
	if("-n" in sys.argv):
		hasNoise = True

for i in range(len(species_file)):
	if(i == 0):
		continue #skip genus species line
	else:
		species_list.append(species_file[i].strip().replace(","," "))

for species in species_list:
	species_short_names.append(get_short_name(species))

for name in species_short_names + species_list:
	genus,species = name.split()
	if(genus not in species_dict):
		species_dict[genus] = []
	species_dict[genus].append(species)



if __name__ == '__main__':
	generated_list = generate_species(count,hasNoise)
	if("-o" in sys.argv):
		output_file = "generated_species_names"
		if(hasNoise):
			output_file += "_noise"
		output = open(output_file + ".csv","w")
		output.write("Genus,Species\n")
		for species in generated_list:
			output.write(species.replace(" ",",") + "\n")
		output.close()
	else:
		print(generated_list)

