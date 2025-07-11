# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request, Response
import json

class PingController(http.Controller):
    @http.route('/ping', auth='public', methods=['GET'], type='http')
    def ping(self, **kwargs):
        headers = dict(request.httprequest.headers)
        # You may filter or manipulate the headers here if needed
        headers_json = json.dumps(headers)
        return Response(headers_json, content_type='application/json')