# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class guestregistration(models.Model):
    _name = 'hotel.guestregistration'
    _description = 'Hotel guest registration list'

    room_id = fields.Many2one("hotel.rooms", string="Room No.")
    guest_id = fields.Many2one("hotel.guests", string="Guest Name")

    # roomname -< related fields found in the model hotel.rooms    
    roomname = fields.Char("Room No.", related='room_id.name')

    # roomtname <- room type name found in the model hotel.rooms 
    # also related to hotel.roomtypes
    #roomtypename = fields.Char("Room Type", related='room_id.roomtypename')

    # guestname <- related field found as a computed field called name in 
    # the model hotel.guests
    guestname = fields.Char("Guest Name", related='guest_id.name')

    datecreated = fields.Date("Date Created", default=lambda self: fields.Date.today())
    datefromSched = fields.Date("Scheduled Check In")
    datetoSched = fields.Date("Scheduled Check Out")
    datefromAct = fields.Date("Actual Check In")
    datetoAct = fields.Date("Actual Check Out")

    # computed field called name <- concatenation of room name and guest name
    name = fields.Char("Guest Registration", compute='_compute_name', store=False)

    # State field representing different stages of registration
    state = fields.Selection([
        ('DRAFT', 'Draft'),
        ('RESERVED', 'Reserved'),
        ('CHECKEDIN', 'Checked In'),
        ('CHECKEDOUT', 'Checked Out'),
        ('CANCELLED', 'Cancelled')
    ], string="Status", default="DRAFT", tracking=True)

    @api.depends('room_id', 'guest_id')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.roomname}, {rec.guestname}"

    # Methods to change state
    def action_reserve(self):
        for rec in self:
            if rec.state != 'DRAFT':
                raise ValidationError("You can only reserve when the status is Draft.")
            rec.state = 'RESERVED'

    def action_checkin(self):
        for rec in self:
            if rec.state != 'RESERVED':
                raise ValidationError("You can only check-in a reserved room.")
            rec.state = 'CHECKEDIN'

    def action_checkout(self):
        for rec in self:
            if rec.state != 'CHECKEDIN':
                raise ValidationError("You can only check-out a checked-in room.")
            rec.state = 'CHECKEDOUT'

    def action_cancel(self):
        for rec in self:
            if rec.state in ['CHECKEDIN', 'CHECKEDOUT']:
                raise ValidationError("You cannot cancel a registration that is already checked-in or checked-out.")
            rec.state = 'CANCELLED'