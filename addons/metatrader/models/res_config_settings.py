from odoo import models, fields


class IRConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    metatrader_script_path = fields.Char(
        string="MT5 trader Path", config_parameter="mt5.get_info_script_path")
