# -*- coding: utf-8 -*-
# rooms.py

from odoo import models, fields, api

class rooms(models.Model):
    _name = 'hotel.rooms'
    _description = 'hotel rooms'

    name = fields.Char("Room No.")
    description = fields.Text("Room Description")

    roomtype_id = fields.Many2one('hotel.roomtypes', string="Room Type")
