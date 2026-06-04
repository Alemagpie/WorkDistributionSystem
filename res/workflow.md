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
https://www.odoo.com/it_IT/forum/assistenza-1/creating-automatic-scheduled-job-to-archive-tasks-199693
https://linuxize.com/post/how-to-setup-automatic-odoo-backup/

Useful commands:
docker compose up -d
docker compose restart odoo
docker logs -f odoo_app
docker compose down
docker exec -it odoo_db psql -U odoo -c "DROP DATABASE restore_test;"
docker exec -it odoo_db psql -U odoo -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'restore_test';"
docker logs odoo_app --tail=50

#Fields:
    #id (from id)                       ✔

    #status (from stage_id)             ✔
    #priority                           ✔
    #deadline (from date_deadline)      ✔
    #department (0,1)                   X

    #arrive date                        ✔
    #creation date (from create_date)   ✔
    #last update (from write_time)      ✔

    #sender                             ✔
    #object                             ✔
    #body                               ✔
    #attachments                        ✔

#Functions:
    #Delete
    #Archive
    #Automatic response (it)
    #Automatic response (eng)


CLOUDFLARED:
cloudflared.exe service install eyJhIjoiZmQ5YWU4MjJkNjc4Mzc3NGEyMTU5YTBmMWYwZDI4MWMiLCJ0IjoiNWY1MmZmODMtMzQyOC00NTRjLWI5ZWEtMDJiZDM0YzAzYzQ5IiwicyI6Ik56STNNMkppWWpFdE5UVmtOaTAwT0RjeUxUZzVNRFl0TkRka01tRTBNR0U1TkRrNSJ9

cloudflared tunnel --url http://localhost:8069

cloudflared service uninstall


Alla pagina localhost:8069/web/database/manager si possono creare manualmente backup e/o caricarne.
Una volta caricato un backup con nome DIVERSO dal db di prod, fare il log-out e selezionare il db che si vuole ispezionare premendo "Gestione database, per poi fare il log-in.


AGGIUNGERE AI DOCS:
- come inviare mail ✔
- messaggi interni  ✔
- le risposte vengono aggiunte alla task originale e ai log ✔
- come aumentare font ✔
- cestino ✔
- parole filtro ✔