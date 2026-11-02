# Exercise 1.1 test outcomes

| # | Case | Expected / observed outcome |
|---|---|---|
| 1 | Empty menu input | Unknown choice message; process continues |
| 2 | Valid P0003 and example.test email | Registration is saved and logged |
| 3 | Repeat P0001 for EVT01 | Duplicate rejected, warning logged |
| 4 | ID `12` | Rejected with ID format message |
| 5 | Email `bad` | Rejected with email message |
| 6 | Register into capacity reached | Rejected as full |
| 7 | Missing JSON file | Empty list default used |
| 8 | Malformed JSON file | Error logged, safe empty-list fallback |
| 9 | Cancel existing pair | Registration removed and cancellation logged |
| 10 | Attendance export | CSV header and current registrations written |

Manual checks are reproducible through the menu. The same validation functions can also be imported for focused checks.
