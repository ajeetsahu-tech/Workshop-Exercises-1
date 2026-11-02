# Design limitations

1. JSON files are read and rewritten as a whole; simultaneous writers could overwrite each other. A database with transactions is needed for concurrent use.
2. Email checking only verifies a simple shape and does not establish ownership or deliverability. This local simulator does not send messages.
