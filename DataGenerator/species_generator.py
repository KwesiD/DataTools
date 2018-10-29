import sys
import string
from random import randint,choice
"""
Generates a list of random species with optional noise
"""
charlist = string.ascii_letters

"""
Adds noise (a few errant characters) to species name
"""
def noise(s):
	for i in range(len(s)):
		if(s[i] == " "): #skip whitespace
			continue
		if(randint(0,100) > 92): #arbitrary number 92
			s = s[:i] +  choice(charlist) + s[i + 1:]
	return s


if __name__ == '__main__': #if we are running this from command line
	if(len(sys.argv) == 1):
		raise Exception("Please enter number of species to generate")

	count = int(sys.argv[1])

	hasNoise = False
	if("-n" in sys.argv):
		hasNoise = True


species_file = open("../DataFiles/species_list.csv").readlines()
species_list = []
for i in range(len(species_file)):
	if(i == 0):
		continue #skip genus species line
	else:
		species_list.append(species_file[i].strip().replace(","," "))

"""
Generate list of "count" species. 
"""
def generate_species(count,hasNoise):	
	generated_list = []

	for i in range(count):
		curr = species_list[randint(0,len(species_list)-1)]
		if(hasNoise):
			curr = noise(curr)
		generated_list.append(curr)
	return generated_list

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
