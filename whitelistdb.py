"""
WhitelistDB
Wrapper around SQLAlchemy+sqllite
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import csv
Base = declarative_base()

class PhoneNumber(Base):
    __tablename__ = 'phone_numbers'
    id = Column(Integer, primary_key=True)
    number = Column(String)
    name = Column(String)
    type = Column(String)
    
    def __init__(self, number, name, type):
        self.number = number
        self.name = name
        self.type = type

    def __repr__(self):
        return "<PhoneNumber('%s', '%s', '%s')>" % (self.number, self.name, self.type)

class WhitelistDB(object):
    def __init__(self, filename='/var/lib/asterisk/agi-bin/whitelist.db'):
        self.filename = filename
        self.engine = create_engine('sqlite:///' + self.filename)
        self.session_factory = sessionmaker(bind=self.engine)
        self.session = self.session_factory()
        Base.metadata.create_all(self.engine)
        
    def addNumber(self, number, name, type):
        new_number = PhoneNumber(number, name, type)
        self.session.add(new_number)
        self.session.commit()

    def count(self, filter_number=None, filter_type="any"):
        results = self.session.query(PhoneNumber)
        if filter_number != None:
            results = results.filter_by(number=filter_number)
        if filter_type != 'any':
            results = results.filter_by(type=filter_type)
        return results.count()
    
    def fetchAll(self):
        return self.session.query(PhoneNumber).all()

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="sqllite db")
    parser.add_option("-s", "--csv", dest="csv_filename", help="add a CSV file of numbers")
    parser.add_option("-a", "--add", dest="adduser", help="add a user")
    parser.add_option("-l", "--list", dest="list", help="list users", action="store_true")
    parser.add_option("-c", "--count", dest="count", help="count users", action="store_true")
    parser.add_option("-t", "--type", dest="type", help="type of number")
    parser.add_option("-n", "--number", dest="number", help="phone number")
    
    (options, args) = parser.parse_args()
    whitelistdb_args = []
    if options.filename:
        whitelistdb_args.append(options.filename)
    whitelist_db = WhitelistDB(*whitelistdb_args)
    
    if options.list:
        results = whitelist_db.fetchAll()
        for result in results:
            print "%s, %s, %s" % (result.number, result.name, result.type)
    elif options.adduser:
        args = options.adduser.split(",")
        whitelist_db.addNumber(*args)
    elif options.csv_filename:
        phone_numbers = csv.reader(open(options.csv_filename))
        for entry in phone_numbers:
            whitelist_db.addNumber(*entry)
    elif options.count:
        count_args = []
        if options.number:
            count_args.append(options.number)
        if options.type:
            count_args.append(options.type)
        print "Count: %s" % (whitelist_db.count(*count_args), )
