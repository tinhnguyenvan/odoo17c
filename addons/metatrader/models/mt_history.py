import subprocess
import ast
from datetime import datetime
from odoo import models, fields
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)


class MT5History(models.Model):
    _name = 'meta.trader.history'
    _description = 'Meta Trader History'

    account_id = fields.Many2one('meta.trader.account')
    ticket = fields.Char(string="Ticket")
    order = fields.Char(string="Order")
    time = fields.Datetime(string="Time")
    time_msc = fields.Datetime(string="Time MSC")
    deal_type = fields.Char(string="Type")
    entry = fields.Char(string='Entry')
    magic = fields.Char(string="Magic")
    position_id = fields.Char(string='Position ID')
    reason = fields.Char(string="Reason")
    volume = fields.Char(string="Volume")
    price = fields.Float(string="Price")
    commission = fields.Float(string="Commission")
    swap = fields.Float(string="Swap")
    profit = fields.Float(string="Profit")
    fee = fields.Float(string='Fee')
    symbol = fields.Char(string='Symbol')
    comment = fields.Text(string='Comment')
    external_id = fields.Char(string='External ID')

    def _get_login_info(self):
        recs = self.env['meta.trader.account'].search([])
        result = []
        for rec in recs:
            account_info = {'login': rec.login,
                            "password": rec.password,
                            "server": rec.server}
            result.append(account_info)
        return result

    def _get_history_by_logins(self):
        def write_data_to_file(data, login_id, path):
            try:
                with open(f"{path}/history_logs/history_{login_id}.txt", 'w') as history_log:
                    if isinstance(data, list):
                        for e in data:
                            history_log.write(e + "\n")
                    else:
                        history_log.write(data)
            
            except Exception as e:
                logger.error(f"Have error while write to history_{login_id}:{e}")
            return True

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
                'wine', 'python', f'{script_path}/models/get_history_info.py', f"{int(login)}", f"{pw}", f"{mt5server}"
            ]
            try:
                results = subprocess.run(commands,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True,
                                        cwd=script_path+'/models')
                #logger.info(results)
                write_data_to_file(results.stdout, login, script_path)

                if results.returncode == 0:
                    with open(f"{script_path}/history_logs/history_{login}.txt", 'r') as history_file:
                        for line in history_file:
                            line = ast.literal_eval(line)
                            ticket_id = self.search([('ticket', '=', line.get('ticket', ''))])
                            #logger.info(f"{ticket_id}")
                            account_id = self.env['meta.trader.account'].search([('login','=', login)])
                            line['deal_type'] = line.pop('type')
                            line.pop('time_msc')
                            line['time'] = datetime.fromtimestamp(line['time'])
                            line['account_id'] = account_id.id
                            logger.info(f"{line}")
                            if ticket_id:
                                ticket_id.write(line)
                                logger.info(f"ticket update")
                            else:
                                ticket_id.create(line)
                                logger.info(f"new ticket created")
                        logger.info(f"Complete generate history ticket {line.get('ticket', '')}")
                    logger.info(f'Get history from ID {login} Done')
                #else:
                    #raise ValidationError(
                        #'There have unexpected error. please contact to your Administrator')
            except Exception as e:
                logger.error(f"ID login {login} has error: {e}")

    def cron_get_history_deals(self):
        return self._get_history_by_logins()
