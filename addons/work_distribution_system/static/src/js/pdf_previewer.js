/** @odoo-module **/
import { Component, xml, useRef, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class PdfPreviewerWidget extends Component {
    static template = xml`
        <div class="pdf_previewer">
            <t t-foreach="props.pdfs" t-as="pdf" t-key="pdf.id">
                <div>
                    <p><b t-esc="pdf.name"/></p>
                    <iframe 
                        t-att-src="'/web/content/' + pdf.id + '?download=false'"
                        width="100%" 
                        height="500px"
                        style="border: 1px solid #ccc;">
                    </iframe>
                </div>
            </t>
        </div>
    `;

    static props = {
        pdfs: Array,
    };
}