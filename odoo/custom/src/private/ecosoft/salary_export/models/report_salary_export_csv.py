# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import csv

import pytz

from odoo import _, models
from odoo.exceptions import UserError


class SalaryExportCSV(models.AbstractModel):
    _name = "report.report_csv.salary_export"
    _inherit = "report.report_csv.abstract"
    _description = "Salary Export to CSV"

    def generate_csv_report(self, writer, data, exports):
        tz = self.env.context.get("tz") or self.env.user.tz or "UTC"
        banks = self.env.user.partner_id.company_id.bank_ids.filtered(
            lambda l: l.bank_id.name == "Kasikorn Bank"
        )
        if not banks:
            raise UserError(_("No Kasikorn Bank in this company"))
        company_acc_holder_name = banks[0].acc_holder_name if banks else ""
        company_acc_number = banks[0].acc_number if banks else ""
        for obj in exports:
            total_amount = sum(obj.line_ids.mapped("amount"))
            tz_date = obj.date.astimezone(pytz.timezone(tz))
            obj_date = tz_date.strftime("%y%m%d")
            obj_time = tz_date.strftime("%H%M%S")
            obj_date_transfer = obj.date_transfer.strftime("%y%m%d")
            head_seq = "HPCTPCT{}{} {}".format(obj_date, obj_time, "000000")
            emp_count = len(obj.line_ids)
            # 1st line
            header = {
                "sequence": head_seq,
                "acc_number": company_acc_number.replace(" ", "").rjust(23),
                "amount": "{:.2f}".format(total_amount).replace(".", "").zfill(15),
                "date": obj_date,
                "space": "".rjust(23),
                "acc_holder_name": company_acc_holder_name.ljust(49),
                "date_transfer": "%s%s"
                % (obj_date_transfer, ("%sN" % emp_count).zfill(19)),
                "end": "".rjust(4),
            }
            writer.writerow(header)
            i = 0
            for line in obj.line_ids:
                i += 1
                acc_number, acc_holder_name = (
                    line.employee_id.bank_account_id.acc_number or "",
                    line.employee_id.bank_account_id.acc_holder_name or "",
                )
                writer.writerow(
                    {
                        "sequence": "D%s" % str(i).zfill(6),
                        "acc_number": acc_number.replace(" ", "").rjust(23),
                        "amount": "{:.2f}".format(line.amount)
                        .replace(".", "")
                        .zfill(15),
                        "date": obj_date,
                        "space": "".rjust(23),
                        "acc_holder_name": acc_holder_name.ljust(49),
                        "date_transfer": "%s%s"
                        % (obj_date_transfer, ("%s" % i).zfill(19)),
                        "end": "0000000000.000000000000.000000000000.00".rjust(189),
                    }
                )

    def csv_report_options(self):
        res = super().csv_report_options()
        res["fieldnames"].append("sequence")
        res["fieldnames"].append("acc_number")
        res["fieldnames"].append("amount")
        res["fieldnames"].append("date")
        res["fieldnames"].append("space")
        res["fieldnames"].append("acc_holder_name")
        res["fieldnames"].append("date_transfer")
        res["fieldnames"].append("end")
        res["delimiter"] = " "
        res["quotechar"] = ","
        res["quoting"] = csv.QUOTE_ALL
        return res
