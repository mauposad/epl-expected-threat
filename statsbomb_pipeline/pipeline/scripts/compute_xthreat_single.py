from statsbomb_pipeline.pipeline.parsing.events_parser import parse_event_file
from statsbomb_pipeline.pipeline.xthreat.transition_builder import build_transitions
from statsbomb_pipeline.pipeline.xthreat.value_iteration import build_value_function
from statsbomb_pipeline.pipeline.xthreat.xthreat_scorer import (
    score_actions_with_xthreat,
)
from statsbomb_pipeline.pipeline.xthreat.xthreat_aggregator import aggregate_xthreat

parsed = parse_event_file("statsbomb_pipeline/data/events/7298.json")
transitions, shot_counts, shot_xg = build_transitions(parsed)
values = build_value_function(transitions, shot_counts, shot_xg)
scored = score_actions_with_xthreat(parsed, values)
results = aggregate_xthreat(scored)

print(results)
