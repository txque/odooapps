from odoo import models, fields

class StockMove(models.Model):
    _inherit = "stock.move"

    product_image = fields.Image(related='product_id.image_128', readonly=True, store=False)


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    product_image = fields.Image(related='product_id.image_128', readonly=True, store=False)
