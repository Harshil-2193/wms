# Copyright (c) 2026, Harshil Patel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StorageLocation(Document):
	pass


def get_direct_qty(location):
	# qty directly at this location only, not summed from children
	received = frappe.db.sql(
		"select sum(qty) from `tabStorage Location Ledger` where to_storage_location=%s",
		location,
	)[0][0] or 0
	issued = frappe.db.sql(
		"select sum(qty) from `tabStorage Location Ledger` where from_storage_location=%s",
		location,
	)[0][0] or 0
	return received - issued


@frappe.whitelist()
def get_stock_summary(location):
	children = frappe.get_all(
		"Storage Location",
		filters={"parent_storage_location": location},
		fields=["name", "location_type"],
	)
	for child in children:
		child["qty"] = get_direct_qty(child.name)

	return {"direct_qty": get_direct_qty(location), "children": children}
