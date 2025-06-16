/** @odoo-module **/

import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { routeToUrl } from "@web/core/browser/router";
import { patch } from "@web/core/utils/patch";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { _t } from "@web/core/l10n/translation";  // Import _t for translations

const userMenuRegistry = registry.category("user_menuitems");

patch(UserMenu.prototype, {
    setup() {
        super.setup();
        userMenuRegistry.remove("documentation");
        userMenuRegistry.remove("support");
        userMenuRegistry.remove("odoo_account");
        userMenuRegistry.add("debug", debugItem)
            .add("separator0", separator8)  // Add separator8 here
            .add("documentation", documentationItem)
            .add("support", supportItem);
    },
});

function debugItem(env) {
    const router = env.services.router;
    const url_debug = new URL(window.location.href);
    url_debug.searchParams.set('debug', '1');  // Set debug=1 for activation

    if (window.location.href.indexOf('debug=1') > -1) {
        // Deactivate developer mode
        return {
            type: "item",
            description: _t("Deactivate the developer mode"),
            callback: () => {
                const route = router ? router.current : null;
                console.log(route); // Log the route to debug

                if (route) {
                    // Remove the debug parameter to deactivate
                    route.search.debug = undefined;
                    browser.location.href = browser.location.origin + routeToUrl(route);
                } else {
                    // Fallback logic if router is unavailable
                    // Manually remove the debug parameter and reload
                    url_debug.searchParams.delete('debug');
                    window.location.href = url_debug.toString();
                }
            },
            sequence: 7,
        };
    } else {
        // Activate developer mode
        return {
            type: "item",
            id: "debug",
            description: _t("Activate the developer mode"),
            href: url_debug.toString(),
            callback: () => {
                browser.open(url_debug.toString(), "_self");
            },
            sequence: 5,
        };
    }
}



function separator8() {
    return {
        type: "separator",
        sequence: 8,
    };
}

function documentationItem(env) {
    // const _t = env.services.translation._t;  // Get the translation service
    const documentationURL = "https://www.odoo.com/documentation/18.0"; // Updated to v18 documentation
    return {
        type: "item",
        id: "documentation",
        description: _t("Documentation"),  // Use _t here
        href: documentationURL,
        callback: () => {
            browser.open(documentationURL, "_blank");
        },
        sequence: 10,
    };
}

function supportItem(env) {
    // const _t = env.services.translation._t;  // Get the translation service
    const url = session.support_url;
    return {
        type: "item",
        id: "support",
        description: _t("Support"),  // Use _t here
        href: url,
        callback: () => {
            browser.open(url, "_blank");
        },
        sequence: 20,
    };
}

