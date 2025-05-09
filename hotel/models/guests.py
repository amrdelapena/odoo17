from datetime import date
from odoo import api, models, fields

class guests(models.Model):
    _name = 'hotel.guests'
    _description = 'Hotel Guests'

    lastname = fields.Char("Lastname", required=True)
    firstname = fields.Char("Firstname", required=True)
    middlename = fields.Char("Middlename")
    birthdate = fields.Date("Birthdate")
    age = fields.Integer("Age", compute="_compute_age", store=True)

    address_streetno = fields.Char("Address/ Street & No.")
    address_area = fields.Char("Address / Area, Unit & Bldg, Brgy")
    address_city = fields.Char("Address / City/Town")
    address_province = fields.Char("Address / Province/State")
    zipcode = fields.Char("ZIP Code")

    contactno = fields.Char("Contact No.")
    email = fields.Char("Email")

    gender = fields.Selection([
        ('FEMALE', 'Female'),
        ('MALE', 'Male')
    ], string="Gender")

    photo = fields.Image("Guest Photo")

    name = fields.Char(string='Guest Name', compute='_compute_name')

    _order = 'lastname, firstname, middlename'

    @api.depends('firstname', 'lastname', 'middlename')
    def _compute_name(self):
        for rec in self:
            full_name = f"{rec.lastname or ''}, {rec.firstname or ''}, {rec.middlename or ''}"
            rec.name = ', '.join(part for part in full_name.split(',') if part).strip()

    @api.depends('birthdate')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birthdate:
                birthdate = rec.birthdate
                rec.age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            else:
                rec.age = 0  # Default if no birthdate is provided
