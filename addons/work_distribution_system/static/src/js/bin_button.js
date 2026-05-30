/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, xml, onMounted, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class BinButton extends Component {
    static template = xml`<div/>`;

    setup() {
        const actionService = useService("action");
        const orm = useService("orm");

        const injectButton_project = () => {
            const controller = actionService.currentController;
            if (controller?.action?.res_model !== 'project.task') return;
            if (controller?.view?.type !== 'kanban') return;

            // Don't inject twice
            if (document.getElementById('bin_button_injected')) return;

            const cpButtons = document.querySelector('.o_cp_buttons');
            if (!cpButtons) return;

            const btn = document.createElement('button');
            btn.id = 'bin_button_injected';
            btn.className = 'btn btn-secondary ms-2';
            btn.innerHTML = '<i class="fa fa-trash"></i> Cestino';
            btn.onclick = async () => {
                const result = await orm.call(
                    "project.task",
                    "open_bin",
                    [[]]
                );
                actionService.doAction(result);
            };
            cpButtons.appendChild(btn);
        };

        const injectButton_bin = () => {
            const controller = actionService.currentController;
            if (controller?.action?.res_model !== 'project.task') return;
            
            // Only inject in bin view (check if domain contains is_deleted)
            const domain = controller?.action?.domain;
            const isBinView = domain && JSON.stringify(domain).includes('is_deleted');
            if (!isBinView) return;

            if (document.getElementById('empty_bin_button_injected')) return;

            const cpButtons = document.querySelector('.o_cp_buttons');
            if (!cpButtons) return;

            const btn = document.createElement('button');
            btn.id = 'empty_bin_button_injected';
            btn.className = 'btn btn-danger ms-2';
            btn.innerHTML = '<i class="fa fa-trash"></i> Svuota cestino';
            btn.style.marginTop = '16px'
            btn.onclick = async () => {
                if (!confirm('Eliminare definitivamente tutti i task nel cestino?')) return;
                await orm.call('project.task', 'empty_bin', [[]]);
                // Refresh current view keeping breadcrumb
                const controller = actionService.currentController;
                if (controller?.jsId) {
                    await actionService.restore(controller.jsId);
                }
            };
            cpButtons.appendChild(btn);
        };

        onMounted(() => {
            // Try immediately and also after a short delay for initial load
            injectButton_project()
            injectButton_bin()

            this.interval = setInterval( () => {
                    injectButton_project()
                    injectButton_bin()
                },
                2000);
        });

        onWillUnmount(() => {
            clearInterval(this.interval);
            const btn = document.getElementById('bin_button_injected');
            if (btn) btn.remove();
        });
    }
}

registry.category("systray").add("bin_button", {
    Component: BinButton,
    sequence: 1,
});