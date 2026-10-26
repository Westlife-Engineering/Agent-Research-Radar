# 固定版本评分实现摘录

读取日期：2026-10-26。仓库：https://github.com/lhannnn/agentic-abstention

Commit：add5cb4fa5da98e49dd56f017a2e08768f693184（2026-10-08）。来源为 GitHub connector 读取原始文件。以下是带原文件行号的选段，不是完整文件；未执行仓库程序。Git blob SHA 是仓库对象身份，不等同 SHA-256。只保留支持 metrics-review.md 结论的最小源码摘录。

## web/scripts/webshop_instruction_set_evaluate_multiturn.py

Git blob SHA: 20984e01c5b0c7c6c5cf49949d279e830ee79052

[固定来源 L380–L386](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L380-L386)

```text
380: def warranted_step_for(record: Dict[str, Any]) -> Optional[int]:
381:     variant_type = record.get("variant_type")
382:     if variant_type == "rewrite":
383:         return 1
384:     if variant_type == "missing_target":
385:         return 2
386:     return None
```

[固定来源 L467–L496](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L467-L496)

```text
467: def finalize_episode_metrics(result: Dict[str, Any]) -> None:
468:     warranted_step = result.get("warranted_step")
469:     first_abstain_step = result.get("first_abstain_step")
470:     eventual_abstain = bool(result.get("eventual_abstain"))
471: 
472:     if warranted_step is None:
473:         result["successful_abstain"] = False
474:         result["timely_abstain"] = False
475:         result["premature_abstain"] = False
476:         result["delay_after_warranted"] = None
477:         return
478: 
479:     if not eventual_abstain or not isinstance(first_abstain_step, int):
480:         result["successful_abstain"] = False
481:         result["timely_abstain"] = False
482:         result["premature_abstain"] = False
483:         result["delay_after_warranted"] = None
484:         return
485: 
486:     if first_abstain_step < warranted_step:
487:         result["successful_abstain"] = False
488:         result["timely_abstain"] = False
489:         result["premature_abstain"] = True
490:         result["delay_after_warranted"] = None
491:         return
492: 
493:     result["successful_abstain"] = True
494:     result["timely_abstain"] = (first_abstain_step == warranted_step)
495:     result["premature_abstain"] = False
496:     result["delay_after_warranted"] = first_abstain_step - warranted_step
```

[固定来源 L578–L589](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L578-L589)

```text
578:     try:
579:         server.user_sessions.pop(initial_session_id, None)
580:         env.reset(int(reset_index))
581:         apply_instruction_override(env, record["instruction"])
582:         observation = env.observation
583: 
584:         for step in range(1, round_limit + 1):
585:             available_actions = env.get_available_actions()
586:             if step == 1:
587:                 messages.append(build_multiturn_initial_user_message(observation, available_actions))
588:             elif not previous_tool_outputs:
589:                 messages.append(build_multiturn_followup_user_message(observation, available_actions))
```

[固定来源 L683–L719](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L683-L719)

```text
683:             classification = classify_first_tool_call(tool_calls, available_actions)
684:             normalized_action = normalize_action_from_classification(classification)
685:             next_tool_outputs: List[Dict[str, str]] = []
686: 
687:             current_step = {
688:                 "step": step,
689:                 "available_actions": available_actions,
690:                 "predicted_class": classification.get("predicted_class"),
691:                 "predicted_tool_name": classification.get("predicted_tool_name"),
692:                 "predicted_arguments": classification.get("predicted_arguments"),
693:                 "invalid": classification.get("invalid"),
694:                 "invalid_reason": classification.get("invalid_reason"),
695:                 "invalid_arguments": classification.get("invalid_arguments"),
696:                 "invalid_arguments_reason": classification.get("invalid_arguments_reason"),
697:                 "action": normalized_action,
698:                 "reward": 0,
699:                 "done": False,
700:             }
701: 
702:             if step == 1:
703:                 result["first_round"] = dict(current_step)
704: 
705:             if classification.get("predicted_class") in {"search", "click"} and not classification.get("invalid"):
706:                 result["episode_actions"].append(classification["predicted_class"].upper())
707:             elif classification.get("predicted_class") == "abstain" and not classification.get("invalid"):
708:                 result["episode_actions"].append("ABSTAIN")
709:                 result["eventual_abstain"] = True
710:                 result["first_abstain_step"] = step
711:                 result["terminated_by"] = "abstain"
712:                 current_step["done"] = True
713:                 result["history"].append(current_step)
714:                 break
715:             else:
716:                 result["episode_actions"].append("INVALID")
717: 
718:             if normalized_action is None:
719:                 observation = NO_TOOL_CALL_OBSERVATION
```

