/** @odoo-module **/
import { registry } from "@web/core/registry";

const autoRefreshService = {
    dependencies: ["bus_service", "action"],

    start(env, { bus_service, action }) {

        bus_service.addEventListener("notification", ({ detail: notifications }) => {

            for (const notif of notifications) {

                let channel, payload;

                // Case 1: array format
                if (Array.isArray(notif)) {
                    [channel, payload] = notif;
                }
                // Case 2: object format
                else if (notif.payload) {
                    channel = notif.payload.channel || notif.channel;
                    payload = notif.payload.message || notif.payload;
                }
                else {
                    channel = notif.channel;
                    payload = notif.message;
                }

                if (channel !== "task_update") continue;
                if (!payload || payload.type !== "task_created") continue;

                const currentController = action.currentController;

                if (currentController?.action?.res_model !== "project.task") continue;

                const currentProjectId =
                    currentController.model?.root?.resId ||
                    currentController.props?.context?.default_project_id;

                if (payload.project_id !== currentProjectId) continue;

                currentController.reload();
            }
        });

        bus_service.start();
    }
};

registry.category("services").add("auto_refresh", autoRefreshService);