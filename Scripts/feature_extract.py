import argparse

# Converts one byte to int
def myInt (b):
    return int.from_bytes(b, byteorder='little')


# Converts two bytes to int
def two_byte_hex (f):
    return myInt(f.read(1)) << 8 | myInt(f.read(1))


# Converts four bytes to int
def four_byte_hex (f):
    return two_byte_hex(f) << 16 | two_byte_hex(f)


# Get a list of instruction codes from a Code attribute
def get_instr (f, ConstantPool):
    # skip the attribute length/ max stack/ max locals
    f.read(8)
    
    # get code length
    code_length = four_byte_hex(f)
    # get the code
    code = [myInt(f.read(1)) for x in range(code_length)]
    
    # get exception table length
    exception_table_length = two_byte_hex(f)
    # skip the exception table
    f.read(exception_table_length * 8)
    
    # get attributes count
    attributes_count = two_byte_hex(f)
    for _ in range(attributes_count):
        # 2 bytes attribute name index
        attribute_name_index = two_byte_hex(f)

        # 4 bytes attribute_length
        attribute_length = four_byte_hex(f)

        f.read(attribute_length)
        
    return code

def extract_instructions (f):
	insns = []
	# Open class file as f
	with open(f, "rb") as f:
	    
	    # All java class files start with cafe babe so the first two tokens should be ignored.
	    # The next 4 bytes comprise the version of Java
	    # Ignore the first 4 tokens
	    f.read(8)
	    
	    # Skipping through the constant pool
	    # Get the size of the constant pool which is the next two bytes
	    CPoolSize = two_byte_hex(f)
	    
	    ConstantPool = {}
	    
	    
	    for x in range(CPoolSize - 1):
	        typ = myInt(f.read(1))

	        # utf8 : next 2 bytes are the length of the string
	        if typ == 1:
	            l = two_byte_hex(f)
	            ConstantPool[x+1] = f.read(l)
	            
	        # Class : next 2 bytes location of Class Name
	        elif typ == 7:
	            f.read(2)
	            
	        # String: next 2 bytes location of String
	        elif typ == 8:
	            f.read(2)
	        
	        # Field Refference : 2 bytes location of Class, 2 bytes location of NameAndType
	        elif typ == 9:
	            f.read(4)
	        
	        # Method Refference : 2 bytes location of Class, 2 bytes location of NameAndType
	        elif typ == 0xa:
	            f.read(4)
	        
	        # Name and Type : 2 bytes location of utf8, 2 bytes location of utf8
	        elif typ == 0xc:
	            f.read(4)
	            
	            
	    # The 2 bytes after the constant table are the access flags
	    access_flags = two_byte_hex(f)
	    
	    # The next 2 bytes are the location of this class in the constant table
	    f.read(2)
	    
	    # The next 2 bytes are the locaiton of this class's super class in the constant table
	    f.read(2)
	    
	    # The next 2 bytes are the number of interfaces this class implements
	    interfaces_count = two_byte_hex(f)
	    
	    # 2 byte location for each interface in the constant table
	    f.read(interfaces_count * 2)
	    
	    # The next 2 bytes are the number of fields this class has
	    fields_count = two_byte_hex(f)
	    
	    for _ in range(fields_count):
	        access_flags = two_byte_hex(f)
	        
	        name_index = two_byte_hex(f)
	        
	        descriptor_index = two_byte_hex(f)
	        
	        attributes_count = two_byte_hex(f)
	        
	        for _ in range(attribute_count):
	        # START SPECIFIC ATTRIBUTE (WILL NEED LOOP HERE)

	            # 2 bytes attribute name index
	            attribute_name_index = two_byte_hex(f)

	            # 4 bytes attribute_length
	            attribute_length = four_byte_hex(f)

	            f.read(attribute_length)
	        
	    #The next 2 bytes are the number of methods this class has
	    methods_count = two_byte_hex(f)
	    
	    for _ in range(methods_count):
	        # 2 bytes access flags
	        access_flags = two_byte_hex(f)

	        # 2 bytes location of method name in constant table
	        name_index = two_byte_hex(f)

	        # 2 bytes location of _ in constant table
	        descriptor_index = two_byte_hex(f)

	        # 2 bytes number of attributes in this method
	        attribute_count = two_byte_hex(f)

	        for _ in range(attribute_count):
	        # START SPECIFIC ATTRIBUTE (WILL NEED LOOP HERE)

	            # 2 bytes attribute name index
	            attribute_name_index = two_byte_hex(f)

	            if ConstantPool[attribute_name_index].decode("utf-8") == 'Code':
	                # Extract the instructions
	                insns += [get_instr(f, ConstantPool)]
	                
	            else:
	                # Skip this attribute
	                # 4 bytes attribute_length
	                attribute_length = four_byte_hex(f)

	                f.read(attribute_length)
	            
	    # 2 bytes number of attributes in this method
	    attribute_count = two_byte_hex(f)

	    for _ in range(attribute_count):
	    # START SPECIFIC ATTRIBUTE (WILL NEED LOOP HERE)

	        # 2 bytes attribute name index
	        attribute_name_index = two_byte_hex(f)
	        
	        # 4 bytes attribute_length
	        attribute_length = four_byte_hex(f)
	        
	        f.read(attribute_length)	    
	return insns

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("f", help = "The .class file to extract features from", type = str)

	args = parser.parse_args()
	f = args.f
	methods = extract_instructions(f)

	with open("/".join(f.split("/")[:-1] + ["code.csv"]), "w+") as f:
		for method in methods:
			f.write(", ".join(str(x) for x in method))
			f.write("\n")

		f.close()