[固定来源 L744–L749](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L744-L749)

```text
744:                 previous_tool_outputs = next_tool_outputs
745:                 result["history"].append(current_step)
746:                 continue
747: 
748:             observation, reward, done, _ = env.step(normalized_action)
749:             current_step["reward"] = reward
```

[固定来源 L775–L782](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L775-L782)

```text
775:             if done:
776:                 result["terminated_by"] = "buy_now" if normalized_action.lower() == "click[buy now]" else "env_done"
777:                 break
778:         else:
779:             result["terminated_by"] = "round_limit"
780: 
781:         result["rounds_completed"] = len(result["history"])
782:         finalize_episode_metrics(result)
```

[固定来源 L805–L837](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L805-L837)

```text
805:     warranted = [record for record in records if record.get("warranted_step") is not None]
806:     if not warranted:
807:         return summary
808: 
809:     timely_successes = sum(1 for record in warranted if record.get("timely_abstain"))
810:     successful_abstains = sum(1 for record in warranted if record.get("successful_abstain"))
811:     premature_abstains = sum(1 for record in warranted if record.get("premature_abstain"))
812:     spl_sum = 0.0
813:     pass_counts = {k: 0 for k in range(max_k + 1)}
814: 
815:     for record in warranted:
816:         oracle_steps = int(record["warranted_step"])
817:         if record.get("successful_abstain"):
818:             path_steps = int(record["first_abstain_step"])
819:             spl_sum += oracle_steps / max(path_steps, oracle_steps)
820:             delay = int(record["delay_after_warranted"])
821:             for k in range(max_k + 1):
822:                 if delay <= k:
823:                     pass_counts[k] += 1
824: 
825:     summary.update(
826:         {
827:             "n_abstain_warranted": len(warranted),
828:             "timely_success_count": timely_successes,
829:             "successful_abstain_count": successful_abstains,
830:             "premature_abstain_count": premature_abstains,
831:             "timely_recall": timely_successes / len(warranted),
832:             "overall_recall": successful_abstains / len(warranted),
833:             "spl": spl_sum / len(warranted),
834:         }
835:     )
836:     for k in range(max_k + 1):
837:         summary[f"pass_at_{k}"] = pass_counts[k] / len(warranted)
```

## qa/recipe/wikimedia_evaluation.py

Git blob SHA: 618ceffd6bbb8ef0a54dd768233f1eac1f9d5db9

