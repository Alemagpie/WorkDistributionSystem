{
    'name': 'Work Distribution System',
    'technical-name': 'work_distribution_system',
    'version': '1.0',
    'depends': ['project', 'hr'],  
    'author': 'Alessio Fagnani (UNIPD)',
    'description': 'Custom extension of project tasks',
    'data': [
        'views/task_views.xml',
        'data/archive_tasks_cron.xml',
        'data/delete_tasks_cron.xml',
        'data/response_template_it.xml',
        'data/response_template_en.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'work_distribution_system/static/src/img',
            #'work_distribution_system/static/src/js/auto_refresh.js',
            'work_distribution_system/static/src/css/main.css'
        ]
    },
    'installable': True,
    'auto_install': False,
}