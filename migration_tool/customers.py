# -*- coding: utf-8 -*-

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import *
import xmlrpclib


#Conexion Mysql
mysql_dbname = 'autotech_osc'
mysql_dbuser = 'root'
mysql_dbpass = 'root'
mysql_dbhost = 'localhost'

# Conexion Odoo
odoo_dbuser = "admin"
odoo_dbpass = "7Twiljebrath"
odoo_dbname = "autotech_backup01"
odoo_dbhost = 'localhost'

def connect_mysql(dbuser, dbpass, dbhost, dbname):
    Base = automap_base()
    engine = create_engine('mysql://'+dbuser+':'+dbpass+'@'+dbhost+'/'+dbname)
    Base.prepare(engine, reflect=True)

    return Base, engine

def connect_odoo(dbhost, dbname, dbuser, dbpass):
    sock_common = xmlrpclib.ServerProxy ('http://'+dbhost+':8069/xmlrpc/common')
    uid = sock_common.login(dbname, dbuser, dbpass)

    sock = xmlrpclib.ServerProxy('http://'+dbhost+':8069/xmlrpc/object')

    return sock, uid

def create_customer(dbname, dbpass, uid, sock, customer):

    #customer.update({'supplier' : False, 'customer' : True})

    customer_id = sock.execute(dbname, uid, dbpass, 'res.partner', 'create', customer)
    print "customer %s created" % str(customer['name'])

def get_customers(Base, engine, uid, sock):
    customers = [] 

    # Schemas de la tablas
    customers_table = Base.classes.customers
    address_book_table = Base.classes.address_book
    products_attributes_table =  Base.classes.products_attributes

    
    session = Session(engine)

    customers_query = session.query(customers_table, address_book_table). \
                      filter(customers_table.customers_id == address_book_table.customers_id). \
                      all()
    for item in customers_query:
        parent = {
            'name' : item.address_book.entry_company,
            'is_company' : True,
        }
        partner = {
            'name': item.customers.customers_firstname.title() + " " + item.customers.customers_lastname.title(),
            'street': item.address_book.entry_street_address.upper(),
            'type' : 'default',
            #'parent_id': , 
            'customer' : 'True',
            'supplier' : 'False',
            #'is_company': item.address_book.entry_company,
            'zip': item.address_book.entry_postcode,
            'city': item.address_book.entry_city.upper(),
            'email': item.customers.customers_email_address,
            'phone': item.customers.customers_telephone,
            'fax': item.customers.customers_fax,
            'active': True,
        }
        customers.append(partner)
        create_customer(odoo_dbname, odoo_dbpass, uid, sock, partner)

    #print customers

def main():
    (Base, engine) = connect_mysql(mysql_dbuser, mysql_dbpass, mysql_dbhost, mysql_dbname)
    (sock, uid) = connect_odoo(odoo_dbhost, odoo_dbname, odoo_dbuser, odoo_dbpass)
    get_customers(Base, engine, uid, sock)

main()

#    args = [('id', '=', '6'),]
#    ids = sock.execute(dbname, uid, pwd, 'res.partner', 'search', args)
#
#    partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'write', ids, partner)

