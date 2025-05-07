from odoo import models, fields, api
import requests
from ..utils.jwt_utils import get_valid_token, get_jwt_mes_config
from odoo.exceptions import (
    UserError
)

class Company(models.Model):
    _inherit = 'res.company'

    def sync_company_send_to_mes(self):
        mes_config = get_jwt_mes_config(self.env.user)

        payload = {
            "code": self.name,
            "type": self.name,
            "desc": self.name,

        }
        token = get_valid_token(self.env.user)
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.post(mes_config.mes_api_url + '/mill/sync_mill_from_odoo', json=payload,
                                     headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise UserError(f"MES同步失败：{e}")