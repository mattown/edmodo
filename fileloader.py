import sys, os
from CustomRowParser import get_formatted_row
from config import allowed_quotes
from config import delimiter
#
#
#   Pass this fileloader an absolute filepath and it will create a Hashmap of our values, stored as a list in memory
#
#   It will validate the model which assumes we have 5 rows with the type
#       ID date-time string1 string2 string3
#
#       Delimiter is space, and to quote strings with space we encapsulate them in before and after curly quotes “ ”, but we can tweak these in the config.py
#
#
#   It will then prompt the user to enter in valid IDs to list the values of st2 in the order they are in the file
#
#
#
#






#
#
# Main Method
#
#

def main():

    # Memory object
    mem_obj = {}


    # make sure the filepath works
    try:
        assert os.path.exists(sys.argv[1])
    except:
        print("Enter in a valid Path to a file")
        print("E.G. python3 fileloader.py <full-absolute-path-to-file>")
        sys.exit(1)
    filepath = sys.argv[1]
    file = open(filepath, 'r')


    # Read and process the file into memory
    print("Attempting to Load file %s...." % filepath )
    bad_num_rows = 0
    for row in file:
        bad_num_rows += process_row(mem_obj, row)
    print("File loaded to memory!!\n")
    print("Ignored %i Rows due to Errors" % bad_num_rows)
    file.close()


    # Begin User prompt
    current_response = ''
    while 'quit' not in current_response:
        if current_response:
            ids = current_response.split(',')
            for id in ids:
                id = id.strip()
                if id.isdigit(): ## remember this is true for only non negative integers
                    get_entry(mem_obj,int(id))
                elif id =='':
                    print("ERROR:   Entry is Blank!! must be a non-negative Integer")
                else:
                    print("ERROR:   Invalid entry for %s must be a non-negative Integer" % id)

        current_response = input("\nPlease enter IDs comma seperated:    ")
        current_response = current_response.strip().lower()









#
#
# Processing row functions
#
#


# check to make sure we have a 5 row object with int as 1, date-time 2 and
def is_valid_row(parsed_row):

    if len(parsed_row) != 5:
        return False
    else:
        id = parsed_row[0]
        if id.isdigit(): # this also is invalid if its a negative number
            return True
    return False

# returns 0 if no errors on row, returns 1 if error
def process_row(mem_obj, row):

    parsed_row = parse_row(row)

    if is_valid_row(parsed_row):
        add_entry(mem_obj, parsed_row)
        return 0
    else:
        return 1

# this reads the rows, valid
def parse_row(row):

    #first check if there are curly braces or quotes, if not then lets just try to split it on spaces

    quotes_in_row = False
    for item in allowed_quotes:
        if item in row:
            quotes_in_row = True

    if quotes_in_row:
        split_row = get_formatted_row(row)
    else:
        split_row = row.split(delimiter)

    return split_row













#
#
# Memory Object functions
#
#





# this adds the values we want to the memory lookup object
def add_entry(mem_obj, row):
    id, stored_str = int(row[0]), row[3]
    if id in mem_obj.keys():
        mem_obj[id].append(stored_str)
    else:
        mem_obj[id] = [stored_str]
# this prints the values of a given ID to the screen
def get_entry(mem_obj, id):
    try:
        data =mem_obj[id]
        for item in data:
            print('%s %s' % (id, item))
    except:
        print("ERROR:   id %s does not exist" % id)







if __name__ == "__main__":
    main()