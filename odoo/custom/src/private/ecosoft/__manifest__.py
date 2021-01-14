# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Ecosoft Customization",
    "version": "13.0.1.2.0",
    "category": "Localization",
    "summary": """
* New Report Layout
* Fix SO and INV form
  * Add Tax Branch
  * Remove Tax Column
 * Salary Export to Text File
    """,
    "website": "http://ecosoft.co.th/",
    "depends": [
        "web",
        "sale",
        "l10n_th_partner",
        "hr",
        "report_csv",
        "excel_import_export",
    ],
    "author": "Ecosoft",
    "license": "AGPL-3",
    "data": [
        # Forms and Reports
        "report/data/report_layout.xml",
        "report/invoice_report_templates.xml",
        "report/sale_report_templates.xml",
        "report/report_receipt_tax_invoice.xml",
        "report/report_invoices_tax_invoice.xml",
        # Salary Export
        "salary_export/security/ir.model.access.csv",
        "salary_export/views/salary_export.xml",
        # Import Expense Invoice
        "import_expense_report/menu_action.xml",
        "import_expense_report/templates.xml",
    ],
}
