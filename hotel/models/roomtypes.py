from odoo import models, fields, api

class roomtypes(models.Model):
    _name = 'hotel.roomtypes'
    _description = 'Room Types Master List'

    name = fields.Char("Room Type", required=True)
    description = fields.Text("Room Type Description")
    daily_charge = fields.Float("Daily Charge")

    # Image Fields for the Images Page
    room_image = fields.Image("Room Image", store=True)
    bathroom_image = fields.Image("Bathroom Image", store=True)
    
    # One2many relation to the hotel.rooms model
    room_ids = fields.One2many('hotel.rooms', 'roomtype_id', string="Rooms")
