/** @odoo-module **/
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { registry } from "@web/core/registry";
import { STATIC_ACTIONS_GROUP_NUMBER } from "@web/search/action_menus/action_menus";
import { _t } from "@web/core/l10n/translation";
import { Component } from "@odoo/owl";

const cogMenuRegistry = registry.category("cogMenu");

export class CopyToClipboard extends Component {
  static template = "web.CopyToClipboard";
  static components = { DropdownItem };

  onCopyToClipboard() {
    var listRecords = document.getElementsByClassName("o_list_table");
    var rows = listRecords[0].getElementsByTagName("tr");
    var records = [];
    var headerCells = rows[0].getElementsByTagName("th");
    var fieldNames = [];
    for (var k = 0; k < headerCells.length; k++) {
      fieldNames.push(headerCells[k].innerText);
    }
    var startIndex = 0;
    while (startIndex < fieldNames.length && fieldNames[startIndex].trim() === "") {
        startIndex++;
    }
    var endIndex = fieldNames.length - 1;
    while (endIndex >= 0 && fieldNames[endIndex].trim() === "") {
        endIndex--;
    }
    fieldNames = fieldNames.slice(startIndex, endIndex + 1);
    const concatenatedFieldNames = fieldNames.join("\t") + "\t";
    records.push(concatenatedFieldNames);
    var previousRecordLength = null; // Variable to store the length of the previous record

    for (var i = 1; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        var record = [];
        for (var j = 0; j < cells.length; j++) {
            var cellText = cells[j].innerText.replace(/\n/g, ",");
            record.push(cellText);
        }
        var recordStartIndex = 0;
        while (recordStartIndex < record.length && record[recordStartIndex].trim() === "") {
            recordStartIndex++;
        }
        var recordEndIndex = record.length - 1;
        while (recordEndIndex >= 0 && record[recordEndIndex].trim() === "") {
            recordEndIndex--;
        }
        record = record.slice(recordStartIndex, recordEndIndex + 1);

        // Check if the previousRecordLength is null or if the current record length matches the previous record length
        if (previousRecordLength === null || record.length === previousRecordLength) {
            var hasNonEmptyElements = record.some(text => text.trim() !== "");
            if (hasNonEmptyElements) {
                records.push(record.join("\t"));
            }
        }
        // Update the previousRecordLength for the next iteration
        previousRecordLength = record.length;
    }
    var copiedData = records.join("\n");
    var tempInput = document.createElement('textarea');
    tempInput.value = copiedData;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);

    var recordCount = records.length - 1;
    var message = _t("Copied ") + recordCount + " " + _t("record(s)") + " " + _t("to the clipboard");
    alert(message);
  }
}

const copyToClipboardItem = {
  Component: CopyToClipboard,
  groupNumber: STATIC_ACTIONS_GROUP_NUMBER,
  isDisplayed: async (env) => true,
};
cogMenuRegistry.add("copy-to-clipboard-menu", copyToClipboardItem, { sequence: 20 });