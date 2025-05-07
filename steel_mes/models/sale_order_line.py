from odoo import models, fields, api
import requests
import traceback

from ..utils.jwt_utils import get_valid_token, get_jwt_mes_config

import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    mes_product_type = fields.Selection(
        selection=lambda self: self._get_mes_product_type(),
        string='MES Product Type'
    )

    mes_spec = fields.Selection(
        selection=lambda self: self._get_mes_spec(),
        string='MES Spec'
    )

    mes_rolling = fields.Selection(
        selection=lambda self: self._get_mes_rolling(),
        string='MES Rolling'
    )

    mes_length_mm = fields.Char(
        string='MES Length MM',
    )

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        if 'mes_product_type' in res:
            res['mes_product_type']['selection'] = self._get_mes_product_type()
        if 'mes_spec' in res:
            res['mes_spec']['selection'] = self._get_mes_spec()
        if 'mes_rolling' in res:
            res['mes_rolling']['selection'] = self._get_mes_rolling()
        return res

    def _get_mes_product_type(self):
        try:
            mes_config = get_jwt_mes_config(self.env.user)
            token = get_valid_token(self.env.user)
            headers = {"Authorization": f"Bearer {token}"}

            r = requests.get(mes_config.mes_api_url + '/product_type/', timeout=5, headers=headers)
            r.raise_for_status()

            # Return selection options dynamically
            return [(str(x['id']), x['code']) for x in r.json().get('items', [])]

        except requests.exceptions.RequestException as e:
            _logger.error(f"Error fetching MES product types: {traceback.format_exc()}")

        except Exception as e:
            _logger.error(f"Unexpected error: {traceback.format_exc()}")

    def _get_mes_spec(self):
        try:
            mes_config = get_jwt_mes_config(self.env.user)
            token = get_valid_token(self.env.user)
            headers = {"Authorization": f"Bearer {token}"}

            r = requests.get(mes_config.mes_api_url + '/spec/', timeout=5, headers=headers)
            r.raise_for_status()

            # Return selection options dynamically
            return [(str(x['id']), x['spec_code']) for x in r.json().get('items', [])]

        except requests.exceptions.RequestException as e:
            _logger.error(f"Error fetching MES spec: {traceback.format_exc()}")

        except Exception as e:
            _logger.error(f"Unexpected error: {traceback.format_exc()}")

    def _get_mes_rolling(self):
        try:
            mes_config = get_jwt_mes_config(self.env.user)
            token = get_valid_token(self.env.user)
            headers = {"Authorization": f"Bearer {token}"}

            r = requests.get(mes_config.mes_api_url + '/rolling/', timeout=5, headers=headers)
            r.raise_for_status()

            # Return selection options dynamically
            return [(str(x['id']), x['rolling_code']) for x in r.json().get('items', [])]

        except requests.exceptions.RequestException as e:
            _logger.error(f"Error fetching MES rolling: {traceback.format_exc()}")

        except Exception as e:
            _logger.error(f"Unexpected error: {traceback.format_exc()}")