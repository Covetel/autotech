# *-* coding=utf-8 *-*
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import xmlrpclib, pprint

mysql_dbuser = 'root'
mysql_dbpass = '123321...'
mysql_dbname = 'autotech'
mysql_dbhost = 'localhost'

odoo_dbuser = 'admin'
odoo_dbpass = '123321...'
odoo_dbname = 'autotech'
odoo_dbhost = 'localhost'

def get_product_categ_id(sock, uid, dbname, dbpass, product_categ_name):

    filt = [('name','=', product_categ_name)]

    categ_id = sock.execute(dbname, uid, dbpass, 'product.public.category', 'search', filt)

    return categ_id

def create_autotech_products(dbuser, dbpass, dbname, dbhost, product):
    # Get the uid
    sock_common = xmlrpclib.ServerProxy ('http://'+dbhost+':8069/xmlrpc/common')
    uid = sock_common.login(dbname, dbuser, dbpass)

    sock = xmlrpclib.ServerProxy('http://'+dbhost+':8069/xmlrpc/object')

    try:
        categ_name = str(product['public_categ_id']).title()
    except KeyError:
        pass

    try:
        if categ_name:
            categ_id = get_product_categ_id(sock, uid, dbname, dbpass, categ_name)
    except UnboundLocalError:
        pass

    try:
        if categ_id:
            product.update({'public_categ_id': categ_id[0]})
        else:
            try:
                del product['public_categ_id']
            except KeyError:
                pass
    except UnboundLocalError:
        pass

    product_id = sock.execute(dbname, uid, dbpass, 'product.product', 'create', product)
    print "Creado producto %s" % str(product['name'])

def build_dict_products(dbuser, dbpass, dbhost, dbname):
    product_list = []
    autotech_product = {}

    Base = automap_base()
     
    engine = create_engine('mysql://'+dbuser+':'+dbpass+'@'+dbhost+'/'+dbname+'')

    Base.prepare(engine, reflect=True)

    #Table schemes
    products = Base.classes.products
    products_description = Base.classes.products_description

    #Table with id for categories
    products_attributes =  Base.classes.products_attributes

    #Table with types of products
    products_options = Base.classes.products_options

    session = Session(engine)

    #Products query
    products = session.query(products).all()
    i = 0

    #Products Attributes Query
    for product in products: 
        autotech_product.update({'name' : product.products_model})

        query_descriptions = session.query(products_description).filter(products_description.products_id == product.products_id)
        descriptions = query_descriptions.all()

        for description in descriptions:
            autotech_product.update({'more_info' : description.products_description})

        query_attributes = session.query(products_attributes).filter(products_attributes.products_id == product.products_id)
        attributes = query_attributes.all()

        for attr in attributes:
            try:
                query_categories = session.query(products_options).filter(products_options.products_options_id == attr.options_id)
                product_types = query_categories.all()

                for typ in product_types:
                    autotech_product.update({'public_categ_id' : typ.products_options_name})
            except AttributeError:
                print "product_id no encontrado en la tabla products_attributes"

        create_autotech_products(odoo_dbuser, odoo_dbpass, odoo_dbname, odoo_dbhost, autotech_product)

def main():
    build_dict_products(mysql_dbuser, mysql_dbpass, mysql_dbhost, mysql_dbname)

main()
