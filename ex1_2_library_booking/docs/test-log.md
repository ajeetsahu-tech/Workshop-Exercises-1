# Booking simulator test log

| # | Scenario | Expected outcome |
|---|---|---|
| 1 | Valid future resource booking | Active booking persisted and audit entry added |
| 2 | Overlapping slot, same resource/date | Rejected |
| 3 | Adjacent slot (10:00–11:00 then 11:00–12:00) | Accepted |
| 4 | Same slot, different resource | Accepted |
| 5 | End before start or malformed time | Rejected without crash |
| 6 | Unknown resource ID | Rejected |
| 7 | Cancel active booking | Status cancelled and audit entry added |
| 8 | Missing JSON | Empty list used |
| 9 | Corrupt or non-list JSON | Safe empty list and explanatory message |
| 10 | Daily schedule and report | Active rows exported; counts and cancellations summarized |

Slots use a single date and 24-hour `HH:MM` time. Booking output directory is named with the current date.
