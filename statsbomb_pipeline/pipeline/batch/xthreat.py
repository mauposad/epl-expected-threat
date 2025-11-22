from statsbomb_pipeline.pipeline.parsing.events_parser import parse_event_file
from statsbomb_pipeline.pipeline.xthreat.value_iteration import test_value_iteration

if __name__ == "__main__":
    parsed = parse_event_file("../data/events/7298.json")
    values = test_value_iteration(parsed)
