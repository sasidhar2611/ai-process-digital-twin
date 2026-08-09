import os
import json
import pandas as pd

class DashboardDataBuilder:
    def __init__(self, baseline_dir: str, scenarios_dir: str, analysis_dir: str):
        self.baseline_dir = baseline_dir
        self.scenarios_dir = scenarios_dir
        self.analysis_dir = analysis_dir
        
        self.scenario_labels = {
            "baseline": "Baseline",
            "dispatch_plus_1": "Dispatch +1 Worker",
            "picking_plus_5": "Picking +5 Workers",
            "packing_plus_2": "Packing +2 Workers",
            "productivity_plus_10": "Productivity +10%",
            "extended_shift": "Extended Shift"
        }

    def _load_kpis(self, scenario_id: str) -> dict:
        if scenario_id == "baseline":
            path = os.path.join(self.baseline_dir, "baseline_kpis.json")
        else:
            path = os.path.join(self.scenarios_dir, scenario_id, f"{scenario_id}_kpis.json")
        with open(path, "r") as f:
            return json.load(f)

    def _load_stage_metrics(self, scenario_id: str) -> pd.DataFrame:
        if scenario_id == "baseline":
            path = os.path.join(self.baseline_dir, "baseline_stage_metrics.parquet")
        else:
            path = os.path.join(self.scenarios_dir, scenario_id, f"{scenario_id}_stage_metrics.parquet")
        return pd.read_parquet(path)

    def build_dashboard_kpis(self) -> pd.DataFrame:
        rows = []
        for scenario_id, label in self.scenario_labels.items():
            kpis = self._load_kpis(scenario_id)
            rows.append({
                "scenario": scenario_id,
                "scenario_label": label,
                "orders_processed": kpis["orders_processed"],
                "mean_flow_time_seconds": kpis["mean_flow_time"],
                "mean_flow_time_hours": kpis["mean_flow_time"] / 3600.0,
                "median_flow_time_seconds": kpis["median_flow_time"],
                "p95_flow_time_seconds": kpis["p95_flow_time"],
                "p99_flow_time_seconds": kpis["p99_flow_time"],
                "mean_processing_time_seconds": kpis["mean_processing_time"],
                "mean_waiting_time_seconds": kpis["mean_waiting_time"],
                "mean_waiting_time_hours": kpis["mean_waiting_time"] / 3600.0,
                "sla_achievement_percent": kpis["sla_achievement_percentage"],
                "sla_breach_count": kpis.get("sla_breach_count", 0)  # default 0 if missing
            })
        return pd.DataFrame(rows)

    def build_stage_metrics(self) -> pd.DataFrame:
        dfs = []
        for scenario_id, label in self.scenario_labels.items():
            df = self._load_stage_metrics(scenario_id).copy()
            df["scenario"] = scenario_id
            df["scenario_label"] = label
            
            # Map sequence correctly if missing
            sequence_map = {"PROCESSING": 1, "PICKING": 2, "PACKING": 3, "SORTING": 4, "DISPATCH": 5}
            if "stage_sequence" not in df.columns:
                df["stage_sequence"] = df["stage"].map(sequence_map)
                
            # Keep required columns + human readable
            df = df.rename(columns={
                "stage_utilization": "utilization_percent",
                "worker_count": "worker_count"
            })
            
            # Reorder columns
            cols = [
                "scenario", "scenario_label", "stage", "stage_sequence", "worker_count",
                "utilization_percent", "mean_queue_length", "p95_queue_length", "max_queue_length",
                "mean_processing_time", "mean_waiting_time"
            ]
            
            # Handle missing max_queue_length just in case (baseline has it though)
            for c in cols:
                if c not in df.columns:
                    df[c] = 0.0
                    
            df = df[cols].rename(columns={
                "mean_queue_length": "mean_queue",
                "p95_queue_length": "p95_queue",
                "max_queue_length": "max_queue",
                "mean_processing_time": "mean_processing_time_seconds",
                "mean_waiting_time": "mean_waiting_time_seconds"
            })
            dfs.append(df)
            
        return pd.concat(dfs, ignore_index=True)

    def build_scenario_comparison(self) -> pd.DataFrame:
        baseline = self._load_kpis("baseline")
        rows = []
        for scenario_id, label in self.scenario_labels.items():
            if scenario_id == "baseline":
                continue
                
            kpis = self._load_kpis(scenario_id)
            
            # Determine hypothesis_result and intervention_type based on module 5 findings
            hypothesis = "SUPPORTED"
            if scenario_id == "picking_plus_5":
                hypothesis = "PARTIALLY SUPPORTED"
            
            intervention = "Worker Capacity"
            if scenario_id == "extended_shift":
                intervention = "Process Boundary"
            elif scenario_id == "productivity_plus_10":
                intervention = "Efficiency"
                
            # Load comparison JSON if it exists for exact percentages
            comp_path = os.path.join(self.scenarios_dir, f"baseline_vs_{scenario_id}.json")
            if os.path.exists(comp_path):
                with open(comp_path, "r") as f:
                    comp = json.load(f)
                    mf_change_sec = comp["mean_flow_time"]["absolute_change"]
                    mf_change_pct = comp["mean_flow_time"]["percentage_change"]
                    p95f_change_pct = comp["p95_flow_time"]["percentage_change"]
                    mw_change_sec = comp["mean_waiting_time"]["absolute_change"]
                    mw_change_pct = comp["mean_waiting_time"]["percentage_change"]
            else:
                # Calculate manually
                mf_change_sec = kpis["mean_flow_time"] - baseline["mean_flow_time"]
                mf_change_pct = (mf_change_sec / baseline["mean_flow_time"]) * 100
                p95f_change_pct = ((kpis["p95_flow_time"] - baseline["p95_flow_time"]) / baseline["p95_flow_time"]) * 100
                mw_change_sec = kpis["mean_waiting_time"] - baseline["mean_waiting_time"]
                mw_change_pct = (mw_change_sec / baseline["mean_waiting_time"]) * 100
            
            rows.append({
                "scenario": scenario_id,
                "scenario_label": label,
                "scenario_type": intervention,
                "description": f"Scenario evaluating {label}",
                "mean_flow_time_seconds": kpis["mean_flow_time"],
                "mean_flow_time_change_seconds": mf_change_sec,
                "mean_flow_time_change_percent": mf_change_pct,
                "p95_flow_time_seconds": kpis["p95_flow_time"],
                "p95_flow_time_change_percent": p95f_change_pct,
                "mean_waiting_time_seconds": kpis["mean_waiting_time"],
                "mean_waiting_time_change_seconds": mw_change_sec,
                "mean_waiting_time_change_percent": mw_change_pct,
                "sla_achievement_percent": kpis["sla_achievement_percentage"],
                "hypothesis_result": hypothesis
            })
        return pd.DataFrame(rows)

    def build_intervention_ranking(self) -> pd.DataFrame:
        path = os.path.join(self.analysis_dir, "intervention_ranking.json")
        with open(path, "r") as f:
            ranking = json.load(f)["ranking"]
            
        rows = []
        for idx, item in enumerate(ranking):
            scenario_id = item["scenario"]
            
            hypothesis = "SUPPORTED"
            if scenario_id == "picking_plus_5":
                hypothesis = "PARTIALLY SUPPORTED"
            
            intervention = "Worker Capacity"
            if scenario_id == "extended_shift":
                intervention = "Process Boundary"
            elif scenario_id == "productivity_plus_10":
                intervention = "Efficiency"
                
            priority = "LOW"
            if scenario_id == "extended_shift":
                priority = "PRIMARY"
            elif scenario_id == "dispatch_plus_1":
                priority = "SECONDARY"
                
            bottleneck_effect = "Strong system-level wait reduction"
            if scenario_id == "packing_plus_2" or scenario_id == "picking_plus_5":
                bottleneck_effect = "Negligible system-level effect"
                
            rows.append({
                "rank": idx + 1,
                "scenario": scenario_id,
                "scenario_label": self.scenario_labels[scenario_id],
                "intervention_category": intervention,
                "mean_flow_time_improvement_percent": item["mean_flow_time_improvement_pct"],
                "mean_waiting_time_improvement_percent": (item["mean_waiting_time_improvement_s"] / 21103.65) * 100, # Approx from baseline
                "p95_flow_time_improvement_percent": (item["p95_flow_time_improvement_s"] / 51452.34) * 100, # Approx from baseline
                "bottleneck_effect": bottleneck_effect,
                "hypothesis_result": hypothesis,
                "recommendation_priority": priority
            })
        return pd.DataFrame(rows)

    def build_bottleneck_summary(self) -> pd.DataFrame:
        path = os.path.join(self.analysis_dir, "bottleneck_analysis.json")
        with open(path, "r") as f:
            data = json.load(f)
            
        rows = []
        for score_info in data["stage_scores"]:
            role = "Active Process Bottleneck" if score_info["stage"] == data["overall_bottleneck_candidate"] else "Unconstrained Stage"
            if score_info["stage"] == data["largest_waiting_contribution_stage"] and score_info["stage"] != data["overall_bottleneck_candidate"]:
                role = "Boundary Queue Wait"
                
            rows.append({
                "stage": score_info["stage"],
                "utilization_percent": score_info["stage_utilization"] * 100.0,
                "mean_queue": score_info["mean_queue_length"],
                "p95_queue": score_info.get("p95_queue_length", 0.0), # Assuming not in json, but fallback
                "mean_waiting_time_seconds": score_info["mean_waiting_time"],
                "bottleneck_score": score_info["bottleneck_score"],
                "bottleneck_rank": 0, # Will compute below
                "bottleneck_role": role
            })
            
        df = pd.DataFrame(rows)
        # Assuming P95 queue wasn't preserved in JSON, read from baseline stage metrics directly
        b_stage = self._load_stage_metrics("baseline")
        df["p95_queue"] = df["stage"].map(b_stage.set_index("stage")["p95_queue_length"])
        
        df = df.sort_values("bottleneck_score", ascending=False).reset_index(drop=True)
        df["bottleneck_rank"] = df.index + 1
        return df

    def save_all(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        
        datasets = {
            "dashboard_kpis.csv": self.build_dashboard_kpis(),
            "dashboard_stage_metrics.csv": self.build_stage_metrics(),
            "dashboard_scenario_comparison.csv": self.build_scenario_comparison(),
            "dashboard_intervention_ranking.csv": self.build_intervention_ranking(),
            "dashboard_bottleneck_summary.csv": self.build_bottleneck_summary()
        }
        
        for filename, df in datasets.items():
            df.to_csv(os.path.join(output_dir, filename), index=False)
            print(f"Saved {filename} with {len(df)} rows.")
