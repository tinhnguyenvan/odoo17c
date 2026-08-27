# -*- coding: utf-8 -*-
# Copyright 2026 NGUYEN VAN TINH <tinhnguyenvan91@gmail.com>
# Website: https://tweb.com.vn/ | Tel: 0909977920
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    hosting_expiry_date = fields.Date(
        string="Ngày hết hạn dịch vụ",
        tracking=True,
        copy=False,
        help="Nhập tay ngày hết hạn hosting/domain của đơn hàng này. "
             "Dùng để hiển thị trong email nhắc gia hạn.",
    )
    hosting_renewal_note = fields.Char(
        string="Ghi chú gia hạn",
        copy=False,
        help="Dòng ghi chú tuỳ chọn hiển thị trong email (VD: tên miền, gói dịch vụ).",
    )
    hosting_days_left = fields.Integer(
        string="Số ngày còn lại",
        compute="_compute_hosting_days_left",
        help="Âm = đã hết hạn. Dùng trong mail template để đổi nội dung.",
    )

    @api.depends("hosting_expiry_date")
    def _compute_hosting_days_left(self):
        today = fields.Date.context_today(self)
        for order in self:
            order.hosting_days_left = (
                (order.hosting_expiry_date - today).days
                if order.hosting_expiry_date
                else 0
            )

    def action_send_hosting_renewal_mail(self):
        """Mở wizard soạn mail với template nhắc gia hạn."""
        self.ensure_one()
        template = self.env.ref(
            "tweb_hosting_renewal_mail.mail_template_hosting_renewal",
            raise_if_not_found=False,
        )
        return {
            "type": "ir.actions.act_window",
            "name": _("Gửi email nhắc gia hạn"),
            "res_model": "mail.compose.message",
            "view_mode": "form",
            "views": [(False, "form")],
            "target": "new",
            "context": {
                "default_model": "sale.order",
                "default_res_ids": self.ids,
                "default_composition_mode": "comment",
                "default_template_id": template.id if template else False,
                "default_email_layout_xmlid": "mail.mail_notification_light",
                "force_email": True,
                "mark_so_as_sent": False,
            },
        }
