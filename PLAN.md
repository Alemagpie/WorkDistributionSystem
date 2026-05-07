- Setup IMAP    ✔
- Definizione workflow email    ✔
- Modulo custom (estensione di Project)     
    1) Fetching
    2) Parsing
- Attachment handling
- Cron remove (remove tasks from view after a while)
- Extra functions
    1) Archive
    2) Delete
    3) Send response (it)
    4) Send response (eng)
- Protocol connections (TCP, ...)
- Backup
    1) DB dump
    2) restore test
- LAN porting
- Mobile support
- Users
- Assignment logic
- Automation 
    1) defaults
    2) auto-routing
    3) notifications
- Field tests
- Legacy migration
- Refactor and optimization
- Docs


Useful resources:
https://www.odoo.com/documentation/16.0/
https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html
https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html
https://www.odoo.com/documentation/19.0/applications/studio/fields.html#studio-fields-simple-fields
https://learnopenerp.blogspot.com/2020/05/how-to-create-scheduled-action-in-odoo.html
https://learnopenerp.blogspot.com/2020/05/how-to-create-scheduled-action-in-odoo.html


Useful commands:
docker compose up -d
docker compose restart odoo
docker logs -f odoo_app
docker compose down