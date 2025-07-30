from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class InventoryShelf(models.Model):
    _name = "inventory.shelf"
    _description = "Inventory Shelf"

    name = fields.Char(string="Rack Name", required=True)
    location_id = fields.Many2one("stock.location", string="Location", required=True)

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    shelf_id = fields.Many2one("inventory.shelf", string="Rack", domain="[('location_id', '=', location_dest_id)]")

class StockQuant(models.Model):
    _inherit = "stock.quant"

    shelf_id = fields.Many2one("inventory.shelf", string="Rack", domain="[('location_id', '=', location_id)]")

    @api.constrains('shelf_id', 'location_id')
    def _check_shelf_location(self):
        for quant in self:
            if quant.shelf_id and quant.shelf_id.location_id != quant.location_id:
                raise ValidationError(_("Shelf must belong to the quant's location."))

    def _get_grouping_key(self):
        """Override to include shelf_id in the quant uniqueness key"""
        key = super()._get_grouping_key()
        return key + ['shelf_id']

    @api.model
    def create(self, vals):
        """Set shelf_id from context if not provided in vals"""
        if 'shelf_id' not in vals and 'shelf_id' in self.env.context:
            vals['shelf_id'] = self.env.context['shelf_id']
        return super().create(vals)


class InventoryShelfProduct(models.Model):
    _name = "inventory.shelf.product"
    _description = "Shelf Product Assignment"
    _rec_name = "location_id"

    location_id = fields.Many2one("stock.location", string="Location", required=True)
    product_ids = fields.One2many("inventory.shelf.product.line", "shelf_product_id", string="Rack Products")


class InventoryShelfProductLine(models.Model):
    _name = "inventory.shelf.product.line"
    _description = "Shelf Product Line"

    shelf_product_id = fields.Many2one("inventory.shelf.product", string="Rack Product", required=True, ondelete="cascade")
    shelf_id = fields.Many2one("inventory.shelf", string="Rack", required=True, domain="[('location_id', '=', parent.location_id)]")
    product_ids = fields.Many2many("product.product", string="Products")

    _sql_constraints = [
        ('uniq_shelf', 'unique(shelf_id, shelf_product_id)', 'Shelf must be unique within a location.'),
    ]


class ProductProduct(models.Model):
    _inherit = "product.product"
    
    shelf_ids = fields.Many2many('inventory.shelf', 
                                 compute='_compute_shelf_ids',
                                 string='Racks')
    
    def _compute_shelf_ids(self):
        for product in self:
            shelf_product_lines = self.env['inventory.shelf.product.line'].search([
                ('product_ids', 'in', product.id)
            ])
            product.shelf_ids = shelf_product_lines.mapped('shelf_id')


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    shelf_ids = fields.Many2many('inventory.shelf', 
                                 compute='_compute_shelf_ids',
                                 string='Racks')
    
    def _compute_shelf_ids(self):
        for template in self:
            shelf_ids = template.product_variant_ids.mapped('shelf_ids')
            template.shelf_ids = shelf_ids