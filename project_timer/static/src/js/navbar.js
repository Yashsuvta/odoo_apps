/** @odoo-module **/

import { NavBar } from '@web/webclient/navbar/navbar';
import { patch } from '@web/core/utils/patch';
import { onMounted, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

patch(NavBar.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.state = useState({
            hasActiveTimer: false,
        });        
        onMounted(this.checkTimer.bind(this));
    },
    async checkTimer() {      
        const res = await this.orm.call("project.task", "check_user_timer", []);
        if (res?.has_timer) {
            this.state.hasActiveTimer = true;
        }
    },

    async stopTimer() {
        await this.orm.call("project.task", "stop_user_timer", []);
        this.state.hasActiveTimer = false;
        window.location.reload();
    },
});
