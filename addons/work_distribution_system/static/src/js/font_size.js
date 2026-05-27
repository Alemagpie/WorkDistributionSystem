/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { xml } from "@odoo/owl";

class FontSizeWidget extends Component {
    static template = xml`
        <div style="display:flex; align-items:center; gap:4px; padding: 0 8px;">
            <button t-on-click="decrease" title="Diminuisci font" class="btn btn-sm btn-light">-</button>
            <button t-on-click="reset" title="Resetta font" class="btn btn-sm btn-light">R</button>
            <button t-on-click="increase" title="Aumenta font" class="btn btn-sm btn-light">+</button>
        </div>
    `;

    setup() {
        this.state = useState({ 
            fontSize: parseInt(localStorage.getItem('odoo_font_size') || '12')
        });
        this.applyFontSize(this.state.fontSize);
    }

    applyFontSize(size) {
        document.documentElement.style.fontSize = size + 'px';
        localStorage.setItem('odoo_font_size', size);
    }

    increase() {
        this.state.fontSize = Math.min(this.state.fontSize + 1, 30);
        this.applyFontSize(this.state.fontSize);
    }

    decrease() {
        this.state.fontSize = Math.max(this.state.fontSize - 1, 10);
        this.applyFontSize(this.state.fontSize);
    }

    reset() {
        this.state.fontSize = 12;
        this.applyFontSize(12);
    }
}

registry.category("systray").add("font_size_widget", {
    Component: FontSizeWidget,
});