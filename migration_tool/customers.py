# -*- coding: utf-8 -*-

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import *
import xmlrpclib

Base = automap_base()

#Conexion
engine = create_engine('mysql://root:root@localhost/autotech_osc')

Base.prepare(engine, reflect=True)

#Schemas de la tablas
customers = Base.classes.customers
address_book = Base.classes.address_book

#De aqui saco el id para la categoria
products_attributes =  Base.classes.products_attributes


session = Session(engine)

for ins in session.query(customers, address_book). \
                   filter(customers.customers_id == address_book.customers_id). \
                   limit(1):

    partner = {
        'name': ins.customers.customers_firstname + " " + ins.customers.customers_lastname,
        'street': ins.address_book.entry_street_address,
        'type' : 'default',
        '': ins.address_book.entry_company,
        'is_company': ins.address_book.entry_company,
        'zip': ins.address_book.entry_postcode,
        'city': ins.address_book.entry_city,
        'email': ins.customers.customers_email_address,
        'phone': ins.customers.customers_telephone,
        'fax': ins.customers.customers_fax,
        'active': True,
    }
    print ins.customers.customers_id, \
          ins.customers.customers_id, \
          ins.customers.customers_gender, \
          ins.customers.customers_firstname, \
          ins.customers.customers_lastname, \
          ins.customers.customers_dob, \
          ins.customers.customers_email_address, \
          ins.customers.customers_default_address_id , \
          ins.customers.customers_telephone, \
          ins.customers.customers_fax, \
          ins.customers.customers_password, \
          ins.customers.customers_newsletter, \
          ins.customers.member_level, \
          ins.customers.is_license, \
          ins.customers.license_number, \
          ins.address_book.entry_company, \
          ins.address_book.entry_gender, \
          ins.address_book.entry_firstname, \
          ins.address_book.entry_lastname, \
          ins.address_book.entry_street_address, \
          ins.address_book.entry_suburb, \
          ins.address_book.entry_postcode, \
          ins.address_book.entry_city, \
          ins.address_book.entry_state, \
          ins.address_book.entry_country_id, \
          ins.address_book.entry_zone_id 

username = "admin"
pwd = "123"
dbname = "autotech-website"

sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)

sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

args = [('id', '=', '6'),]
ids = sock.execute(dbname, uid, pwd, 'res.partner', 'search', args)

partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'write', ids, partner)

