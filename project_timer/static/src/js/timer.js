/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { KanbanRecord } from "@web/views/kanban/kanban_record";
import { useService } from "@web/core/utils/hooks";
import { useState, onMounted, onWillUpdateProps, onWillUnmount } from "@odoo/owl";

let intervalMap = {};
patch(KanbanRecord.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        const startTimer = () => {
            const recordId = this.props.record.resId;
            if (!this.props.record.data.has_active_timer) {
                return;
            }
            const timerEl = document.getElementsByClassName('Livetimerviwer')[0];
            const startTime = new Date(this.props.record.data.user_timer_start);
            function updateTimer() {
                const now = new Date();
                const elapsed = Math.floor((now - startTime) / 1000);
                const h = String(Math.floor(elapsed / 3600)).padStart(2, '0');
                const m = String(Math.floor((elapsed % 3600) / 60)).padStart(2, '0');
                const s = String(elapsed % 60).padStart(2, '0');
                timerEl.textContent = `${h}:${m}:${s}`;
                var valueToAppend =timerEl.textContent;
                const timerDiv = document.getElementsByClassName('Livetimerviwer')[0];
                if (timerDiv) {
                    timerDiv.innerHTML = valueToAppend; 
                    }
            }
            if (intervalMap[recordId]) {
                clearInterval(intervalMap[recordId]);
            }
            updateTimer(); 
            intervalMap[recordId] = setInterval(updateTimer, 1000);
        };
        
        onMounted(() => {
            startTimer(); 
        });

        onWillUpdateProps(() => {
            const recordId = this.props.record.resId;
            if (!this.props.record.data.has_active_timer && intervalMap[recordId]) {
                clearInterval(intervalMap[recordId]);
                delete intervalMap[recordId];
            } else if (this.props.record.data.has_active_timer) {
                startTimer(); 
            }
        });

        onWillUnmount(() => {
            const recordId = this.props.record.resId;
            if (intervalMap[recordId]) {
                clearInterval(intervalMap[recordId]);
                delete intervalMap[recordId];
            }
        });
    },

    async onClick(event) {
        const name = event.currentTarget.getAttribute("name");
        const recordId = this.props.record.resId;

        if (name === "start_timer") {
            await this.orm.call("project.task", "start_timer", [[recordId]]);
            await this.props.record.model.load();
            window.location.reload(); 
        }

        if (name === "stop_timer") {
            if (intervalMap[recordId]) {
                clearInterval(intervalMap[recordId]);
                delete intervalMap[recordId];
            }
            await this.orm.call("project.task", "stop_timer", [[recordId]]);
            await this.props.record.model.load();
        }
    },
});