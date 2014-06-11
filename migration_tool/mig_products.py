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

def connect_mysql(dbuser, dbpass, dbhost, dbname):
    Base = automap_base()

    engine = create_engine('mysql://'+dbuser+':'+dbpass+'@'+dbhost+'/'+dbname+'')
    
    Base.prepare(engine, reflect=True)

    return Base, engine

def connect_odoo(dbhost, dbname, dbuser, dbpass):
    # Get the uid
    sock_common = xmlrpclib.ServerProxy ('http://'+dbhost+':8069/xmlrpc/common')
    uid = sock_common.login(dbname, dbuser, dbpass)

    sock = xmlrpclib.ServerProxy('http://'+dbhost+':8069/xmlrpc/object')

    return sock, uid

def get_product_categ_id(sock, uid, dbname, dbpass, product_categ_name):

    filt = [('name','=', product_categ_name)]

    categ_id = sock.execute(dbname, uid, dbpass, 'product.public.category', 'search', filt)

    return categ_id

def get_manufacture_id(sock, uid, dbname, dbpass, manufacture_name):

    filt = [('name','=', manufacture_name)]

    manufacture_id = sock.execute(dbname, uid, dbpass, 'res.partner', 'search', filt)

    return manufacture_id

def create_manufacturers(dbname, dbpass, uid, sock, manufacture):

    manufacture.update({'supplier' : True, 'customer' : False})

    manufacture_id = sock.execute(dbname, uid, dbpass, 'res.partner', 'create', manufacture)
    print "Manufacture %s created" % str(manufacture['name'])

def create_autotech_products(dbname, dbpass, uid, sock, product):
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

    try:
        manufacture_name = str(product['manufacture']).title()
    except KeyError:
        pass

    try:
        manufacture_id = get_manufacture_id(sock, uid, dbname, dbpass, manufacture_name)
    except UnboundLocalError:
        pass

    try:
        if manufacture_id:
            product.update({'manufacture': manufacture_id[0]})
        else:
            try:
                del product['manufacture']
            except KeyError:
                pass
    except UnboundLocalError:
        pass

    product_id = sock.execute(dbname, uid, dbpass, 'product.product', 'create', product)
    print "Product %s created" % str(product['name'])

def get_and_create_products(Base, engine, uid, sock):
    product_list = []
    autotech_product = {}

    #Table schemes
    products = Base.classes.products
    products_description = Base.classes.products_description

    #Table with id for categories
    products_attributes =  Base.classes.products_attributes

    #Table with types of products
    products_options = Base.classes.products_options

    #Table with manufacturers
    products_manufacturers =  Base.classes.manufacturers

    session = Session(engine)

    #Products query
    products = session.query(products).all()

    #Products Attributes Query
    for product in products: 
        autotech_product.update({'name' : product.products_model})
        autotech_product.update({'weight' : float(product.products_weight)})

        query_descriptions = session.query(products_description).filter(products_description.products_id == product.products_id)
        descriptions = query_descriptions.all()

        for description in descriptions:
            autotech_product.update({'more_info' : description.products_description})

        query_manufactures = session.query(products_manufacturers).filter(products_manufacturers.manufacturers_id == product.manufacturers_id)
        manufacturers = query_manufactures.all()
        
        for manufacture in manufacturers:
            autotech_product.update({'manufacture' : manufacture.manufacturers_name})

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

        create_autotech_products(odoo_dbname, odoo_dbpass, uid, sock, autotech_product)

def get_and_create_manufacturers(Base, engine, uid, sock):
    manufac = {}

    db_manufacturers =  Base.classes.manufacturers

    session = Session(engine)

    manufacturers = session.query(db_manufacturers).all()
    
    for manufacture in manufacturers:
        manufac.update({'name' : str(manufacture.manufacturers_name).title()})
        create_manufacturers(odoo_dbname, odoo_dbpass, uid, sock, manufac)

def main():
    (Base, engine) = connect_mysql(mysql_dbuser, mysql_dbpass, mysql_dbhost, mysql_dbname)
    (sock, uid) = connect_odoo(odoo_dbhost, odoo_dbname, odoo_dbuser, odoo_dbpass)
    get_and_create_manufacturers(Base, engine, uid, sock)
    get_and_create_products(Base, engine, uid, sock)

main()
