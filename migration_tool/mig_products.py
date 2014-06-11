from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()
 
#Conexion
engine = create_engine('mysql://root:123321...@localhost/autotech')

Base.prepare(engine, reflect=True)

#Schemas de la tablas
products = Base.classes.products
products_description = Base.classes.products_description

#De aqui saco el id para la categoria
products_attributes =  Base.classes.products_attributes

#Lo que es en odoo category type
products_options = Base.classes.products_options

session = Session(engine)

#Query de productos all o first
products = session.query(products).all()

#Query atributos productos
for product in products: 
    query_attributes = session.query(products_attributes).filter(products_attributes.products_id == product.products_id)
    attributes = query_attributes.all()

    for attr in attributes:
        try:
            query_categories = session.query(products_options).filter(products_options.products_options_id == attr.options_id)
            product_types = query_categories.all()

            for typ in product_types:
                print typ.products_options_name

        except AttributeError:
            print "product_id no encontrado en la tabla products_attributes"
