/** @odoo-module */

import { ListController } from "@web/views/list/list_controller";

import { onWillStart, onWillDestroy } from "@odoo/owl";

export class RefreshListController extends ListController {
    setup() {
        super.setup();
        this._interval = null;
        onWillStart(async () => {
            this._interval = setInterval(this.refreshData.bind(this), 5000);
        });
        onWillDestroy(() => {
            clearInterval(this._interval);
        });
    }
    async refreshData() {
        await this.model.root.load();
        this.render(true);
    }
}