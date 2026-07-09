import frappe

def on_submit(doc, method):
    for row in doc.items:
        from_loc = row.get("custom_from_storage_location")
        to_loc = row.get("custom_to_storage_location")
        if from_loc or to_loc:
            _log_movement(row, from_loc, to_loc, doc)

def on_cancel(doc, method):
    for row in doc.items:
        from_loc = row.get("custom_from_storage_location")
        to_loc = row.get("custom_to_storage_location")
        if from_loc or to_loc:
            # swap from/to so the net effect of the entry cancels out
            _log_movement(row, to_loc, from_loc, doc)

def _log_movement(row, from_loc, to_loc, doc, voucher_type="Stock Entry"):
    entry = frappe.new_doc("Storage Location Ledger")
    entry.update({
        "posting_datetime": frappe.utils.now_datetime(),
        "item_code": row.item_code,
        "qty": row.qty,
        "from_storage_location": from_loc,
        "to_storage_location": to_loc,
        "warehouse": row.t_warehouse or row.s_warehouse,
        "user": frappe.session.user,
        "voucher_type": voucher_type,
        "voucher_no": doc.name,
    })
    entry.insert(ignore_permissions=True)