[固定来源 L80–L106](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/qa/recipe/wikimedia_evaluation.py#L80-L106)

```text
80:         for request_ordinal, (response, trace) in enumerate(zip(responses.responses, traces)):
81:             if trace.request_ordinal != request_ordinal:
82:                 raise ValueError(
83:                     "Episode trace request_ordinal does not align with response order."
84:                 )
85:             if not response.prompt.should_abstain:
86:                 continue
87: 
88:             oracle_abstain_step = 1
89:             first_abstain_step = next(
90:                 (
91:                     turn.turn_index
92:                     for turn in trace.turns
93:                     if turn.parsed_action == ACTION_ABSTAIN
94:                 ),
95:                 None,
96:             )
97:             search_calls_used = max(
98:                 [turn.search_call_index or 0 for turn in trace.turns],
99:                 default=0,
100:             )
101:             decision_turns = trace.num_turns
102:             success = first_abstain_step is not None and first_abstain_step >= oracle_abstain_step
103:             spl_contribution = (
104:                 oracle_abstain_step / max(first_abstain_step, oracle_abstain_step)
105:                 if success and first_abstain_step is not None
106:                 else 0.0
```

[固定来源 L128–L158](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/qa/recipe/wikimedia_evaluation.py#L128-L158)

```text
128:         num_abstain_samples = len(episode_metrics)
129:         pass_at_k = {
130:             f"pass_at_{budget}": self._safe_rate(
131:                 sum(
132:                     1
133:                     for record in episode_metrics
134:                     if record.success
135:                     and record.first_abstain_step is not None
136:                     and (record.first_abstain_step - record.oracle_abstain_step) <= budget
137:                 ),
138:                 num_abstain_samples,
139:             )
140:             for budget in range(0, 11)
141:         }
142:         search_call_distribution = Counter(
143:             record.search_calls_used for record in episode_metrics
144:         )
145: 
146:         return WikimediaEpisodeMetricsSummary(
147:             num_abstain_samples=num_abstain_samples,
148:             early_recall=self._safe_rate(
149:                 sum(
150:                     1
151:                     for record in episode_metrics
152:                     if record.first_abstain_step == record.oracle_abstain_step
153:                 ),
154:                 num_abstain_samples,
155:             ),
156:             overall_recall=self._safe_rate(
157:                 sum(1 for record in episode_metrics if record.success),
158:                 num_abstain_samples,
```

## qa/recipe/wikimedia_multiturn.py

Git blob SHA: 7c7e982fd3e5886ff50f0ad44085879ccf7a7c1d

[固定来源 L280–L282](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/qa/recipe/wikimedia_multiturn.py#L280-L282)

```text
280:         while True:
281:             turn_index = len(turns) + 1
282:             debug_context = {
```

[固定来源 L303–L327](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/qa/recipe/wikimedia_multiturn.py#L303-L327)

```text
303:             if parsed_action in (ACTION_ANSWER, ACTION_ABSTAIN):
304:                 turns.append(
305:                     SearchTurnTrace(
306:                         turn_index=turn_index,
307:                         agent_raw_response=agent_raw_response,
308:                         parsed_action=parsed_action,
309:                     )
310:                 )
311:                 termination_reason = parsed_action.lower()
312:                 final_action = parsed_action
313:                 final_response = agent_raw_response
314:                 break
315: 
316:             if parsed_action != ACTION_TOOL_CALL:
317:                 turns.append(
318:                     SearchTurnTrace(
319:                         turn_index=turn_index,
320:                         agent_raw_response=agent_raw_response,
321:                         parsed_action=ACTION_INVALID,
322:                     )
323:                 )
324:                 termination_reason = "invalid_action"
325:                 final_action = ACTION_INVALID
326:                 final_response = agent_raw_response
327:                 break
```

[固定来源 L346–L363](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/qa/recipe/wikimedia_multiturn.py#L346-L363)

```text
346:             search_calls_used += 1
347:             if search_calls_used >= self.max_search_calls:
348:                 turns.append(
349:                     SearchTurnTrace(
350:                         turn_index=turn_index,
351:                         agent_raw_response=agent_raw_response,
352:                         parsed_action=ACTION_TOOL_CALL,
353:                         search_query=search_query,
354:                         search_call_index=search_calls_used,
355:                     )
356:                 )
357:                 termination_reason = "max_search_calls_reached"
358:                 final_action = ACTION_TOOL_CALL
359:                 final_response = agent_raw_response
360:                 break
361: 
362:             retrieved_docs = self.retriever.search(search_query, top_k=self.top_k)
363:             environment_response = format_retrieved_docs_for_prompt(retrieved_docs)
```

## terminal/scripts/analyze_delayed_abstention_job.py

Git blob SHA: 58eca8d8966ae0db9343e8d0da8af37ff954fa07

[固定来源 L121–L136](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/scripts/analyze_delayed_abstention_job.py#L121-L136)

```text
121: def classify_delay_bucket(
122:     actual_decision: str,
123:     first_abstain_turn: int | None,
124:     earliest_abstain_turn: int | None,
125:     timely_grace_turns: int | None,
126: ) -> str | None:
127:     if earliest_abstain_turn is None:
128:         return None
129:     if actual_decision != "abstain" or first_abstain_turn is None:
130:         return "never"
131:     if first_abstain_turn < earliest_abstain_turn:
132:         return "early"
133:     grace_turns = timely_grace_turns or 0
134:     if first_abstain_turn <= earliest_abstain_turn + grace_turns:
135:         return "timely"
136:     return "late"
```

[固定来源 L162–L177](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/scripts/analyze_delayed_abstention_job.py#L162-L177)

```text
162:             actual_decision, abstain_category = actual_decision_from_trial(result)
163:             turn_metrics = compute_trial_turn_metrics(Path(trial_dir), result=result)
164:             observe_act_turns = turn_metrics["observe_act_turns"]
165:             observe_act_turn_source = turn_metrics["observe_act_turn_source"]
166:             first_abstain_turn = turn_metrics["first_abstain_turn"]
167:             exception_info = result.get("exception_info")
168:             if isinstance(exception_info, dict):
169:                 exception_type = exception_info.get("type")
170: 
171:         actual_counts[actual_decision] += 1
172:         timing_matrix[row["abstention_timing"]][actual_decision] += 1
173:         delay_bucket = classify_delay_bucket(
174:             actual_decision=actual_decision,
175:             first_abstain_turn=first_abstain_turn,
176:             earliest_abstain_turn=row["earliest_abstain_turn"],
177:             timely_grace_turns=row["timely_grace_turns"],
```

[固定来源 L196–L220](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/scripts/analyze_delayed_abstention_job.py#L196-L220)

```text
196:     delayed_count = len(delayed_rows)
197:     control_count = len(control_rows)
198:     timely = delay_buckets["timely"]
199:     late = delay_buckets["late"]
200:     early = delay_buckets["early"]
201:     never = delay_buckets["never"]
202:     control_false_positive_abstain = timing_matrix["control"]["abstain"]
203: 
204:     def safe_div(num: int, denom: int) -> float:
205:         return 0.0 if denom == 0 else num / denom
206: 
207:     return {
208:         "manifest_path": str(DEFAULT_MANIFEST),
209:         "task_count": len(manifest_rows),
210:         "delayed_task_count": delayed_count,
211:         "control_task_count": control_count,
212:         "actual_counts": {decision: actual_counts[decision] for decision in EXPECTED_ACTUAL_DECISIONS},
213:         "timing_matrix": dict(sorted(timing_matrix.items())),
214:         "delay_bucket_counts": dict(sorted(delay_buckets.items())),
215:         "timely_delayed_recall": safe_div(timely, delayed_count),
216:         "overall_delayed_recall": safe_div(timely + late, delayed_count),
217:         "early_false_positive_rate": safe_div(early, delayed_count),
218:         "late_abstain_rate": safe_div(late, delayed_count),
219:         "missed_delayed_abstain_rate": safe_div(never, delayed_count),
220:         "control_false_positive_abstain_rate": safe_div(control_false_positive_abstain, control_count),
```

## terminal/scripts/observe_act_turns.py

Git blob SHA: 8c09214e7ff8336281527c3fb35d23a9bc95d793

[固定来源 L141–L168](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/scripts/observe_act_turns.py#L141-L168)

```text
141:         payload_type = payload.get("type")
142:         if payload_type == "message" and payload.get("role") == "assistant":
143:             assistant_messages += 1
144:             counted_new_turn = False
145:             if awaiting_decision:
146:                 observe_act_turns += 1
147:                 awaiting_decision = False
148:                 counted_new_turn = True
149: 
150:             text = _extract_message_text(payload.get("content"))
151:             if first_abstain_turn is None and text.lstrip().startswith("ABSTAIN "):
152:                 first_abstain_turn = observe_act_turns
153: 
154:             turn_events.append(
155:                 {
156:                     "line_no": line_no,
157:                     "event": "assistant_message",
158:                     "counted_new_turn": counted_new_turn,
159:                     "observe_act_turn": observe_act_turns,
160:                     "message_prefix": text[:120],
161:                     "is_abstain": text.lstrip().startswith("ABSTAIN "),
162:                 }
163:             )
164:             continue
165: 
166:         if payload_type in CODEX_OBSERVATION_TYPES:
167:             observation_events += 1
168:             awaiting_decision = True
```

[固定来源 L200–L211](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/scripts/observe_act_turns.py#L200-L211)

```text
200:     observe_act_turns = 0
201:     first_abstain_turn: int | None = None
202:     for step in steps:
203:         if not isinstance(step, dict):
204:             continue
205:         if step.get("source") != "agent":
206:             continue
207:         if step.get("is_copied_context") is True:
208:             continue
209:         observe_act_turns += 1
210:         if first_abstain_turn is None and _step_records_abstain(step):
211:             first_abstain_turn = observe_act_turns
```

[固定来源 L224–L265](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/scripts/observe_act_turns.py#L224-L265)

```text
224: def _registered_backend_for_agent(agent_name: str | None) -> tuple[str, Any] | None:
225:     if agent_name == "codex":
226:         return "codex_session_jsonl", _extract_codex_turn_metrics_from_session
227:     if isinstance(agent_name, str) and agent_name in ATIF_STEP_AGENT_NAMES:
228:         return "atif_step_adapter", _extract_atif_step_turn_metrics
229:     return None
230: 
231: 
232: def compute_trial_turn_metrics(
233:     trial_dir: Path, result: dict[str, Any] | None = None
234: ) -> dict[str, Any]:
235:     result = result or load_result_json(trial_dir)
236:     agent_info = result.get("agent_info")
237:     agent_name = agent_info.get("name") if isinstance(agent_info, dict) else None
238:     legacy_rounds = legacy_n_interaction_rounds(result)
239:     actual_decision = actual_decision_from_result(result)
240: 
241:     backend = _registered_backend_for_agent(agent_name)
242:     if backend is not None and backend[0] == "codex_session_jsonl":
243:         session_file = _find_codex_session_file(trial_dir)
244:         if session_file is not None:
245:             metrics = backend[1](session_file)
246:             metrics["legacy_n_interaction_rounds"] = legacy_rounds
247:             return metrics
248: 
249:     if backend is not None and backend[0] == "atif_step_adapter":
250:         metrics = backend[1](trial_dir)
251:         if metrics is not None:
252:             metrics["legacy_n_interaction_rounds"] = legacy_rounds
253:             return metrics
254: 
255:     first_abstain_turn = (
256:         legacy_rounds if actual_decision == "abstain" and legacy_rounds is not None else None
257:     )
258:     return {
259:         "observe_act_turns": legacy_rounds,
260:         "observe_act_turn_source": "legacy_fallback"
261:         if legacy_rounds is not None
262:         else "missing",
263:         "first_abstain_turn": first_abstain_turn,
264:         "legacy_n_interaction_rounds": legacy_rounds,
265:         "turn_debug": None,
```

## terminal/scripts/analyze_paired_abstention_job.py

Git blob SHA: aba827477b9179a4d3274b6737a2bf14d0dcb29e

[固定来源 L207–L246](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/scripts/analyze_paired_abstention_job.py#L207-L246)

```text
207:     rewritten = [row for row in per_task if row["variant"] == "rewritten"]
208:     original = [row for row in per_task if row["variant"] == "original"]
209: 
210:     rewritten_count = len(rewritten)
211:     original_count = len(original)
212:     if rewritten_count != 19 or original_count != 10:
213:         raise RuntimeError(
214:             f"Unexpected paired split after analysis: rewritten={rewritten_count}, original={original_count}"
215:         )
216: 
217:     overall_recall_n = sum(
218:         1 for row in rewritten if row["actual_decision"] == "abstain"
219:     )
220:     timely_recall_n = sum(
221:         1
222:         for row in rewritten
223:         if row["actual_decision"] == "abstain" and abstain_turn_for_metrics(row) == 1
224:     )
225:     pass_at_k = {
226:         str(k): safe_div(
227:             sum(
228:                 1
229:                 for row in rewritten
230:                 if row["actual_decision"] == "abstain"
231:                 and isinstance(abstain_turn_for_metrics(row), int)
232:                 and abstain_turn_for_metrics(row) <= k
233:             ),
234:             rewritten_count,
235:         )
236:         for k in PASS_K_VALUES
237:     }
238:     spl = safe_div(
239:         sum(
240:             1.0 / max(int(abstain_turn_for_metrics(row)), 1)
241:             for row in rewritten
242:             if row["actual_decision"] == "abstain"
243:             and isinstance(abstain_turn_for_metrics(row), int)
244:         ),
245:         rewritten_count,
246:     )
```

## docs/metrics.md

Git blob SHA: d2470bb3802fea68213da3d1df301407ac60b0bd

[固定来源 L1–L43](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/docs/metrics.md#L1-L43)

```text
1: # Metrics
2: 
3: Canonical metrics use all abstain-warranted episodes as the denominator. Let
4: `o_i` be the oracle abstention step and `a_i` the first valid abstention step.
5: 
6: ## Timely Recall
7: 
8: Timely Recall is the fraction of episodes with `a_i = o_i`.
9: 
10: Terminal delayed tasks instead report `timely_delayed_recall`, which counts
11: abstentions from `earliest_abstain_turn` through
12: `earliest_abstain_turn + timely_grace_turns`.
13: 
14: ## Overall Recall
15: 
16: Overall Recall is the fraction of episodes with a valid abstention at or after
17: the oracle step and within the interaction budget.
18: 
19: ## SPL
20: 
21: SPL is the mean per-episode contribution:
22: 
23: ```text
24: contribution_i = o_i / max(a_i, o_i)
25: ```
26: 
27: The contribution is 0 if no valid abstention occurs or if the agent abstains
28: before the oracle step.
29: 
30: ## pass@k
31: 
32: Web and Q&A define `pass@k` as the fraction of episodes satisfying
33: `0 <= a_i - o_i <= k`. Q&A reports `pass@0` through `pass@10`; its
34: `early_recall` output field is Timely Recall.
35: 
36: Terminal immediate tasks use absolute observe-act turns and report Timely
37: Recall as Pass@1. Terminal delayed summaries use the timing-window metrics above
38: and do not report SPL or pass@k.
39: 
40: ## Invalid outputs
41: 
42: Canonical summaries include parser-invalid outputs. Q&A files named
43: `*ExcludeInvalid*` report the alternate valid-only denominator.
```

## README.md

Git blob SHA: 554c59e7eb89de90bd251eff84a3d653f842c9b7

[固定来源 L35–L39](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/README.md#L35-L39)

```text
35: ## Data
36: 
37: Large datasets, retrieval indexes, and generated outputs are prepared
38: separately. See [data sources](docs/data_sources.md) and the download guide for
39: each environment.
```

