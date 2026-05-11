/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useEffect } from "@odoo/owl";

const autoRefreshService = {
    start(env) {
        setInterval(() => {
            const actionService = env.services.action;
            const currentController = actionService.currentController;
            if (currentController?.jsId && 
                currentController?.action?.res_model === 'project.task') {
                env.services.action.restore(currentController.jsId);
            }
        }, 60000);  //Every 60s
    }
};

//Registers a service
registry.category("services").add("auto_refresh", autoRefreshService);