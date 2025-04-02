# -*- coding: utf-8 -*-
# roomtypes.py

from odoo import models, fields, api


class roomtypes(models.Model):
    _name = 'hotel.rooms'
    _description = 'hotel rooms'

    name = fields.Char("Room No.")
    description = fields.Text("Room Description")

    #roomtype_id = fields.Many2one('hotel.roomtypes', string="Room Type")
    #roomtypename = fields.Char("Room Tpye", )_

