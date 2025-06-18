/** @odoo-module **/

import { ListRenderer } from "@web/views/list/list_renderer";
import { SearchBar } from "@web/search/search_bar/search_bar";
import { patch } from "@web/core/utils/patch";
import { Domain } from "@web/core/domain";
import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useBus } from "@web/core/utils/hooks";
import { DateTimePicker } from "@web/core/datetime/datetime_picker";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { serializeDate, serializeDateTime } from "@web/core/l10n/dates";
import { fuzzyTest } from "@web/core/utils/search";
import { _lt, _t } from "@web/core/l10n/translation";
import { KeepLast } from "@web/core/utils/concurrency";
import { AccordionItem } from "@web/core/dropdown/accordion_item";
import { CheckboxItem } from "@web/core/dropdown/checkbox_item";
import { useService } from "@web/core/utils/hooks";


const { DateTime } = luxon;

let field_date = [DateTime.local()];

const parsers = registry.category("parsers");
let previousTargetValue = null;
let selected_status = []
let previousBooleanValue = null;

const CHAR_FIELDS = ["char", "html", "many2many", "many2one", "one2many", "text",];
const FIELD_TYPES = {
  boolean: "boolean",
  char: "char",
  date: "date",
  datetime: "datetime",
  float: "number",
  id: "id",
  integer: "number",
  html: "char",
  many2many: "char",
  many2one: "char",
  monetary: "number",
  one2many: "char",
  text: "char",
  selection: "selection",
};

const FIELD_OPERATORS = {
  boolean: [
    { symbol: "=", description: _lt("is Yes"), value: true },
    { symbol: "!=", description: _lt("is No"), value: true },
  ],
  char: [
    { symbol: "ilike", description: _lt("contains") },
    { symbol: "not ilike", description: _lt("doesn't contain") },
    { symbol: "=", description: _lt("is equal to") },
    { symbol: "!=", description: _lt("is not equal to") },
    { symbol: "!=", description: _lt("is set"), value: false },
    { symbol: "=", description: _lt("is not set"), value: false },
  ],
  date: [
    { symbol: "=", description: _lt("is equal to") },
    { symbol: "!=", description: _lt("is not equal to") },
    { symbol: ">", description: _lt("is after") },
    { symbol: "<", description: _lt("is before") },
    { symbol: ">=", description: _lt("is after or equal to") },
    { symbol: "<=", description: _lt("is before or equal to") },
    { symbol: "between", description: _lt("is between") },
    { symbol: "!=", description: _lt("is set"), value: false },
    { symbol: "=", description: _lt("is not set"), value: false },
  ],
  datetime: [
    { symbol: "between", description: _lt("is between") },
    { symbol: "=", description: _lt("is equal to") },
    { symbol: "!=", description: _lt("is not equal to") },
    { symbol: ">", description: _lt("is after") },
    { symbol: "<", description: _lt("is before") },
    { symbol: ">=", description: _lt("is after or equal to") },
    { symbol: "<=", description: _lt("is before or equal to") },
    { symbol: "!=", description: _lt("is set"), value: false },
    { symbol: "=", description: _lt("is not set"), value: false },
  ],
  id: [{ symbol: "=", description: _lt("is") }],
  number: [
    { symbol: "=", description: _lt("is equal to") },
    { symbol: "!=", description: _lt("is not equal to") },
    { symbol: ">", description: _lt("greater than") },
    { symbol: "<", description: _lt("less than") },
    { symbol: ">=", description: _lt("greater than or equal to") },
    { symbol: "<=", description: _lt("less than or equal to") },
    { symbol: "!=", description: _lt("is set"), value: false },
    { symbol: "=", description: _lt("is not set"), value: false },
  ],
  selection: [
    { symbol: "=", description: _lt("is") },
    { symbol: "in", description: _lt("is in"), value: false },
    { symbol: "!=", description: _lt("is not") },
    { symbol: "!=", description: _lt("is set"), value: false },
    { symbol: "=", description: _lt("is not set"), value: false },
  ],
};

const formatters = registry.category("formatters");
var domain1 = "";
var domain2 = "";
function formatField(field, value) {
  if (FIELD_TYPES[field.type] === "char") {
    return value;
  }
  const type = field.type === "id" ? "integer" : field.type;
  const format = formatters.contains(type) ? formatters.get(type) : (v) => v;
  return format(value, { digits: field.digits });
}
let nextItemId = 1;
patch(ListRenderer.prototype, {
  setup() {
    super.setup();
    this.orm = useService("orm");
    this.rpc = useService("rpc");
    const fields = this.env.searchModel.searchViewFields;
    this.options_field = Object.values(this.env.searchModel.searchViewFields)
      .filter((field) => this.validateField(field))
      .concat({ string: "ID", type: "id", name: "id" })
      .sort(({ string: a }, { string: b }) => (a > b ? 1 : a < b ? -1 : 0));
    this.items = useState([]);
    this.subItems = {};
    this.keepLast = new KeepLast();
    this.OPERATORS = FIELD_OPERATORS;
    this.FIELD_TYPES = FIELD_TYPES;
    useBus(this.env.searchModel, "update", this.render);
    this.searchItems = this.env.searchModel.getSearchItems(
      (f) => f.type === "field"
    );

    console.log("columns", this.state.columns);

  },
  /**
   * @param {Object} field
   * @returns {boolean}
   */
  validateField(field) {
    return (
      !field.deprecated && field.searchable && FIELD_TYPES[field.type] && field.name !== "id"
    );
  },
  /**
  * @param {InputEvent} ev
  */
  onSearchBarInput(ev) {
    const query = ev.target.value;
    if (query.trim()) {
      this.searchComputeState({
        query,
        expanded: [],
        focusedIndex: 0,
        subItems: [],
      });
    } else if (this.items.length) {
      this.searchResetState();
    }
  },
  /**
 * @param {Object} [options={}]
 * @param {number[]} [options.expanded]
 * @param {number} [options.focusedIndex]
 * @param {string} [options.query]
 * @param {Object[]} [options.subItems]
 * @returns {Object[]}
 */
  async searchComputeState(options = {}) {
    const query = "query" in options ? options.query : this.state.query;
    const expanded = "expanded" in options ? options.expanded : this.state.expanded;
    const focusedIndex =
      "focusedIndex" in options ? options.focusedIndex : this.state.focusedIndex;
    const subItems = "subItems" in options ? options.subItems : this.subItems;
    const tasks = [];
    for (const id of expanded) {
      if (!subItems[id]) {
        tasks.push({ id, prom: this.computeSubItems(id, query) });
      }
    }
    const prom = this.keepLast.add(Promise.all(tasks.map((task) => task.prom)));
    if (tasks.length) {
      const taskResults = await prom;
      tasks.forEach((task, index) => {
        subItems[task.id] = taskResults[index];
      });
    }
    this.state.expanded = expanded;
    this.state.query = query;
    this.state.focusedIndex = focusedIndex;
    this.subItems = subItems;
    const trimmedQuery = this.state.query.trim();
    this.items.length = 0;
    if (!trimmedQuery) {
      return;
    }

    for (const searchItem of this.searchItems) {
      const field = this.fields[searchItem.fieldName];
      const type = field.fieldType === "reference" ? "char" : field.fieldType;
      /** @todo do something with respect to localization (rtl) */
      const preposition = _t(["date", "datetime"].includes(type) ? "at" : "for");
      if (["selection", "boolean"].includes(type)) {
        const options = field.selection || [
          [true, this.env._t("Yes")],
          [false, this.env._t("No")],
        ];
        for (const [value, label] of options) {
          if (fuzzyTest(trimmedQuery.toLowerCase(), label.toLowerCase())) {
            this.items.push({
              id: nextItemId++,
              searchItemDescription: searchItem.description,
              preposition,
              searchItemId: searchItem.id,
              label,
              /** @todo check if searchItem.operator is fine (here and elsewhere) */
              operator: searchItem.operator || "=",
              value,
            });
          }
        }
        continue;
      }

      const parser = parsers.contains(type) ? parsers.get(type) : (str) => str;
      let value;
      try {
        switch (type) {
          case "date": {
            value = serializeDate(parser(trimmedQuery));
            break;
          }
          case "datetime": {
            value = serializeDateTime(parser(trimmedQuery));
            break;
          }
          case "many2one": {
            value = trimmedQuery;
            break;
          }
          default: {
            value = parser(trimmedQuery);
          }
        }
      } catch (_e) {
        continue;
      }
      const item = {
        id: nextItemId++,
        searchItemDescription: searchItem.description,
        preposition,
        searchItemId: searchItem.id,
        label: this.state.query,
        operator:
          searchItem.operator || (CHAR_FIELDS.includes(type) ? "ilike" : "="),
        value,
      };
      if (type === "many2one") {
        item.isParent = true;
        item.isExpanded = this.state.expanded.includes(item.searchItemId);
      }
      this.items.push(item);
      if (item.isExpanded) {
        this.items.push(...this.subItems[searchItem.id]);
      }
    }
  },
  searchResetState() {
    this.searchComputeState({
      expanded: [],
      focusedIndex: 0,
      query: "",
      subItems: [],
    });
  },
  /**
 * @param {KeyboardEvent} ev
 */
  async onSearchBarKeydown(ev) {
    switch (ev.key) {
      case "Enter":
        if (ev.target.value !== previousTargetValue || previousTargetValue === null) {
          previousTargetValue = ev.target.value;
          const preFilters = this.items.map((condition) => {
            let id = ev.target.id;
            if (this.env.searchModel.resModel === "res.partner" && ev.target.id === "display_name"){
              id ="complete_name";
            }
            if (this.fields.hasOwnProperty(id)) {
              const field = this.fields[id];
              const genericType = this.FIELD_TYPES[field.type];
              const operator = this.OPERATORS[genericType][0];
              const descriptionArray = [
                field.string,
                operator.description.toString(),
              ];
              const domainArray = [];
              let domainValue;
              if ("value" in operator) {
                domainValue = [operator.value];
              } else if (["date", "datetime"].includes(genericType)) {
                const serialize = genericType === "date" ? serializeDate : serializeDateTime;
                condition.value = this.date
                domainValue = condition.value.map(serialize);
                descriptionArray.push(
                  `"${condition.value
                    .map((val) => formatField(field, val))
                    .join(" " + this.env._t("and") + " ")}"`
                );
              } else {
                if (ev.target.value != condition.value) { condition.value = ev.target.value }
                domainValue = [condition.value];
                descriptionArray.push(`"${condition.value}"`);
              }
              if (ev.target.value != domainValue[0]) {
                domainValue[0] = ev.target.value
              }
              if (operator.symbol === "between") {
                domainArray.push(
                  [field.name, ">=", domainValue[0]],
                  [field.name, "<=", domainValue[1]]
                );
              } else {
                domainArray.push([field.name, operator.symbol, domainValue[0]]);
              }

              if (this.env.searchModel.resModel === "res.partner" && ev.target.value === "display_name"){
                descriptionArray[0] = 'Name'
              }
              const preFilter = {
                description: descriptionArray.join(" "),
                domain: new Domain(domainArray).toString(),
                type: 'filter',
              };
              return preFilter;
            }
          });
          if (preFilters.length > 0) {
            const filter = [preFilters[0]];
            this.env.searchModel.createNewFilters(filter);
          }
        }
        break;
      case "Backspace":
        for (const field_facet of this.env.searchModel.facets) {
          const match = field_facet.values[0].match(/"([^"]+)"/);
          if (match && ev.target.value === match[1]) {
            this.removeFacet(field_facet);
            previousTargetValue = null;
          }
        }
        break;
    }

  },
  /**
  * @param {Object} facet
  */
  removeFacet(facet) {
    this.env.searchModel.deactivateGroup(facet.groupId);
  },


  /**
       * @param {Name} name
       * @param {Event} ev
  */

  onDateChange(name, ev) {
    var datetime = ev.target.value;
    if (datetime) {
      field_date = [datetime];
      if (this.fields.hasOwnProperty(name)) {
        const field = this.fields[name];
        const genericType = this.FIELD_TYPES[field.type];
        let operator = this.OPERATORS[genericType][0];
        if (genericType === "datetime") {
          operator = this.OPERATORS[genericType][1];
        }
        const descriptionArray = [
          field.string,
          operator.description.toString(),
        ];
        const domainArray = [];
        var date = field_date.toString();
        var parts = date.split('-');
        var year = parts[0];
        var month = parts[1];
        var day = parts[2];

        let domainValue;
        if (["date"].includes(genericType)) {
          var formattedDate = '\"' + month + '/' + day + '/' + year + '\"';
          domainValue = [field_date];
          descriptionArray.push(formattedDate);
        }
        if (operator.symbol === "between") {
          domainArray.push(
            [field.name, ">=", domainValue[0]],
            [field.name, "<=", domainValue[1]]
          );
        } else {
          domainArray.push([field.name, operator.symbol, domainValue[0]]);
        }
        const preFilter = [{
          description: descriptionArray.join(" "),
          domain: new Domain(domainArray).toString(),
          type: 'filter',
        }];
        this.env.searchModel.createNewFilters(preFilter);
      }
    }
    else{
      const facets = this.env.searchModel.facets[0];
      this.removeFacet(facets);
    }
  },

  /**
       * @param {Name} name
       * @param {Event} ev
  */
  onDateTimeChange(name, ev) {
    var datetime = ev.target.value;
    var datevalue = datetime.split('T')[0];
    var timevalue = datetime.split('T')[1];

    if (datetime) {
      field_date = [datevalue];
      if (this.fields.hasOwnProperty(name)) {
        const field = this.fields[name];
        const genericType = this.FIELD_TYPES[field.type];
        let operator = this.OPERATORS[genericType][0];
        if (genericType === "datetime") {
          operator = this.OPERATORS[genericType][1];
        }
        const descriptionArray = [
          field.string,
          operator.description.toString(),
        ];
        const domainArray = [];
        var date = field_date.toString();
        var parts = date.split('-');
        var year = parts[0];
        var month = parts[1];
        var day = parts[2];

        // Format the date string

        let domainValue;
        if (["datetime"].includes(genericType)) {
          var formattedDate = '\"' + month + '/' + day + '/' + year + ' ' + timevalue + '\"';
          var datetimevalue = field_date + ' ' + timevalue
          domainValue = [datetimevalue];
          descriptionArray.push(formattedDate);
        }
        if (operator.symbol === "between") {
          domainArray.push(
            [field.name, ">=", domainValue[0]],
            [field.name, "<=", domainValue[1]]
          );
        } else {
          domainArray.push([field.name, operator.symbol, domainValue[0]]);
        }
        const preFilter = [{
          description: descriptionArray.join(" "),
          domain: " [(\"create_date\", \"=\", \"2024-02-01 05:42:22\")]",
          type: 'filter',
        }];
        this.env.searchModel.createNewFilters(preFilter);
      }
    }
  },
  /**
   * @param {Name} name
   * @param {Event} ev
   */
  onValueChange(name, ev) {
    const selectedvalue = ev.target.value;
    const selectedname = name.name;

    if (!selected_status.includes(selectedvalue) || selected_status.length === 0) {
      // If selectedvalue is not already in the selected_status array or the array is empty
      selected_status.push(selectedvalue);
      if (this.fields.hasOwnProperty(selectedname)) {
        const field = this.fields[selectedname];
        const genericType = this.FIELD_TYPES[field.type];
        const operator = this.OPERATORS[genericType][1];
        const descriptionArray = [
          field.string,
          operator.description.toString()
        ];
        const domainArray = [];
        let domainValue;
        domainValue = [selected_status];

        if (field.type === "selection") {
          if (selected_status.length >= 2) {
            const selectedStatusString = selected_status.map(status => `"${status}"`).join(" or ");
            descriptionArray.push(`[${selectedStatusString}]`);
          }
          else {
            descriptionArray.push(
              `"${field.selection.find((v) => selected_status.includes(v[0]))[1]}"`
            );
          }
        } else {
          descriptionArray.push(`"${selectedvalue}"`)
        }

        if (operator.symbol === "between") {
          domainArray.push(
            [field.name, ">=", domainValue[0]],
            [field.name, "<=", domainValue[1]]
          );
        } else {
          domainArray.push([field.name, operator.symbol, selected_status]);
        }

        const des_facet = descriptionArray.join(" ");
        const facets = this.env.searchModel.facets[0];
        this.removeFacet(facets);

        const preFilter = [{
          description: descriptionArray.join(" "),
          domain: new Domain(domainArray).toString(),
          type: 'filter',
        }];
        this.env.searchModel.createNewFilters(preFilter);
      }
    }
  },

  /**
       * @param {Name} name
       * @param {Event} ev
       */
  async onBooleanFieldChange(name, ev) {

    const selectedvalue = ev.target.value;
    if (selectedvalue === ""){
      for (const field_facet of this.env.searchModel.facets) {
        if( name.label === field_facet.values[0].split(" is ")[0]){
          this.removeFacet(field_facet);
          previousBooleanValue = null;
        }
      }
    }
    else {
      const selectedname = name.name;
      if (previousBooleanValue === selectedname) {
        for (const field_facet of this.env.searchModel.facets) {
          if( name.label === field_facet.values[0].split(" is ")[0]){
            this.removeFacet(field_facet);
            previousBooleanValue = null;
          }
        }
      }
      if (previousBooleanValue !== selectedname || previousBooleanValue === null) {
        previousBooleanValue = selectedname;
        if (this.fields.hasOwnProperty(selectedname)) {
          const field = this.fields[selectedname];
          const genericType = this.FIELD_TYPES[field.type];
          let operator = this.OPERATORS[genericType];
          if (selectedvalue === 'false') {
            operator = operator[1]
          }
          if (selectedvalue === 'true') {
            operator = operator[0]
          }
          const descriptionArray = [field.string, operator.description.toString(),];
          const domainArray = [];
          let domainValue = [selectedvalue];
          descriptionArray.push(`"${selectedvalue}"`);
          domainArray.push([field.name, operator.symbol, domainValue[0]]);
          const preFilter = [{
            description: descriptionArray.join(" "),
            domain: new Domain(domainArray).toString(),
            type: 'filter',
          }];
          this.env.searchModel.createNewFilters(preFilter);
        }
      }
    }
  },

  /**
    * @param {Object} facet
    */
  removeFacet(facet) {
    if (facet) {
      this.env.searchModel.deactivateGroup(facet.groupId);
    }

  },

  createsearchView(){
    var model = this.env.searchModel.resModel;
    var columns = this.state.columns;
    var validColumns = columns.filter(column => column.field && column.field.supportedTypes && column.field.supportedTypes[0] === 'datetime');
    var datetime_columns = validColumns.map(column => column.name);
    var filter_items = this.env.searchModel.getSearchItems(searchItem =>
      searchItem.type === 'dateFilter'
    );
    var filter_item_names = filter_items.map(filter_item => filter_item.fieldName);
    var arraysEqual = datetime_columns.length === filter_item_names.length && datetime_columns.every((value, index) => value === filter_item_names[index]);

    if (!arraysEqual) {
      var extraElementsInDatetimeColumns = datetime_columns.filter(element => !filter_item_names.includes(element));
      if (extraElementsInDatetimeColumns.length > 0) {
        this.rpc('/create_search_view', {
          extra_elements: extraElementsInDatetimeColumns,
          model: model
        });
      }
      var filter_items = this.env.searchModel.getSearchItems(searchItem =>
        searchItem.type === 'dateFilter');
      var unique_filter_items = [];
      var seen_fieldNames = new Set();
      for (var filter_item of filter_items) {
        if (!seen_fieldNames.has(filter_item.fieldName)) {
          unique_filter_items.push(filter_item);
          seen_fieldNames.add(filter_item.fieldName);
        }
      }
      return unique_filter_items;
    }
  },

  get filterItems() {
    var items = this.createsearchView();
    return items
  },

  onFilterSelected({ itemId, optionId }) {

    if (optionId) {
      this.env.searchModel.toggleDateFilter(itemId, optionId);
    }
  },
  /**
  * @param {Object} item
  */
  searchSelectItem(item) {
    if (!item.unselectable) {
      const { searchItemId, label, operator, value } = item;
      this.env.searchModel.addAutoCompletionValues(searchItemId, {
        label,
        operator,
        value,
      });
    }
    this.searchResetState();
  },
});

patch(SearchBar.prototype, {
  /**
  * @override
 * @param {Object} facet
 */
  removeFacet(facet) {
    this.env.searchModel.deactivateGroup(facet.groupId);
    this.inputRef.el.focus();
    const value_domain = facet.domain
    const jsonString = value_domain;
    const cleanedString = jsonString.replace(/[\[\]\(\)\\"]/g, '');
    const jsonArray = cleanedString.split(',');
    let firstElement = jsonArray[0].trim();
    if (this.env.searchModel.resModel === "res.partner" && firstElement === "complete_name"){
      firstElement = 'display_name';
    }
    const searchBar = document.getElementById(firstElement);
    selected_status = []
    previousBooleanValue = null;
    previousTargetValue = null;
    if (searchBar) {
      searchBar.value = '';
    }
  }
});
ListRenderer.template = "web.ListRenderer";
ListRenderer.components = {
  ...ListRenderer.components,
  DatePicker: DateTimePicker,
  Dropdown: Dropdown,
  AccordionItem: AccordionItem,
  CheckboxItem: CheckboxItem,
};