# -*- coding: utf-8 -*-



# class cinema_management(models.Model):
#     _name = 'cinema_management.cinema_management'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
from odoo import models, fields, api

class movie(models.Model):
    _name = "movie"
    _description = "Cinema Management"

    name = fields.Char("Movie Name", require=True)
    genre = fields.Selection([('comedy', 'Comedy'),('action','Action'),('animated','Animated'),('horor','Horor')], string="Genre")
    release_year = fields.Integer("Release Year")
    description = fields.Text("Description")
    image = fields.Binary("Image")
    timetable = fields.One2many('movie.timetable', 'movie', 'Timetable')

class movie_timetable(models.Model):
    _name = "movie.timetable"
    _description = "Cinema Timetable"
    _rec_name = 'date'

    date = fields.Datetime("Date", require=True)
    movie = fields.Many2one('movie', string="Movie", require=True)
    room = fields.Many2one('cinema.room', string="Room")
    premiere = fields.Boolean("Premiere")
    total_seats = fields.Integer(compute="_compute_toatal_seats", string="Total Seats")
    sold_seats = fields.Integer('Sold Seats')
    remaining_seats = fields.Integer(compute="_compute_remaining_seats", string="Remaining Seats")

    @api.depends('room')
    def _compute_toatal_seats(self):
        for record in self:
            if record.room:
                record.total_seats = record.room.capacity
            else:
                record.total_seats = 0

    @api.depends('room')
    def _compute_remaining_seats(self):
        for record in self:
            if record.room:
                record.remaining_seats = record.total_seats - record.sold_seats
            else:
                record.remaining_seats = 0

class cinema_room(models.Model):
    _name = "cinema.room"
    _description = "Cinema Room"

    name = fields.Char("Name", require=True)
    capacity = fields.Integer("Capacity", require=True)
    timetable = fields.One2many('movie.timetable', 'room', string='Room')

class product_product(models.Model):
    _name = "product.product"
    _description = "eTicke Product"
    _inherit = 'product.product'

    e_ticket = fields.Boolean("Ticket")