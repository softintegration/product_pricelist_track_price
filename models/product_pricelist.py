# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError

# Change the field description in the log according to given language,this is necessary because some times
# the description of the field is so technical or it is not relevant
# (lang,field_technical_name,new_description)
FIELD_DESCRIPTION_LOG = [('fr_FR', 'product.field_product_pricelist_item__fixed_price', 'Prix')]


class PricelistItem(models.Model):
    _name = "product.pricelist.item"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'product.pricelist.item']

    def _track_field_in_order(self,values,field):
        pricelists = self.mapped("pricelist_id")
        for pricelist in pricelists:
            if field == 'fixed_price':
                pricelist_items = self.filtered(lambda x: x.pricelist_id == pricelist)
                msg = "<b>" + _("The Price has been updated.") + "</b><ul>"
                for item in pricelist_items:
                    msg += "<li> %s: <br/>" % item.product_tmpl_id.display_name
                    msg += _(
                        "Price: %(old_price)s -> %(new_price)s",
                        old_price=getattr(item,field),
                        new_price=values[field]
                    ) + "<br/>"
                msg += "</ul>"
                pricelist.message_post(body=msg)

    def write(self, values):
        if 'fixed_price' in values:
            self._track_field_in_order(values,'fixed_price')
        return super(PricelistItem,self).write(values)

    # Below is an other solution

    #fixed_price = fields.Float('Fixed Price', digits='Product Price', track_visibility='onchange')

    #@api.model
    #def _field_description_log(self, field_id):
    #    for lang, field_techname, field_description in FIELD_DESCRIPTION_LOG:
    #        if self.env.context.get('lang') != lang:
    #            continue
    #        field = self.env.ref(field_techname)
    #        if field.id == field_id:
    #            return field_description

    #@api.model
    #def _append_note(self, note, desc, position='before'):
    #    if position == 'before':
    #        return '%s %s' % (note, desc)
    #    elif position == 'after':
    #        return '%s %s' % (desc, note)
    #    else:
    #        return desc

    #def _message_create(self, values_list):
    #    res = super(PricelistItem, self)._message_create(values_list)
    #    values_list.update({'model': 'product.pricelist', 'res_id': self.pricelist_id.id})
    #    for tracking_value in values_list['tracking_value_ids']:
    #        try:
    #            field_dict = tracking_value[2]
    #            new_field_desc = self._field_description_log(field_dict['field'])
    #            if new_field_desc:
    #                new_field_desc = self._append_note(self.product_tmpl_id.display_name,new_field_desc)
    #                field_dict['field_desc'] = new_field_desc
    #        except IndexError as ie:
    #            continue
    #    self.pricelist_id._message_create(values_list)
    #    return res
