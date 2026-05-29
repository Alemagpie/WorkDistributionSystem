/** @odoo-module **/
import { registry } from "@web/core/registry";

const markReadService = {
    dependencies: ["orm", "action"],
    start(env, { orm, action }) {
        document.addEventListener("click", async (e) => {
            const kanbanCard = e.target.closest(".oe_kanban_global_click");
            if (kanbanCard) {
                const resId = parseInt(kanbanCard.dataset.id);
                if (resId) {
                    await orm.call("project.task", "mark_read", [[resId]]);
                }
            }
        });
    }
};

registry.category("services").add("mark_read_service", markReadService);