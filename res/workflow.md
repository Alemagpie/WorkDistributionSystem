Email -> Task:
- Email arriva
- Ogni 30s l'applicazione fa un fetch dell'IMAP
- Un parsing avviene sulla mail: corpo, oggetto e allegati sono letti
- Nel db è aggiunta una nuova task con stato "nuovo"
- Dopo x ore dall'assegnazione allo stato "completato", il lavoro è rimosso dalla vista e rimane nel db


Useful resources:
https://www.odoo.com/documentation/16.0/
https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html
https://www.odoo.com/documentation/19.0/applications/studio/fields.html#studio-fields-simple-fields
https://learnopenerp.blogspot.com/2020/05/how-to-create-scheduled-action-in-odoo.html

Useful commands:
docker compose up -d
docker compose restart odoo
docker logs -f odoo_app
docker compose down