# -*- coding: utf-8 -*-


from odoo import models, fields, api, exceptions

class movie(models.Model):
    _name = "movie"
    _description = "Cinema Management"
    _order = "id desc"

    name = fields.Char("Movie Name", require=True)
    genre = fields.Selection([('comedy', 'Comedy'),('action','Action'),('animated','Animated'),('horor','Horor')], string="Genre")
    release_year = fields.Integer("Release Year", format=None)
    description = fields.Text("Description")
    image = fields.Binary("Image")
    timetable = fields.One2many('movie.timetable', 'movie', 'Timetable')

class movie_timetable(models.Model):
    _name = "movie.timetable"
    _description = "Cinema Timetable"
    _rec_name = 'date'
    _order = "date desc"

    date = fields.Datetime("Start Date", require=True)
    date_end = fields.Datetime("End Date", require=True)
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

    @api.multi
    def sell_tickets_wizard(self):

        return {

            'type': 'ir.actions.act_window',
            'name': 'sell_cinema_tickets_wizard_form',
            'view_type': 'form',
            'view_mode': 'form',
            'context': {},
            'res_model': 'sell.cinema.tickets.wizard',
            'target': 'new',

        }

class sell_cinema_tickets_wizard(models.TransientModel):
    _name = "sell.cinema.tickets.wizard"
    _description = "Wizard for selling tickets"

    def _get_movies_timetable(self):
        return self.env['movie.timetable'].browse(self._context.get('active_ids'))

    tickets = fields.Integer("Number of tickets")
    movies_timetable = fields.Many2one('movie.timetable', string="Movies Timetable", default=_get_movies_timetable)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True, domain="[('customer', '=', True)]")
    product_id = fields.Many2one('product.product', string="Product", required=True, domain="[('e_ticket', '=', True)]")

    @api.multi
    def sell_tickets(self):
        for record in self:
            if record.movies_timetable:
                if not record.product_id.e_ticket:
                    raise exceptions.Warning('Warning!!! Only eTicket product can be used in this transaction!')
                if record.tickets < 1:
                    raise exceptions.Warning('Warning!!! Number of tickets to sold must be grater than 1!')
                elif record.movies_timetable.remaining_seats < record.tickets:
                    raise exceptions.Warning('Warning!!! Number of remain seats is less than the number of tickets to sell!')
                else:
                    record.movies_timetable.sold_seats += record.tickets
                    invoice = self.env['account.invoice'].create(
                        {
                            'partner_id':record.partner_id.id
                        }
                    )
                    self.env['account.invoice.line'].create(
                        {
                            'name': record.product_id.name,
                            'product_id': record.product_id.id,
                            'quantity': record.tickets,
                            'invoice_id': invoice.id,
                            'price_unit': record.product_id.lst_price,
                            'account_id' : invoice.account_id.id
                        }
                    )
                    invoice.action_invoice_open()
                    invoice.action_invoice_sent()
                    return {

                        'type': 'ir.actions.act_window',
                        'name': 'account.invoice_form',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'context': {},
                        'res_model': 'account.invoice',
                        'res_id': invoice.id,
                        'target': 'current',
                    }

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