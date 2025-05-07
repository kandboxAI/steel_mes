# -*- coding: utf-8 -*-

from odoo import api, fields, models
import requests
from odoo.http import request

from ..utils.jwt_utils import get_valid_token, get_jwt_mes_config
from odoo.exceptions import (
    UserError
)

class MesMenu(models.Model):
    _name = 'mes.menu'
    _description = u'MES Menu'

    name = fields.Char(string="菜单名称")
    title = fields.Char(string="菜单标识")
    sort = fields.Integer(string="排序")
    icon = fields.Char(string="icon")

    is_link = fields.Boolean(string="是否外链")
    is_catalog = fields.Boolean(string="是否目录")
    web_path = fields.Char(string="路由地址")
    component = fields.Char(string="组件")
    component_name = fields.Char(string="组件名称")
    status = fields.Boolean(string="菜单状态")
    visible = fields.Boolean(string="侧边栏中是否显示")
    desc = fields.Char(string="备注")

    parent_id = fields.Many2one(
        comodel_name='mes.menu',
        string='父级菜单'
    )

    button_ids = fields.One2many(
        comodel_name='mes.menu.button',
        inverse_name='mes_menu_id',
        string='菜单按钮'
    )

    def menu_create_send_to_mes(self,menus):
        '''mes menu 创建时同步内容'''
        mes_config = get_jwt_mes_config(self.env.user)

        for menu in menus:
            payload = {
                "menu": {
                    "name": menu.name,
                    "title": menu.title,
                    "sort": menu.sort,
                    "icon": menu.icon,

                    "is_link": menu.is_link,
                    "is_catalog": menu.is_catalog,
                    "web_path": menu.web_path,
                    "component": menu.component,
                    "component_name": menu.component_name,
                    "status": menu.status,
                    "visible": menu.visible,
                    "desc": menu.desc,
                    "parent_name": menu.parent_id.name if menu.parent_id.id else None,
                },
                "menu_buttons": [],
            }

            for button in menu.button_ids:
                payload["menu_buttons"].append({
                    "name": button.name,
                    "value": button.value,
                    "remark": button.remark,
                    "api":""

                })

            token = get_valid_token(self.env.user)
            headers = {"Authorization": f"Bearer {token}"}
            try:
                response = requests.post(mes_config.mes_api_url + '/menu/create_menu_from_odoo', json=payload, headers=headers)
                response.raise_for_status()
            except Exception as e:
                raise UserError(f"MES同步失败：{e}")



    def menu_update_send_to_mes(self,menus):
        '''mes menu 修改时同步内容'''
        mes_config = get_jwt_mes_config(self.env.user)
        payload= {"name": self.name}
        for key, value in menus.items():
            if key != "button_ids":
                payload.update({key: value})

        add_button = []
        update_button = []
        delete_button = []
        button_ids_commands = menus.get('button_ids', [])
        for command in button_ids_commands:
            op_type = command[0]
            if op_type == 0:
                # 新增
                add_button.append(command[2])
            elif op_type == 1:
                # 更新
                update_button_val = self.env['mes.menu.button'].sudo().search([("id", "=", int(command[1]))])
                command[2].update({"name": update_button_val.name})
                update_button.append(command[2])
            elif op_type == 2:
                # 删除
                delete_button_val = self.env['mes.menu.button'].sudo().search([("id", "=", int(command[1]))])
                delete_button.append(delete_button_val.name)

        if len(add_button) > 0:
            payload["add_button"] = add_button
        if len(update_button) > 0:
            payload["update_button"] = update_button
        if len(delete_button) > 0:
            payload["delete_button"] = delete_button


        token = get_valid_token(self.env.user)
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.post(mes_config.mes_api_url + '/menu/update_menu_from_odoo', json=payload, headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise UserError(f"MES同步失败：{e}")


    def menu_delete_send_to_mes(self):
        '''mes menu 删除时同步内容'''
        mes_config = get_jwt_mes_config(self.env.user)
        payload= {
            "name": self.name,
            "web_path": self.web_path,
        }

        token = get_valid_token(self.env.user)
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.post(mes_config.mes_api_url + '/menu/delete_menu_from_odoo', json=payload, headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise UserError(f"MES同步失败：{e}")




    @api.model_create_multi
    def create(self, vals_list):
        menus = super().create(vals_list)
        self.menu_create_send_to_mes(menus=menus)
        return menus


    def write(self, vals):
        self.menu_update_send_to_mes(menus=vals)
        res = super().write(vals)

        return res

    def unlink(self):
        self.menu_delete_send_to_mes()
        return super().unlink()



class MesMenuButton(models.Model):
    _name = 'mes.menu.button'
    _description = u'MES Menu Button'

    name = fields.Char(string="按钮名称")
    value = fields.Char(string="按钮值")
    remark = fields.Char(string="备注")
    api = fields.Char(string="api")


    mes_menu_id = fields.Many2one(
        comodel_name='mes.menu',
        string='菜单'
    )

