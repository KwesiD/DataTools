from random import randint,choice
import sys

"""
python name_generator.py [name_count] [name_format] [output file name](optional)
Generates a list of "name_count" names in the format "name_format"
"""

standard_formats = ["f l","fi l","f m l","f mi l","l, f","l, fi","l, f mi","l, fi mi"]#the built in formats

def read_into_list(file):
	arr = []
	for line in file:
		if(line.strip() != ""):
			arr.append(line.strip().replace(" ",""))
	return arr

def load_names():
	first_names = read_into_list(open("../DataFiles/first-names.txt","r"))
	middle_names = read_into_list(open("../DataFiles/middle-names.txt","r"))
	last_names = read_into_list(open("../DataFiles/last-names.txt","r"))
	return first_names,middle_names,last_names

"""
f = firstname
l = lastname
m = middle name
Append "i" to make an initial
mix = choose a random combination of formats

Possible Formats:
f l = Firstname Lastname
fi l = F Lastname
f m l = Firstname Middlename Lastname
f mi l = Firstname M Lastname
l, f = Lastnam, Firstname
l, fi = Lastname, F
l, f mi = Lastname, Firstname M
l, fi mi = Lastname, F M
"""
def generate_names(num,name_format):
	name_list = []
	formats = standard_formats
	is_mix = True if name_format == "mix" else False
	for i in range(num):
		if is_mix:
			name_format = formats[randint(0,len(formats)-1)] #
		name = ""
		if(name_format == "f l"):
			name = generate_name("first") + " " + generate_name("last")
		elif(name_format == "fi l"):
			name = generate_name("first")[0] + " " + generate_name("last")
		elif(name_format == "f m l"):
			name = generate_name("first") + " " + generate_name("middle") + " " + generate_name("last")
		elif(name_format == "f mi l"):
			name = generate_name("first") + " " + generate_name("middle")[0] + " " + generate_name("last")
		elif(name_format == "l, f"):
			name = generate_name("last") + ", " + generate_name("first")
		elif(name_format == "l, fi"):
			name = generate_name("last") + ", " + generate_name("first")[0]
		elif(name_format == "l, f mi"):
			name = generate_name("last") + ", " + generate_name("first") + " " + generate_name("middle")[0]
		elif(name_format == "l, fi mi"):
			name = generate_name("last") + ", " + generate_name("first")[0] + " " + generate_name("middle")[0]
		else:
			raise Exception("Invalid Name Format " + name_format)
		name_list.append(name)
	return name_list



def generate_name(type):
	if(type == "first"):
		return first_names[randint(0,len(first_names)-1)]
	if(type == "middle"):
		return middle_names[randint(0,len(middle_names)-1)]	
	if(type == "last"):
		return last_names[randint(0,len(last_names)-1)]


"""
Converts name from informat to outformat
"""
def convert_name(inname,informat,outformat):
	if(outformat == "mix"):
		outformat = choice(standard_formats)
	informat = informat.split()
	outformat = outformat.split()
	for c in informat+outformat:
		if((len(c) > 2) or (len(c) == 2 and (c[0] not in ["f","m","l"] or c[1] not in ["i",","]))): #token length greater than 2 or token is not (f,m, or l) + (i or ",") 
			raise Exception("Invalid format token: " + c)
	inname = inname.split()
	outname = []
	first,middle,last = "","",""
	for ftoken,ntoken in zip(informat,inname): #format token and name token
		if("f" in ftoken):
			first = ntoken
		if("m" in ftoken):
			middle = ntoken
		if("l" in ftoken):
			last = ntoken
	for token in outformat: #format token and name token
		curr = "" #current token
		if("f" in token):
			curr = first
		if("m" in token):
			curr = middle
		if("l" in token):
			curr = last
		if("i" in token):
			curr = curr[0]
		if("," in token):
			curr += ","
		outname.append(curr)
	outname = " ".join(outname)
	return outname



first_names,middle_names,last_names = load_names()

if __name__ == '__main__': #if this is run as a script
	if(len(sys.argv) < 3):
		raise Exception("Enter number of names to produce and the name format")
	name_count = int(sys.argv[1])
	name_format = sys.argv[2]
	names = generate_names(name_count,name_format)
	if(len(sys.argv) > 3):
		output = open(sys.argv[3],'w')
		for name in names:
			output.write(name + "\n")
		output.close()
	else:
		print(names)
#else, we are importing it