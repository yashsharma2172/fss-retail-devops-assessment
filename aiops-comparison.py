# Task 6: Compare open-source AIOps tools vs traditional monitoring for FSS Retail on EKS

tools = {
    "Prometheus":   "Metrics collection and alerting rules for Kubernetes",
    "Grafana":      "Dashboards and visualization for all Prometheus metrics",
    "Loki":         "Log aggregation for all container and app logs (open source)",
    "Robusta":      "Kubernetes-native alerts with AI-powered root cause analysis",
    "OpenObserve":  "Open source Datadog alternative - logs, metrics, traces together",
}

traditional = {
    "Log analysis":          "Manual kubectl logs and grep",
    "Alert noise":           "High false alarms, manual threshold tuning",
    "Root cause":            "Hours of investigation by engineers",
    "Anomaly detection":     "Static thresholds only",
    "Incident response":     "Reactive - users report before team knows",
    "MTTR":                  "High - slow detection and resolution",
}

ai_assisted = {
    "Log analysis":          "Auto pattern detection via Claude AI",
    "Alert noise":           "Low - events correlated, fewer false alarms",
    "Root cause":            "Minutes - Claude suggests fix instantly",
    "Anomaly detection":     "ML-based dynamic thresholds",
    "Incident response":     "Proactive - detected before user impact",
    "MTTR":                  "Significantly reduced",
}

print("=== Open Source AIOps Tools for FSS Retail ===")
for tool, desc in tools.items():
    print(f"  {tool:15} : {desc}")

print("\n=== Traditional vs AI-Powered Operations ===")
print(f"{'Feature':<25} {'Traditional':<40} {'AI-Powered (AIOps)'}")
print("-" * 105)
for feature in traditional:
    print(f"{feature:<25} {traditional[feature]:<40} {ai_assisted[feature]}")

print("\n=== Recommended Stack for FSS Retail ===")
print("  Prometheus + Grafana (metrics) + Loki (logs) + Robusta (AI alerts) + Claude API (RCA)")
