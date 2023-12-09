from configparser import ConfigParser
import sys

def db_config(filename="../development.ini", section='DB'):
    try:
        parser = ConfigParser()
        parser.read(filename)
        parser.sections()
        db = {}
        if parser.has_section(section):
            parms = parser.items(section)
            for x in parms:
                db[x[0]] = x[1]
        else:
            raise Exception("no section")
        return db
    except Exception as e:
        print(e)
