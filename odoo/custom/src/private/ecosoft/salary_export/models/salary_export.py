# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import api, fields, models


class SalaryExport(models.Model):
    _name = "salary.export"
    _description = "Export Salary in Text File"

    name = fields.Char(
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date = fields.Datetime(
        required=True,
        default=fields.Datetime.now,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date_transfer = fields.Date(
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    line_ids = fields.One2many(
        comodel_name="salary.export.line",
        inverse_name="export_id",
        copy=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    state = fields.Selection(
        [("draft", "Draft"), ("done", "Done")],
        string="Status",
        default="draft",
        readonly=True,
        copy=False,
        index=True,
    )

    @api.onchange("name")
    def _compute_line_ids(self):
        self.ensure_one()
        self.line_ids = False
        if self.name:
            employees = self.env["hr.employee"].search([])
            line_obj = self.env["salary.export.line"]
            lines = [{"employee_id": e.id} for e in employees]
            self.line_ids = [line_obj.new(line).id for line in lines]

    def action_draft(self):
        self.write({"state": "draft"})

    def action_done(self):
        self.write({"state": "done"})


class SalaryExportLine(models.Model):
    _name = "salary.export.line"
    _description = "Salary Export Line"

    export_id = fields.Many2one(
        comodel_name="salary.export",
        index=True,
        required=True,
        ondelete="cascade",
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        required=True,
    )
    acc_number = fields.Char(
        related="employee_id.bank_account_id.acc_number",
    )
    acc_holder_name = fields.Char(related="employee_id.bank_account_id.acc_holder_name")
    amount = fields.Float(
        string="Salary Amount",
    )
