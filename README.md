admin dashboard 
Operational dashboard

KPI tiles: active trucks, available trucks, open loads, loads delivered today/week
Queue views: “Pending verification”, “Unassigned loads”, “Trucks idle > X hours”

admin logs page shows every action that is done on the webpage

Description: Finalize the platform roles and booking lifecycle states so every feature maps to a consistent status model.
Includes:

Roles: Admin (required), User (requestor), Truck Owner (supplier)
States:
Request: Draft → Submitted → Verified → Matched → Assigned → In Transit → Delivered → Closed / Cancelled
Truck: Draft → Submitted → Verified → Active → Unavailable → Suspended
Acceptance Criteria:
One documented state diagram for Request + Truck
List of allowed transitions (who can transition what)

Landing page: [[https://codepen.io/MAHESHBYL/pen/Yzrvywp]]
Dashboard: [[https://codepen.io/ash1198/pen/YPWNxxy]]
