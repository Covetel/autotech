# -*- coding: utf-8 -*-
from openerp.osv import osv, orm, fields
import pprint

class autotech_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'

    def hide_fields(self, cr, uid, ids, categ, context=None):
       categ_name = uom_obj=self.pool.get('product.public.category').browse(cr,uid,categ)
       domain = {'value' : {'domain' : categ_name.name}}
       return domain

    _columns = {
        'domain' : fields.char("Domain", store=False, invisible="1"),
        'sku' : fields.char("SKU"),
        'weight' : fields.float("Weight"),
        'height' : fields.float("Height"),
        'width' :  fields.float("Width"),
        "manufacture" : fields.many2one('res.partner', "Manufacture"),
        'oe_part' : fields.char("OE Part"),
        'chip_id' : fields.char("Chip ID"),
        'lenth' : fields.char("Lenth"),
        'keyway_type' : fields.char("Keyway Type"),
        'keyway_lico' : fields.char("Keyway Lico"),
        'cr_lico' : fields.char("C/R Lico"),
        'cr_lico_ez' : fields.char("C/R Lico EZ"),
        'cr_other' : fields.char("C/R Other"),
        'cr_strattec' : fields.char("C/R Strattec"),
        'code_series' : fields.char("Code Series"),
        'keyway_jma' : fields.char("Keyway JMA"),
        'compatible' : fields.char("Compatible"),
        'cutter' : fields.char("Cutter"),
        'products_by_make' : fields.char("Products By Make"),
        'motor' : fields.char("Motor"),
        'more_info' : fields.text("More Info"),
        'fcc_id' : fields.char("FCC ID"),
        'ic' : fields.char("IC"),
        'frequency' : fields.char("Frequency"),
        'number_of_button' : fields.char("Number of Button"),
        'material' : fields.char("Material"),
        'substitutes' : fields.char("Substitutes"),
        'reusable' : fields.boolean("Reusable"),
        'on_board_programming' : fields.boolean("On Board Programming"),
        'emergency_key' : fields.boolean("Emergency Key"),
        'battery_part' : fields.char("Battery Part"),
        'lock_type' : fields.char("Lock Type"),
        'coded' : fields.char("Coded"),
    }

autotech_product()
