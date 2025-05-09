from odoo import models, fields, api

class rooms(models.Model):
    _name = 'hotel.rooms'
    _description = 'Hotel Rooms'

    name = fields.Char("Room No.")
    description = fields.Text("Room Description")

    roomtype_id = fields.Many2one('hotel.roomtypes', string="Room Type", required=True)

    # Optional: Order rooms by room number
    _order = 'name'

    # Optional: Add related field for Room Type Name if needed
    roomtype_name = fields.Char(related='roomtype_id.name', string="Room Type Name", store=True)
