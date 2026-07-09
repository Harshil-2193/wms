# Copyright (c) 2026, Harshil Patel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StorageLocationLedger(Document):
	def validate(self):
		# insert only, ledger rows are not meant to be edited once created
		if not self.is_new():
			frappe.throw("Storage Location Ledger entries cannot be modified")
