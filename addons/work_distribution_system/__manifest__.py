{
    'name': 'Work Distribution System',
    'technical-name': 'work_distribution_system',
    'version': '1.0',
    'depends': ['project', 'hr', 'base_setup'],  
    'author': 'Alessio Fagnani (UNIPD)',
    'description': 'Custom extension of project tasks',
    'data': [
        'views/actions.xml',
        'views/task_list_customization.xml',
        'views/task_views.xml',
        'data/archive_tasks_cron.xml',
        'data/delete_tasks_cron.xml',
        'data/backup_cron.xml',
        'data/response_template_it.xml',
        'data/response_template_en.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'work_distribution_system/static/src/img',
            #'work_distribution_system/static/src/js/auto_refresh.js',
            'work_distribution_system/static/src/js/action_print.js',
            'work_distribution_system/static/src/js/font_size.js',
            'work_distribution_system/static/src/css/main.css',
            'work_distribution_system/static/src/css/print.css'
        ]
    },
    'installable': True,
    'auto_install': False,
}