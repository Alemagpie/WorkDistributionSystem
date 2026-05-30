from odoo import models

class Project(models.Model):
    _inherit = 'project.project'

    def open_bin(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cestino',
            'res_model': 'project.task',
            'view_mode': 'list,form',
            'domain': [('is_deleted', '=', True)],
            'context': {'show_deleted': True},
            'views': [(self.env.ref('work_distribution_system.project_task_bin_list').id, 'list'), (False, 'form')],
        }