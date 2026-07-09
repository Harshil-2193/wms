### Warehouse Management

Waehouse Management 

### Dynamic Storage Hierarchy

Small layer on top of ERPNext's Warehouse to track exact physical location of
stock inside a warehouse (Room -> Rack -> Section, or whatever the client
wants) without touching how ERPNext itself does stock. SLE, Bin, valuation,
FIFO, accounting entries etc all keep working exactly the same as before.

**Storage Location** doctype - tree doctype (same idea as Item Group /
Warehouse). Every node has a `parent_storage_location`, so you can build any
depth of hierarchy, no code changes needed to add/remove/rename a level.
`location_type` is just free text (Room, Rack, Bin, Zone...) so it's fully
configurable from the UI.

Important bit - every location is independent. A parent's qty is NOT the sum
of its children's qty. Qty is not even a stored field on the doctype, it's
calculated from the ledger, so it can never go out of sync with actual
movements.

**Storage Location Ledger** doctype - one row per stock move between two
storage locations. Has item, qty, from location, to location, warehouse,
user, posting datetime and voucher_type/voucher_no (points back to the Stock
Entry that caused it). Insert only, `validate()` blocks any update after
creation - keeps the audit trail honest, same idea as how ERPNext's own
Stock Ledger Entry works. (tried making it submittable first, but that broke
cancelling the Stock Entry - frappe blocks a submittable doc from linking to
an already-cancelled voucher, only `amended_from` is exempt from that check.
insert-only avoids the whole problem.)

Hook up - added 2 custom fields on Stock Entry Detail,
`custom_from_storage_location` and `custom_to_storage_location` (both Link to
Storage Location). On submit of a Stock Entry, `wms/events/events.py` loops
the items and writes a Storage Location Ledger row for any item row that has
a location set. On cancel it writes the reverse (from/to swapped) so it nets
back to zero. This is completely separate from ERPNext's own stock flow, the
`s_warehouse`/`t_warehouse` fields are untouched - we're only recording
*where inside the warehouse* the stock physically sits.

Viewing qty - open a Storage Location and click the "Stock Summary" button,
shows direct qty at that location plus qty of each immediate child location.
Doesnt roll child qty up into the parent, each number stands on its own.

Known limitation - qty is calculated on the fly from the ledger (sum in -
sum out) every time, not cached. fine for now, would need caching if the
ledger grows huge. also qty shown is total across all items, not item wise -
can extend the ledger query with a group by item_code later if that's
needed.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app wms
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/wms
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade
### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit
