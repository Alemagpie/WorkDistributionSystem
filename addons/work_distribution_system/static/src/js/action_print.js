/** @odoo-module **/
import { registry } from "@web/core/registry"

//Adds a custom action to the odoo registry
registry.category("actions").add("action_print", (env, action) => {
    window.print();
});