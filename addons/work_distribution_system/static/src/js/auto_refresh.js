/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, xml, onMounted, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

//Refreshes the kanban or the list every 30s by finding the current view and switching to it
// (bus events won't work for some reason)
class AutoRefreshComponent extends Component {
    static template = xml`<div/>`;

    setup() {
        const actionService = useService("action");

        onMounted(() => {
            this.interval = setInterval(async () => {
                try {
                    const controller = actionService.currentController;
                    if (!controller) return;
                    if (controller?.action?.res_model !== 'project.task') return;

                    const viewType = controller?.view?.type;
                    if (!viewType) return;

                    //console.log("Refreshing via switchView:", viewType);
                    await actionService.switchView(viewType);
                    //console.log("Refreshed");
                } catch(e) {
                    console.error("Refresh error:", e);
                }
            }, 30000);
        });

        onWillUnmount(() => {
            clearInterval(this.interval);
        });
    }
}

registry.category("systray").add("auto_refresh_component", {
    Component: AutoRefreshComponent,
});