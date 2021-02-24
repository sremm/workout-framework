from pathlib import Path

import config
from wof.adapters.mongo_db import mongo_session_factory
from wof.bootstrap import bootstrap_handle
from wof.domain import commands
from wof.entrypoints.main import Handle
from wof.import_workflows import data_merging, intensity_app, polar
from wof.service_layer import unit_of_work

base_path = Path(__file__).parent.parent.parent / "Data"


# handle_composed = Handle()
# db_settings = config.MongoSettings()
# session_factory = mongo_session_factory(db_settings)
# uow = unit_of_work.MongoUnitOfWork(session_factory=session_factory)
# handle_composed.set_composed_handle(bootstrap_handle(uow=uow))

polar_folder = (
    base_path
    / "Polar"
    / "21-02-2021-polar-user-data-export_b48effbf-1189-4b57-8271-f60cb4238363"
)
instensity_file = (
    base_path
    / "Intensity_app"
    / "21-02-2021-export76769ae64ca185aeb33011882493ed7b.csv"
)
print("Converting polar sessions")
polar_sessions = polar.load_all_sessions_in_folder(polar_folder)
print(f"Got {len(polar_sessions)} sessions")
print("Converting intensity sessions")
intensity_sessions = intensity_app.import_from_file(instensity_file)
print(f"Got {len(intensity_sessions)} sessions")
print("Merging sessions")
merged_sessions = data_merging.merge_polar_and_instensity_imports(
    polar_sessions=polar_sessions, intensity_sessions=intensity_sessions
)
print(f"Got {len(merged_sessions)} sessions")
# results = handle_composed(commands.AddSessions(sessions=merged_sessions))
