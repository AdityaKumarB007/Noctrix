import argparse
import logging
import os
import sys
import yaml

from discovery.scanner_dispatcher import ScannerDispatcher
from graph.graph_writer import GraphWriter
from analysis.risk_scorer import RiskScorer
from remediation.remediation_dispatcher import RemediationDispatcher

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("noctrix.main")

def load_config(config_path: str = "config.yaml") -> dict:
    if not os.path.exists(config_path):
        logger.error(f"Configuration file '{config_path}' not found.")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_pipeline(config_path: str = "config.yaml"):
    print("=" * 80)
    print("                      NOCTRIX PIPELINE ORCHESTRATOR")
    print("        Non-Human Identity Discovery, Graph Mapping & Remediation")
    print("=" * 80)

    config = load_config(config_path)

    # -------------------------------------------------------------
    # STAGE 1: Parallel Multi-Source Discovery
    # -------------------------------------------------------------
    print("\n[STAGE 1/4] Running Discovery Layer (ThreadPoolExecutor)...")
    dispatcher = ScannerDispatcher.from_config(config)
    discovered_nhis = dispatcher.run_all()
    print(f"[OK] Discovery completed: Found {len(discovered_nhis)} non-human identities.")

    # -------------------------------------------------------------
    # STAGE 2: Graph Persistence (Neo4j Ingestion)
    # -------------------------------------------------------------
    print("\n[STAGE 2/4] Persisting Identities to Neo4j Graph Database...")
    neo4j_cfg = config.get("graph", {}).get("neo4j", {})
    graph_writer = GraphWriter(
        uri=neo4j_cfg.get("uri", "bolt://localhost:7687"),
        user=neo4j_cfg.get("user", "neo4j"),
        password=neo4j_cfg.get("password", "password"),
        database=neo4j_cfg.get("database", "neo4j"),
    )

    neo4j_online = graph_writer.verify_connectivity()
    if neo4j_online:
        ingested = graph_writer.write_identities(discovered_nhis)
        print(f"[OK] Graph Ingestion completed: {ingested} identities merged into Neo4j.")
    else:
        print("[!] Neo4j is offline. (Run 'docker compose up -d' to start Neo4j). In-memory evaluation will continue.")

    # -------------------------------------------------------------
    # STAGE 3: Risk Scoring & Ghost Identity Detection
    # -------------------------------------------------------------
    print("\n[STAGE 3/4] Running Risk Analysis & Ghost Identity Detection...")
    risk_scorer = RiskScorer.from_config(config)

    if neo4j_online:
        analyzed = risk_scorer.analyze_graph(graph_writer)
        print(f"[OK] Graph Risk Analysis completed: {analyzed} identities evaluated in Neo4j.")
    else:
        risk_scorer.evaluate_all(discovered_nhis)
        print(f"[OK] In-Memory Risk Analysis completed: {len(discovered_nhis)} identities scored.")

    # -------------------------------------------------------------
    # STAGE 4: Automated Remediation & Slack Alerting
    # -------------------------------------------------------------
    print("\n[STAGE 4/4] Evaluating High-Risk Remediations (Threshold >= 70)...")
    rem_dispatcher = RemediationDispatcher.from_config(config)
    
    remediation_results = []
    if neo4j_online:
        remediation_results = rem_dispatcher.remediate_graph(graph_writer)
    print(f"[OK] Remediation completed: {len(remediation_results)} automated actions executed.")

    # -------------------------------------------------------------
    # SUMMARY & DASHBOARD LAUNCH INFO
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("                          PIPELINE RUN SUMMARY")
    print("=" * 80)
    
    all_records = graph_writer.fetch_all_identities() if neo4j_online else [n.to_dict() for n in discovered_nhis]
    high_risk_count = sum(1 for r in all_records if r.get("risk_score", 0.0) >= 70.0)
    ghost_count = sum(1 for r in all_records if r.get("is_ghost", False))
    remediated_count = sum(1 for r in all_records if r.get("remediated", False))

    print(f"Total Discovered NHIs   : {len(all_records)}")
    print(f"High-Risk NHIs (>=70)   : {high_risk_count}")
    print(f"Ghost Identities (Stale): {ghost_count}")
    print(f"Remediated Identities   : {remediated_count}")
    print("-" * 80)
    print("To view the interactive visualization and risk dashboard, run:")
    print("    streamlit run output/dashboard.py")
    print("=" * 80)

    graph_writer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NOCTRIX Non-Human Identity Pipeline Orchestrator")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml file")
    args = parser.parse_args()
    run_pipeline(args.config)
