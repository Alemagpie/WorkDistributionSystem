/** @odoo-module **/
import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";

patch(FormController.prototype, "work_distribution_system.task_mark_read", {
    async onWillStart() {
        await super.onWillStart();
        console.log("onWillStart fired, model:", this.props.resModel, "id:", this.props.resId);
        if (this.props.resModel === "project.task" && this.props.resId) {
            console.log("Calling action_mark_as_read...");
            const wasUnread = await this.orm.call(
                "project.task",
                "mark_read",
                [[this.props.resId]]
            );
            console.log("wasUnread:", wasUnread);
        }
    }
});