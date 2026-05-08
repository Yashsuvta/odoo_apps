/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

const debugRegistry = registry.category("debug");

// =========================================================
// DYNAMIC FIELD CONFIGURATION
// =========================================================

function dynamicFieldConfiguration({ action, env }) {

    if (!action.res_model) {
        return null;
    }

    const description = _t("Dynamic Field Configuration");

    return {
        type: "item",
        description,

        callback: async () => {

            const modelId = (
                await env.services.orm.search(
                    "ir.model",
                    [["model", "=", action.res_model]],
                    {
                        limit: 1,
                    }
                )
            )[0];

            env.services.action.doAction({
                type: "ir.actions.act_window",

                name: description,

                res_model: "dynamic.field.config",

                views: [
                    [false, "list"],
                    [false, "form"],
                ],

                view_mode: "list,form",

                domain: [
                    ["model_id", "=", modelId]
                ],

                context: {
                    default_model_id: modelId,
                },

                target: "current",
            });
        },

        sequence: 125,
    };
}

// =========================================================
// REGISTER ONLY CUSTOM ITEM
// =========================================================

debugRegistry
    .category("action")
    .add(
        "dynamicFieldConfiguration",
        dynamicFieldConfiguration
    );