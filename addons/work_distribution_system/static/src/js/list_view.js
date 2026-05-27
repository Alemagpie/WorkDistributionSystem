/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { RefreshListController } from "@<module_name>/tree_view/refresh_controller";

export const ListView = {
    ...listView,
    Controller: RefreshListController,
};

registry.category("views").add("refresh_list", ListView);