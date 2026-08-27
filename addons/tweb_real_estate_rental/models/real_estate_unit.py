from odoo import models, fields, api

class RealEstateUnit(models.Model):
    _name = 'real.estate.unit'
    _description = 'Căn hộ thuê và cho thuê lại'

    name = fields.Char('Mã căn hộ', required=True)
    address = fields.Text('Địa chỉ')
    rent_price = fields.Float('Giá thuê gốc')
    repair_cost = fields.Float('Chi phí sửa chữa')
    rental_price = fields.Float('Giá cho thuê lại')
    tenant_id = fields.Many2one('res.partner', string='Khách đang thuê')
    state = fields.Selection([
        ('empty', 'Trống'),
        ('repairing', 'Đang sửa chữa'),
        ('rented', 'Đang cho thuê')
    ], string='Trạng thái', default='empty')
    rent_start_date = fields.Date('Ngày thuê')
    rent_end_date = fields.Date('Hết hạn thuê')
    profit = fields.Monetary('Lợi nhuận/tháng', compute='_compute_profit')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)

    revenue = fields.Float('Doanh thu hàng tháng', compute='_compute_revenue')

    @api.depends('rent_price', 'repair_cost', 'rental_price')
    def _compute_profit(self):
        for rec in self:
            rec.profit = (rec.rental_price or 0.0) - (rec.rent_price or 0.0)

    @api.depends('rental_price', 'state')
    def _compute_revenue(self):
        for rec in self:
            rec.revenue = rec.rental_price if rec.state == 'rented' else 0.0
