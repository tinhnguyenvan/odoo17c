from odoo import models, fields, api


class RealEstateContract(models.Model):
    _name = 'real.estate.contract'
    _description = 'Hợp đồng cho thuê lại căn hộ'

    name = fields.Char(string='Mã hợp đồng', required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('real.estate.contract'))
    unit_id = fields.Many2one('real.estate.unit', string='Căn hộ', required=True)
    tenant_id = fields.Many2one('res.partner', string='Khách thuê', required=True)
    rental_price = fields.Float('Giá thuê/tháng', required=True)
    start_date = fields.Date('Từ ngày', required=True)
    end_date = fields.Date('Đến ngày')
    state = fields.Selection([
        ('draft', 'Dự thảo'),
        ('active', 'Hiệu lực'),
        ('terminated', 'Đã kết thúc')
    ], default='draft', string='Trạng thái')
    notes = fields.Text('Ghi chú')

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.unit_id:
            res.unit_id.write({'tenant_id': res.tenant_id.id, 'state': 'rented'})
        return res
