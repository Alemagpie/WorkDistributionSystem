/** @odoo-module **/
import { registry } from "@web/core/registry"

registry.category("actions").add("action_print", (env, action) => {
    window.print();
});