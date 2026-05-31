/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, xml, onMounted, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class UnreadIcon extends Component {
    static template = xml`<div/>`;

    setup() {
        const actionService = useService("action");
        const orm = useService("orm");

        const injectUnreadIcons = async () => {
            const controller = actionService.currentController;
            if (!controller) return;
            if (controller?.action?.res_model !== 'project.task') return;
            if (controller?.view?.type !== 'kanban') return;

            // Log all card data to find record ID
            document.querySelectorAll('.o_kanban_record').forEach(card => {
                console.log("card dataset:", JSON.stringify(card.dataset));
                console.log("card attributes:", Array.from(card.attributes).map(a => `${a.name}=${a.value}`));
            });
        };

        onMounted(() => {
            this.interval = setInterval(async () => {
                await injectUnreadIcons();
            }, 3000);
        });

        onWillUnmount(() => {
            clearInterval(this.interval);
        });
    }
}

registry.category("systray").add("unread_icon_service", {
    Component: UnreadIcon,
    sequence: 2,
});