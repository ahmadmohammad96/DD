import frappe

def calculate_amount(doc, handler = None):
    total = 0
    for i in doc.items:
        i.amount = i.qty * i.rate
        i.base_amount = i.qty * i.base_rate
        total += i.qty

    return total

def create_gl(doc, handler=None):
    commission_income_account_name = doc.commission_income_account_name
    commission_expense_account_name = doc.commission_expense_account_name
    account_type_1 = frappe.get_value("Account",commission_income_account_name,"account_type")
    account_type_2 = frappe.get_value("Account",commission_expense_account_name,'account_type')

    default_commission_income = frappe.get_value('Company',doc.company,'default_commission_income')
    default_commission_expense = frappe.get_value('Company',doc.company,'default_commission_expense')

    if not default_commission_income:
        frappe.throw("Please set default commission income account for the company {}".format(doc.company))
    if not default_commission_expense:
        frappe.throw("Please set default commission expense account for the company {}".format(doc.company))

    if account_type_1 == 'Commission Receivable':

        gl = frappe.new_doc("GL Entry")
        gl.posting_date = doc.posting_date
        gl.account = default_commission_income
        gl.credit = calculate_amount(doc) * doc.commission_income_rate
        gl.account_currency = doc.currency
        gl.against = doc.supplier
        gl.voucher_type = 'Purchase Invoice'
        gl.voucher_no = doc.name
        gl.cost_center = doc.cost_center
        gl.company = doc.company
        gl.flags.ignore_permissions = 1

        gl_2 = frappe.new_doc("GL Entry")
        gl_2.posting_date = doc.posting_date
        gl_2.account = commission_income_account_name
        gl_2.debit = calculate_amount(doc) * doc.commission_income_rate
        gl_2.account_currency = doc.currency
        gl_2.against = doc.supplier
        gl_2.voucher_type = 'Purchase Invoice'
        gl_2.voucher_no = doc.name
        gl_2.cost_center = doc.cost_center
        gl_2.company = doc.company
        gl_2.flags.ignore_permissions = 1
        
        gl.save()
        gl_2.save()

    # else:
    #     frappe.throw('Please Set Account Type as "Commission Receivable" for {}'.format(commission_income_account_name))
    #     return False

    if account_type_2 == 'Commission Payable':
        gl = frappe.new_doc("GL Entry")
        gl.posting_date = doc.posting_date
        gl.account = default_commission_expense
        gl.debit = calculate_amount(doc) * doc.commission_expense_rate
        gl.account_currency = doc.currency
        gl.against = doc.supplier
        gl.voucher_type = 'Purchase Invoice'
        gl.voucher_no = doc.name
        gl.cost_center = doc.cost_center
        gl.company = doc.company
        gl.flags.ignore_permissions = 1

        gl_2 = frappe.new_doc("GL Entry")
        gl_2.posting_date = doc.posting_date
        gl_2.account = commission_expense_account_name
        gl_2.credit = calculate_amount(doc) * doc.commission_expense_rate
        gl_2.account_currency = doc.currency
        gl_2.against = doc.supplier
        gl_2.voucher_type = 'Purchase Invoice'
        gl_2.voucher_no = doc.name
        gl_2.cost_center = doc.cost_center
        gl_2.company = doc.company
        gl_2.flags.ignore_permissions = 1
        
        gl.save()
        gl_2.save()

    # else:
    #     frappe.throw('Please Set Account Type as "Commission Payable" for {}'.format(commission_expense_account_name))
    #     return False
    
    
