# -*- coding: utf-8 -*-
import requests
from odoo import api, fields, models
from ..utils.jwt_utils import get_valid_token, get_jwt_mes_config
from odoo.exceptions import (
    UserError
)
class MesRole(models.Model):
    _name = 'mes.role'
    _description = u'MES Role'

    name = fields.Char(string="角色名称")
    key = fields.Char(string="角色标识")
    sort = fields.Integer(string="排序")
    status = fields.Boolean(string="是否启用")
    admin = fields.Boolean(string="是否管理员")
    remark = fields.Char(string="备注")
    homepage_path = fields.Char(string="主页地址")

    menu_ids = fields.Many2many(
        comodel_name='mes.menu',
        relation='mes_menu_role_rel', column1='mes_menu_id', column2='mes_role_id',
        string="菜单名称")

    menu_lines = fields.One2many(comodel_name="mes.role.menu.rel", inverse_name="role_id", string="Menu Permissions")


    def sync_role_send_to_mes(self):
        ''' 同步role信息
            "name": "test",
            "key": "test",
            "remark": "test",
            "homepage_path": "1",
            "sort": 1,
            "admin": false,

            "menu": [
                {
                    "name": "1111",
                    "web_path": "/1111",
                    "menu_buttons": [
                        {
                            "name": "123",
                            "value": "123",
                            "api": "123",
                            "method": "123"
                        }

                    ]
                }
            ]

        '''
        mes_config = get_jwt_mes_config(self.env.user)

        payload = {
            "name": self.name,
            "key": self.key,
            "sort": self.sort,
            "status": self.status,
            "admin": self.admin,
            "remark": self.remark,
            "homepage_path": self.homepage_path,
            "menu":[]
        }

        if len(self.menu_lines)>0:
            for menu in self.menu_lines:
                print(menu.button_ids)
                menu_dict = {
                    "name": menu.menu_id.name,
                    "web_path": menu.menu_id.web_path,
                    "menu_buttons": []
                }
                if menu.button_ids:
                    for button in menu.button_ids:
                        menu_dict["menu_buttons"].append({
                            "name": button.name,
                            "value": button.value,
                            "api": button.api
                        })
                print(menu_dict)
                payload["menu"].append(menu_dict)
        token = get_valid_token(self.env.user)
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.post(mes_config.mes_api_url + '/role/sync_role_from_odoo', json=payload,
                                     headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise UserError(f"MES同步失败：{e}")

    def role_delete_send_to_mes(self):
        '''mes role 删除时同步内容'''
        mes_config = get_jwt_mes_config(self.env.user)
        payload= {
            "name": self.name
        }

        token = get_valid_token(self.env.user)
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.post(mes_config.mes_api_url + '/role/delete_role_from_odoo', json=payload, headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise UserError(f"MES同步失败：{e}")

    def unlink(self):
        if self.name:
            self.role_delete_send_to_mes()
        return super().unlink()


class MesRoleMenuRel(models.Model):
    _name = "mes.role.menu.rel"

    role_id = fields.Many2one(comodel_name="mes.role", string="角色")
    menu_id = fields.Many2one(comodel_name="mes.menu", string="菜单", required=True)
    button_ids = fields.Many2many(comodel_name="mes.menu.button", string="按钮")

    @api.onchange('menu_id')
    def _onchange_menu_id(self):
        if self.menu_id:
            print("menu_id",self.menu_id)
            return {
                'domain': {
                    'button_ids': [('mes_menu_id', '=', self.menu_id.id)]
                }
            }