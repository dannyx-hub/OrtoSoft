from configparser import ConfigParser
import os
import traceback

# os.chdir("../")

def db_config(filename="development.ini", section='database'):
    try:
        parser = ConfigParser()
        parser.read(filename)
        print(parser[section]['host'])
        db = {}
        if parser.has_section(section):
            parms = parser.items(section)
            for x in parms:
                db[x[0]] = x[1]
        else:
            raise Exception("no section")
        return db
    except Exception as e:
        print(traceback.format_exc(10))

def app_config(filename="development.ini", section="app"):
    try:
        parser = ConfigParser()
        parser.read(filename)
        app = {}
        if parser.has_section(section):
            parms = parser.items(section)
            for x in parms:
                app[x[0]] = x[1]
        else:
            raise Exception("no section")
        return app
    except Exception as e:
        print(traceback.format_exc(10))



print(db_config())