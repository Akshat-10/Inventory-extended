# -*- coding: utf-8 -*-
{
    
    "name": "Inventory Modification",
    "version": "18.0.1.0.0",
    "category": "Inventory",
    'sequence': 1,
    "author": "Akshat Gupta",
    'license': 'LGPL-3',    
    'website': 'https://github.com/Akshat-10',
    "installable": True,
    "application": True,
    "summary": "Custom modification in Inventory module including Purchase Request enhancements and shelf management",
    "depends": ['stock', 'sale', 'purchase', 'product', "purchase_request", "purchase_request_department",'l10n_in','product_automatic_internal_ref',],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_request_views.xml",
        "views/report_purchase_request.xml",
        "views/shelf_product_views.xml",
        'views/product_category_view_inherit.xml',
    ],
    
    
}
