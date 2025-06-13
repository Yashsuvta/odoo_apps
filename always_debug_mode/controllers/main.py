from odoo import http
from odoo.http import request

from odoo.addons.web.controllers import home

DEBUG_STATES = ["1", "true", "assets", "tests"]


class DebugModeController(home.Home):
    def _set_debug_mode(self):
        uid = request.session.uid
        if not uid:
            return

        if (
            request.env["res.users"].has_always_debug_mode(uid)
            and request.session.debug not in DEBUG_STATES
        ):
            request.session.debug = "1"
            request.params["debug"] = "1"

    @http.route("/web", type="http", auth="none")
    def web_client(self, s_action=None, **kw):
        self._set_debug_mode()
        return super(DebugModeController, self).web_client(s_action=s_action, **kw)
