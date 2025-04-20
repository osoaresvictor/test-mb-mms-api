# just an example
async def handle_event(event_type, payload):
    if event_type == "mms_calculated":
        print(
            f"[EVENT] New MMS calculated for {payload['pair']} "
            f"at {payload['timestamp']}"
        )
