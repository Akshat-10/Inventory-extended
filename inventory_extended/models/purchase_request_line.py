from odoo import fields, models

class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    remarks = fields.Text(string="Remarks")
    
    item_code = fields.Char(
        related='product_id.default_code',
        string="Item Code",
        # readonly=True,
        help="The internal reference or code of the product."
    )
    material = fields.Char(
        related='product_id.name',
        string="Material",
        # readonly=True,
        help="The name of the product."
    )
    hsn_sac_code = fields.Char(
        related='product_id.l10n_in_hsn_code',
        string="HSN/SAC Code",
        # readonly=True,
        help="The HSN/SAC code of the product as per Indian tax regulations."
    )