/** @odoo-module **/

import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { registry } from "@web/core/registry";
import { archParseBoolean } from "@web/views/utils";
import { STATIC_ACTIONS_GROUP_NUMBER } from "@web/search/action_menus/action_menus";
import { _t } from "@web/core/l10n/translation";
import { jsonrpc } from "@web/core/network/rpc_service";
import { ExportDialog } from "../js/export_dialog";
import { Component } from "@odoo/owl";

const cogMenuRegistry = registry.category("cogMenu");
let filename = ''
/**
 * 'Export CSV' menu
 *
 * This component is used to export CSV the records for a particular model.
 * @extends Component
 */
export class ExportCsv extends Component {
    static template = "web.ExportCsv";
    static components = { DropdownItem };

    async onDirectExportCsv() {
        const resIds = await this.__owl__.parent.parent.parent.parent.parent.component.getSelectedResIds();
        const fields = this.__owl__.parent.parent.parent.parent.parent.component.props.archInfo.columns
            .filter((col) => col.type === "field")
            .map((col) => this.__owl__.parent.parent.parent.parent.parent.component.props.fields[col.name]);
        const exportFields = fields.map((field) => ({
            name: field.name,
            label: field.label || field.string,
        }));
        this.__owl__.parent.parent.parent.parent.parent.component.dialogService.add(ExportDialog, {
            title: _t("Export CSV"),
            context: exportFields,
            confirm: async () => {
                const selectedFields = [];
                const checkboxes = document.querySelectorAll(`#${'check'} input[type="checkbox"]`);
                checkboxes.forEach(item => {
                    if (item.checked === true) {
                        selectedFields.push({ name: item.name, label: item.value });
                    }
                });

                const data = await jsonrpc('/get_data', {
                    'model': this.__owl__.parent.parent.parent.parent.parent.component.model.root.resModel,
                    'res_ids': resIds.length > 0 && resIds,
                    'fields': selectedFields,
                    'grouped_by': this.__owl__.parent.parent.parent.parent.parent.component.model.root.groupBy,
                    'context': this.__owl__.parent.parent.parent.parent.parent.component.props.context,
                    'domain': this.__owl__.parent.parent.parent.parent.parent.component.model.root.domain,
                    'context': this.__owl__.parent.parent.parent.parent.parent.component.props.context,
                });
                if (data.filename){
                    filename = data.filename
                }
                const csv = this.convertToCsv(data, selectedFields);
                this.downloadCsv(csv);
            },
            cancel: () => { },
        });
    }

    /**
     * Convert data to CSV format
     * @param {Array|Object} data - Array of objects representing records or single object
     * @param {Array} fields - Array of selected fields metadata
     * @returns {String} CSV content
     */
    convertToCsv(data, fields) {
        const records = Array.isArray(data) ? data : [data];
        let csv = fields.map(field => field.label).join(',') + '\n';

        records.forEach(record => {
            record.data.forEach(record => {
                const csvRow = record.map(value => value || '').join(',');
                csv += csvRow + '\n';
            });
        });
        return csv;
    }
    /**
     * Download CSV file
     * @param {String} csv - CSV content
     */
    downloadCsv(csv) {
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

const exportCsvItem = {
    Component: ExportCsv,
    groupNumber: STATIC_ACTIONS_GROUP_NUMBER,
    isDisplayed: async (env) =>
        env.config.viewType === "list" &&
        !env.model.root.selection.length &&
        await env.model.user.hasGroup("base.group_allow_export") &&
        archParseBoolean(env.config.viewArch.getAttribute("export_csv"), true),
};
cogMenuRegistry.add("export-csv-menu", exportCsvItem, { sequence: 10 });