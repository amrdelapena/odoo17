# -*- coding: utf-8 -*-
# roomtypes.py

from odoo import models, fields, api

class roomtypes(models.Model):
    _name = 'hotel.roomtypes'
    _description = 'room types master list'

    name = fields.Char("Room Type")
    description = fields.Text("Room Type Description")
    daily_charge = fields.Float("Daily Charge")

    # Image Fields for the Images Page
    room_image = fields.Image("Room Image", attachment=False, store=True)
    bathroom_image = fields.Image("Bathroom Image", attachment=False, store=True)

