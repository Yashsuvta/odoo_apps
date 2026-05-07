from odoo import fields, models, api
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'

    timer_start_time = fields.Datetime(string="Start Time")
    timer_end_time = fields.Datetime(string="End Time")
    timer_on = fields.Boolean(string="Timer Onn")
    timer_user_id = fields.Many2one('res.users', string="Timer User")
    has_active_timer = fields.Boolean(compute='_compute_user_timer_status')
    timer_line_ids = fields.One2many('task.timer.line', 'task_id', string='Timer Lines')
    is_done_stage = fields.Boolean(string="Is Done Stage", compute="_compute_is_done_stage", store=True)
    user_timer_start = fields.Datetime(string="Timer Start")
    user_skill_ids = fields.Many2many('res.partner', string="Skills")


   
    @api.depends('stage_id.name')
    def _compute_is_done_stage(self):
        for task in self:
            if task.stage_id.name == "Done":
                task.is_done_stage = True
            else:
                task.is_done_stage = False

    def _compute_user_timer_status(self):
        current_user = self.env.user
        for task in self:
            timer_line = self.env['task.timer.line'].search([
                ('task_id', '=', task.id),
                ('user_id', '=', current_user.id),
                ('timer_on', '=', True)
            ], limit=1)
            task.has_active_timer = bool(timer_line)

    def start_timer(self):
        current_user = self.env.user
        for task in self:
            if current_user.id not in task.user_ids.ids:
                raise UserError("You must be assigned to this task to start the timer.")

            # Check if the user has any other active timers
            active_timer = self.env['task.timer.line'].search([
                ('user_id', '=', current_user.id),
                ('timer_on', '=', True)
            ], limit=1)

            if active_timer:
                raise UserError(f"You already have an active timer on task: '{active_timer.task_id.name}'.")

            # Create new timer line
            self.env['task.timer.line'].create({
                'task_id': task.id,
                'user_id': current_user.id,
                'timer_start_time': fields.Datetime.now(),
                'timer_on': True,
            })
            self.write({
            'user_timer_start': fields.Datetime.now(),
            'has_active_timer': True,
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }



                
    def stop_timer(self):
        current_user = self.env.user
        for task in self:
            # Find the active timer line for this user on this task
            timer_line = self.env['task.timer.line'].search([
                ('task_id', '=', task.id),
                ('user_id', '=', current_user.id),
                ('timer_on', '=', True),
            ], limit=1)

            if not timer_line:
                raise UserError("No active timer found for you on this task.")

            timer_line.timer_end_time = fields.Datetime.now()

            if timer_line.timer_start_time >= timer_line.timer_end_time:
                raise UserError("End time must be after start time.")

            delta = timer_line.timer_end_time - timer_line.timer_start_time
            total_seconds = delta.total_seconds()
            duration_float = total_seconds / 3600.0
            duration_str = f"{int(total_seconds // 3600)}h {int((total_seconds % 3600) // 60)}m"

            # Create analytic line for this user's work
            self.env['account.analytic.line'].create({
                'name': f"Work on task: {task.name} ({duration_str})",
                'task_id': task.id,
                'project_id': task.project_id.id,
                'user_id': current_user.id,
                'date': fields.Date.context_today(self),
                'unit_amount': duration_float,
            })

            # Reset the timer line
            timer_line.timer_on = False
            self.write({
            'has_active_timer': False,
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.model
    def check_user_timer(self):
        active_timer = self.env['task.timer.line'].search([
                ('user_id', '=', self.env.uid),
                ('timer_on', '=', True)
            ], limit=1)
        if active_timer:
            return {
                'has_timer': True,
                'task_id': active_timer.task_id.id,
            }
        return {'has_timer': False}

    @api.model
    def stop_user_timer(self):
        active_timer = self.env['task.timer.line'].search([
                ('user_id', '=', self.env.uid),
                ('timer_on', '=', True)
            ], limit=1)
        if active_timer:
            active_timer.task_id.stop_timer()
        return True



class TaskTimerLine(models.Model):
    _name = 'task.timer.line'
    _description = 'Task Timer Line'
    

    task_id = fields.Many2one('project.task', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', required=True)
    timer_start_time = fields.Datetime()
    timer_end_time = fields.Datetime()
    timer_on = fields.Boolean(default=False)
