# -*- coding: utf-8 -*-

from odoo import api, fields, models

class MesUser(models.Model):
    _name = 'mes.user'
    _description = u'MES User'

    name = fields.Char(string="用户名称")
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="odoo 用户",
        )
    company_id = fields.Many2one('res.company', related='user_id.company_id', store=True, readonly=True)
    email = fields.Char(string="用户名")
    
    role_id = fields.Many2one(
        comodel_name='mes.role',
        string="角色"
    )
    session_id = fields.Char(string="Session ID")

    mes_jwt_token = fields.Char("MES JWT Token")
    mes_jwt_token_expire_time = fields.Datetime("MES JWT Token Expiry")

