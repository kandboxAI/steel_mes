import jwt
import datetime
from odoo import http
from odoo.http import request
from uuid import uuid4

from ..utils.jwt_utils import get_valid_token


class MesJWTLogin(http.Controller):

    @http.route('/mes/jwt/login', type='http', auth='user', website=False)
    def mes_jwt_login(self):
        user = request.env.user
        mes_config = request.env['mes.config'].sudo().search([('type', '=', 'mes')],limit=1)

        if not mes_config:
            return request.render('mes.config', {'error': '未设置mes config信息'})

        mes_login_url = mes_config.mes_login_url

        # mes_user = request.env['mes.user'].sudo().search([('user_id', '=', user.id)], limit=1)
        # if not mes_user:
        #     return request.render('web.login', {'error': '未绑定 MES 用户'})
        #
        # if not mes_user.session_id:
        #     mes_user.session_id = str(uuid4())
        #
        # payload = {
        #     "email": mes_user.email,
        #     "exp": datetime.datetime.now() + datetime.timedelta(minutes=EXPIRATION_MINUTES),
        #     "session_id": mes_user.session_id
        # }
        # token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        token = get_valid_token(user=user)

        print("mesloginurl",mes_login_url)

        redirect_url = f"{mes_login_url}?token={token}"
        print("redirect_url",redirect_url)
        return request.redirect(redirect_url,local=False)