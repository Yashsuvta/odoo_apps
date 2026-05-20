/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FormRenderer } from "@web/views/form/form_renderer";
import { onMounted, onWillUnmount } from "@odoo/owl";

patch(FormRenderer.prototype, {

    setup() {

        super.setup();

        this.phoneValidationObserver = null;

        const applyValidation = (root = document) => {

            const inputs = root.querySelectorAll("input");

            inputs.forEach((input) => {

                // Avoid duplicate listeners
                if (input.dataset.phoneValidationApplied) {
                    return;
                }

                const fieldWidget = input.closest(".o_field_widget");

                if (!fieldWidget) {
                    return;
                }

                const html = fieldWidget.outerHTML;

                // Detect phone-related fields
                const isPhoneField =
                    html.includes('name="phone"') ||
                    html.includes('name="mobile"') ||
                    html.includes('name="work_phone"') ||
                    html.includes('name="private_phone"') ||
                    html.includes('name="emergency_phone"') ||
                    fieldWidget.classList.contains("o_field_phone");

                if (!isPhoneField) {
                    return;
                }

                input.dataset.phoneValidationApplied = true;

                // Restrict typing
                input.addEventListener("keydown", (ev) => {

                    const allowedKeys = [
                        "Backspace",
                        "Delete",
                        "ArrowLeft",
                        "ArrowRight",
                        "ArrowUp",
                        "ArrowDown",
                        "Tab",
                        "Home",
                        "End",
                        "Enter",
                    ];

                    if (ev.ctrlKey || ev.metaKey) {
                        return;
                    }

                    if (allowedKeys.includes(ev.key)) {
                        return;
                    }

                    const regex = /^[0-9+\-\s()]$/;

                    if (!regex.test(ev.key)) {

                        ev.preventDefault();
                    }

                });

                // Cleanup pasted values
                input.addEventListener("input", (ev) => {

                    const oldValue = ev.target.value;

                    const newValue = oldValue.replace(
                        /[^0-9+\-\s()]/g,
                        ""
                    );

                    if (oldValue !== newValue) {

                        ev.target.value = newValue;
                    }

                });

            });

        };

        onMounted(() => {

            // Initial validation
            applyValidation(document);

            // Observe dynamic notebook rendering
            this.phoneValidationObserver = new MutationObserver(
                (mutations) => {

                    mutations.forEach((mutation) => {

                        mutation.addedNodes.forEach((node) => {

                            if (node.nodeType === 1) {

                                applyValidation(node);

                            }

                        });

                    });

                }
            );

            this.phoneValidationObserver.observe(
                document.body,
                {
                    childList: true,
                    subtree: true,
                }
            );

        });

        onWillUnmount(() => {

            if (this.phoneValidationObserver) {

                this.phoneValidationObserver.disconnect();
            }

        });

    },

});