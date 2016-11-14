from config import allowed_quotes
from config import delimiter
# This function reads a line and based on the delimiter and allowed quotes it will handle appropriate escaping of char between valid delimiters
def get_formatted_row(row):
    class DynamicReader:
        def __init__(self):
            self.output = []
            self.str = ''
            self.last_char = None
            self.current_char = None
            self.is_inquotes = False
            self.validquotes = allowed_quotes

        def is_new_entry(self):
            if self.is_inquotes:
                return False
            elif self.current_char ==delimiter:
                return True
            else:
                return False

        # simple switch like iterator that
        def quoteprocess(self):
            if self.current_char in self.validquotes and self.last_char == delimiter:
                self.is_inquotes = True
            elif self.current_char in self.validquotes and self.last_char == "\\":
                # ignore this one
                pass
            elif self.current_char in self.validquotes and self.is_inquotes == True:
                self.is_inquotes = False


        def append_entry(self):
            self.output.append(self.str)
            self.str = ''


        def read(self,char):
            self.last_char =self.current_char
            self.current_char = char
            # Constantly checks wether we are in a quote bracket or not
            self.quoteprocess()
            # if we are at a new entry i.e. space lets store the current str otherwise continue to build the current str
            if self.is_new_entry():
                self.output.append(self.str)
                self.str = ''
            else:
                self.str += self.current_char

        def finish(self):
            self.output.append(self.str)

    r = DynamicReader()
    for item in row:
        r.read(item)
    r.finish()
    return r.output