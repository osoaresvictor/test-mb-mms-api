from app.events.publisher import publish_event
from app.services.mms_loader_service import run_incremental_loader

# just an example
if __name__ == "__main__":
    run_incremental_loader(publish_event_fn=publish_event)
