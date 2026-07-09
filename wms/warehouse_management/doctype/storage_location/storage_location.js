// Copyright (c) 2026, Harshil Patel and contributors
// For license information, please see license.txt

frappe.ui.form.on("Storage Location", {
	refresh(frm) {
		if (frm.is_new()) return;

		frm.add_custom_button(__("Stock Summary"), () => {
			frappe.call({
				method: "wms.warehouse_management.doctype.storage_location.storage_location.get_stock_summary",
				args: { location: frm.doc.name },
				callback: (r) => {
					if (!r.message) return;
					let d = r.message;
					let rows = (d.children || [])
						.map((c) => `<tr><td>${c.name}</td><td>${c.location_type || ""}</td><td>${c.qty}</td></tr>`)
						.join("");
					let html = `
						<p><b>Direct Qty:</b> ${d.direct_qty}</p>
						<table class="table table-bordered">
							<tr><th>Child Location</th><th>Type</th><th>Qty</th></tr>
							${rows || '<tr><td colspan="3">No child locations</td></tr>'}
						</table>`;
					frappe.msgprint({ title: __("Stock Summary - {0}", [frm.doc.name]), message: html });
				},
			});
		});
	},
});
