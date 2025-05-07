from odoo import models, fields, api
import requests
from ..utils.jwt_utils import get_valid_token, get_jwt_mes_config
from odoo.exceptions import (
    UserError
)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def sync_sale_partner_to_mes(self):
        mes_config = get_jwt_mes_config(self.env.user)

        payload = {
            "name": self.name,
            "code": self.name,
            "address_line_1": self.country_id.name if self.country_id else None,
            "address_line_2": self.city,
            "address_line_3": self.state_id.name if self.state_id else None,
            "address_line_4": self.street,
            "address_line_5": self.street2,
            # "customer_type":customer_in["customer_type"],
            # "group":customer_in["group"],
            # "desc":customer_in["desc"],
            # "coh_code":customer_in["coh_code"],
        }
        token = get_valid_token(self.env.user)
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.post(mes_config.mes_api_url + '/customer/sync_customer_from_odoo', json=payload,
                                     headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise UserError(f"MES同步失败：{e}")