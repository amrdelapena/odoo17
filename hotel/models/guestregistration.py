from odoo import models, fields, api
from odoo.exceptions import ValidationError

class guestregistration(models.Model):
    _name = 'hotel.guestregistration'
    _description = 'Hotel guest registration list'

    room_id = fields.Many2one("hotel.rooms", string="Room No.")
    guest_id = fields.Many2one("hotel.guests", string="Guest Name")

    # roomname -< related fields found in the model hotel.rooms    
    roomname = fields.Char("Room No.", related='room_id.name')

    # roomtypename - related to hotel.roomtypes (if needed)
    roomtypename = fields.Char("Room Type", related='room_id.roomtype_id.name')

    # guestname - related field found as a computed field called name in 
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
            # Handle case where roomname or guestname is empty
            rec.name = f"{rec.roomname or 'Unknown Room'}, {rec.guestname or 'Unknown Guest'}"

    def action_reserve(self):
        for rec in self:
            if rec.state != 'DRAFT':
                raise ValidationError("You can only reserve when the status is Draft.")
            elif not rec.room_id or not rec.guest_id:
                raise ValidationError("Please select both a valid Room and a Guest before reserving.")
            elif not rec.datetoSched or not rec.datefromSched:
                raise ValidationError("Please select both a valid date to Check In and Check Out before reserving.")
            elif not rec.datecreated:
                raise ValidationError('Please input a date.')
            elif rec.datetoSched < rec.datefromSched:
                raise ValidationError('Invalid Date Range')
            else:
                #Room Schedule Conflict //This works fine.
                overlapping_room = self.search([
                    ('id', '!=', rec.id),
                    ('room_id', '=', rec.room_id.id),
                    ('state', 'in', ['RESERVED', 'CHECKEDIN']),
                    ('datefromSched', '<=', rec.datetoSched),
                    ('datetoSched', '>=', rec.datefromSched),
                ])
                if overlapping_room:
                    raise ValidationError(f"Room '{rec.room_id.name}' is already booked for the selected schedule.")

                # Guest Schedule Conflict
                overlapping_guest = self.search([
                    ('id', '!=', rec.id),
                    ('guest_id', '=', rec.guest_id.id),
                    ('state', 'in', ['RESERVED', 'CHECKEDIN']),
                    ('datefromSched', '<=', rec.datetoSched),
                    ('datetoSched', '>=', rec.datefromSched),
                ])
                if overlapping_guest:
                    raise ValidationError(f"Guest '{rec.guest_id.name}' already has a conflicting reservation.")

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
