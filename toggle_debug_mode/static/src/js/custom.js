/** @odoo-module **/

import { NavBar } from '@web/webclient/navbar/navbar';
import { patch } from '@web/core/utils/patch';

patch(NavBar.prototype, {
    setup() {
        super.setup();
        this.toggleDebugMode = this.toggleDebugMode.bind(this);
    },

    toggleDebugMode() {
        const url = new URL(window.location.href);
        if (url.searchParams.get('debug') === '1') {
            url.searchParams.delete('debug');
        } else {
            url.searchParams.set('debug', '1');
        }
        window.location.href = url.toString();
    },

    get debugIcon() {
        return window.location.href.includes('debug=1') ? 'fa-toggle-on' : 'fa-toggle-off';
    },

    get debugIconClass() {
        return `fa ${this.debugIcon} ${window.location.href.includes('debug=1') ? 'debug-on' : 'debug-off'}`;
    }
});
