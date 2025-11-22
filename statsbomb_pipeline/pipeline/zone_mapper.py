from helpers.event_parser import parse_event_file
from helpers.zone_mapping import test_zone_mapping

parsed = parse_event_file("../data/events/7298.json")

test_zone_mapping(parsed, n=20)
