from odoo import fields, _
import datetime
import jwt
from uuid import uuid4
from odoo.exceptions import (
    UserError
)
# 替换成你自己的密钥
# JWT_SECRET_KEY = "duanqiyanghaibaoddduanqiyanghaibaoddduanqiyanghaibaoddd"
# JWT_EXPIRATION_MINUTES = 30

def get_jwt_mes_config(user):
    mes_config = user.env['mes.config'].sudo().search([('type', '=', 'mes')], limit=1)

    if not mes_config:
        return UserError(_("未设置 MES Config 信息"))
    return mes_config

def get_valid_token(user):
    mes_config = get_jwt_mes_config(user)

    jwt_secret_key = user.env['ir.config_parameter'].sudo().get_param('mes_config.mes_api_key')
    jwt_expiration_minutes= mes_config.mes_expiration_minutes

    now = fields.Datetime.now()
    mes_user = user.env['mes.user'].sudo().search([('user_id', '=', user.id)], limit=1)
    if not mes_user:
        raise UserError(_("未绑定 MES 用户"))

    if not mes_user.session_id:
        mes_user.session_id = str(uuid4())

    if mes_user.mes_jwt_token and mes_user.mes_jwt_token_expire_time > now:
        return mes_user.mes_jwt_token

    exp_time = now + datetime.timedelta(minutes=jwt_expiration_minutes)

    payload = {
        "email": mes_user.email,
        "exp": exp_time,
        "session_id": mes_user.session_id
    }

    token = jwt.encode(payload, jwt_secret_key, algorithm="HS256")

    mes_user.mes_jwt_token = token
    mes_user.mes_jwt_token_expire_time = exp_time
    return token