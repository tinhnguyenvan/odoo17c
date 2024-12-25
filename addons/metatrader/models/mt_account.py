# importing
import subprocess
import ast
from odoo import fields, models
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)


class MetaTrader(models.Model):
    """Metatrader Account"""
    _name = "meta.trader.account"
    _description = "Metatrader Account"

    # login info
    login = fields.Char(string="ID login")
    password = fields.Char("Password")
    server = fields.Char(string="Server")

    # account info
    trade_mode = fields.Integer(string='Trade Mode')
    leverage = fields.Integer(string="Leverage")
    limit_orders = fields.Integer(string="Limit Orders")
    margin_so_mode = fields.Integer(string="Margin SO mode")
    trade_allowed = fields.Boolean(string="Trade Allow")
    trade_expert = fields.Boolean(string="Trade Expert")
    margin_mode = fields.Integer(string="Margin Mode")
    currency_digits = fields.Integer(string="Currency Digits")
    fifo_close = fields.Boolean(string="Fifo Close")
    balance = fields.Float(string="Balance")
    credit = fields.Float(string="Credit")
    profit = fields.Float(string="Profit")
    equity = fields.Float(string="Equity")
    margin = fields.Float(string="Margin")
    margin_free = fields.Float(string="Margin Free")
    margin_level = fields.Float(string="Margin Level")
    margin_so_call = fields.Float(string="Margin SO Call")
    margin_so_so = fields.Float(string="Margin SO so")
    margin_initial = fields.Float(string="Margin Initial")
    margin_maintenance = fields.Float(string="Margin Maintenance")
    assets = fields.Float(string="Assets")
    liabilities = fields.Float(string="Liabilities")
    commission_blocked = fields.Float(string="Commission Blocked")
    name = fields.Char(string="Name")
    currency = fields.Char(string="Currency")
    company = fields.Char(string="Company")

    def _get_login_info(self):
        recs = self.search([])
        result = []
        for rec in recs:
            account_info = {'login': rec.login,
                            "password": rec.password,
                            "server": rec.server}
            result.append(account_info)
        return result

    def _get_infomation_by_logins(self):
        script_path = self.env['ir.config_parameter'].sudo(
        ).get_param("mt5.get_info_script_path")
        if not script_path:
            raise ValidationError(
                "Please setup 'mt5.get_info_script_path' on system parameter")
        login_accounts = self._get_login_info()
        for login_account in login_accounts:
            login = login_account['login']
            pw = login_account['password']
            mt5server = login_account['server']
            commands = [
                'wine', 'python', f'{script_path}/get_account_info.py', f"{int(login)}", f"{pw}", f"{mt5server}"
            ]
            try:
                result = subprocess.run(commands,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True,
                                        cwd=script_path)
                if result.returncode == 0:
                    result = ast.literal_eval(result.stdout)
                    logger.info(f"login to ID {login} success")
                    login_id = self.search([('login', '=', login)])
                    if login_id:
                        login_id.write(result)
                    else:
                        self.create(result)
                else:
                    raise ValidationError(
                        'There have unexpected error. please contact to your Administrator')
            except Exception as e:
                logger.error(f"ID login {login} has error: {e}")

    def cron_get_information(self):
        return self._get_infomation_by_logins()
