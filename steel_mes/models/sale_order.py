from odoo import models, fields, api
import requests
from ..utils.jwt_utils import get_valid_token, get_jwt_mes_config
from odoo.exceptions import (
    UserError
)
import logging
_logger = logging.getLogger(__name__)


# MES_API_URL = "http://localhost:8000/ed/api/v1/order/"

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def send_to_mes(self):
        mes_config = get_jwt_mes_config(self.env.user)
        token = get_valid_token(self.env.user)
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "order": {
                "order_code": self.name,
                "sap_order_code": self.name,
                "type_of_order": "1",
                "destination_country": self.country_code,
            },
            "order_items": [],
        }

        for order_item in self.order_line:
            mes_spec_code = None
            mes_rolling_code = None

            try:
                if order_item.mes_spec:
                    r = requests.get(mes_config.mes_api_url + f"/spec/{order_item.mes_spec}", timeout=5, headers=headers)
                    r.raise_for_status()
                    mes_spec_code = r.json()['spec_code']
                if order_item.mes_rolling:
                    r = requests.get(mes_config.mes_api_url + f"/rolling/{order_item.mes_rolling}", timeout=5, headers=headers)
                    r.raise_for_status()
                    mes_rolling_code = r.json()['rolling_code']
            except Exception as e:
                raise UserError(f"MES查询spec和rolling失败：{e}")
            payload["order_items"].append({
                "line_item_code": order_item.name,
                "plant_id": 1,
                "product_type_id": order_item.mes_product_type,
                "spec_id": order_item.mes_spec,
                "rolling_id": order_item.mes_rolling,
                "rolling_code": mes_rolling_code,
                "spec_code": mes_spec_code,
                "quantity": order_item.product_uom_qty,
                "stocked_quantity": 0,
                "length_mm": order_item.mes_length_mm,
            })

        try:
            response = requests.post(mes_config.mes_api_url + '/order/create_from_odoo', json=payload, headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise UserError(f"MES同步失败：{e}")


    # @api.model_create_multi
    # def create(self, vals_list):
    #     orders = super().create(vals_list)
    #     self.send_to_mes(orders=orders)
    #     return orders

    @api.model
    def mes_call_update_order(self, odoo_order_name):
        print(f"get param odoo_order_name: {odoo_order_name}")
        # orders = self.search([('quantity_field', '<', quantity)])  # 根据某个字段（如 quantity_field）筛选订单

        # for order in orders:
        #     order.write({'quantity_field': quantity})  # 更新订单的 quantity_field 字段

        return {"ok": True, "odoo_order_name": odoo_order_name}

