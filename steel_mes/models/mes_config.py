# -*- coding: utf-8 -*-

from odoo import api, fields, models

class MesConfig(models.Model):
    _name = 'mes.config'
    _description = u'MES Config'

    name = fields.Char(string="配置名称", default="MES API 连接")
    mes_api_url = fields.Char(string="MES API 地址")
    # mes_api_key = fields.Char(string="MES API Key")
    mes_login_url = fields.Char(string="登录地址")
    type = fields.Selection([('mes', 'MES')], default='mes')
    mes_expiration_minutes = fields.Integer(string="过期时间")

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mes_api_key = fields.Char(
        string="MES API Key",
        config_parameter='mes_config.mes_api_key'
    )