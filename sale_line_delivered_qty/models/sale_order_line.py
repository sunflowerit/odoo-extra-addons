# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_delivered_stored = fields.Float(
        compute="_get_pick_qty",
        digits=dp.get_precision('Product Unit of Measure'),
        string='Delivered',
        store=True,
        help="Quantity Delivered"
    )

    @api.multi
    @api.depends('procurement_ids.move_ids.state')
    def _get_pick_qty(self):
        for record in self:
            #import pdb; pdb.set_trace()
            moves_to = record.mapped('procurement_ids.move_ids').filtered(
                lambda m: m.state == 'done' and m.location_id.usage == 'internal')
            moves_from = record.mapped('procurement_ids.move_ids').filtered(
                lambda m: m.state == 'done' and m.location_dest_id.usage == 'internal')
            qty_delivered = sum(moves_to.mapped('product_qty')) - sum(moves_from.mapped('product_qty'))
            # qty_delivered_list = moves.mapped('product_qty')
            # qty_delivered = sum(qty_delivered_list)
            record.qty_delivered_stored = qty_delivered




