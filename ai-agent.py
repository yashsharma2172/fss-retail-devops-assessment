# Task 5: AI-powered EKS troubleshooting agent for FSS Retail App using Claude AI

import subprocess
import anthropic

# Collect pod logs from Kubernetes
def get_logs(pod_name, namespace="murali-ns"):
    result = subprocess.run(
        ["kubectl", "logs", pod_name, "-n", namespace, "--tail=100"],
        capture_output=True, text=True
    )
    return result.stdout

# Collect pod events and describe output
def get_events(pod_name, namespace="murali-ns"):
    result = subprocess.run(
        ["kubectl", "describe", "pod", pod_name, "-n", namespace],
        capture_output=True, text=True
    )
    return result.stdout

# Get all pods status in namespace
def get_pods(namespace="murali-ns"):
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace],
        capture_output=True, text=True
    )
    return result.stdout

# Get K8s events sorted by time
def get_k8s_events(namespace="murali-ns"):
    result = subprocess.run(
        ["kubectl", "get", "events", "-n", namespace, "--sort-by=.lastTimestamp"],
        capture_output=True, text=True
    )
    return result.stdout

# Get deployment rollout history
def get_rollout_history(namespace="murali-ns"):
    result = subprocess.run(
        ["kubectl", "rollout", "history", "deployment/retail-app-deployment", "-n", namespace],
        capture_output=True, text=True
    )
    return result.stdout

# Send data to Claude AI for analysis
def analyze_with_claude(data, scenario):
    client = anthropic.Anthropic(api_key="YOUR_CLAUDE_API_KEY")
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Kubernetes issue: {scenario}\n\nData:\n{data}\n\nFind root cause and provide step-by-step fix."
        }]
    )
    return message.content[0].text

# Scenario 1: Retail App unavailable after deployment
def scenario1_app_unavailable(pod_name):
    print("\n--- Scenario 1: App unavailable after deployment ---")
    pods = get_pods()
    logs = get_logs(pod_name)
    events = get_k8s_events()
    data = f"Pods:\n{pods}\nLogs:\n{logs}\nEvents:\n{events}"
    print(analyze_with_claude(data, "retail app is unavailable after deployment"))

# Scenario 2: Slow checkout response
def scenario2_slow_checkout(pod_name):
    print("\n--- Scenario 2: Customers report slow checkout ---")
    logs = get_logs(pod_name)
    events = get_events(pod_name)
    data = f"Logs:\n{logs}\nEvents:\n{events}"
    print(analyze_with_claude(data, "slow checkout response, high latency reported by customers"))

# Scenario 3: Pods continuously restarting
def scenario3_pod_restart(pod_name):
    print("\n--- Scenario 3: Pods continuously restarting (CrashLoopBackOff) ---")
    logs = get_logs(pod_name)
    events = get_events(pod_name)
    data = f"Logs:\n{logs}\nEvents:\n{events}"
    print(analyze_with_claude(data, "pods restarting CrashLoopBackOff - check resource limits and config"))

# Scenario 4: Production errors increase after new release
def scenario4_errors_after_release(pod_name):
    print("\n--- Scenario 4: Production errors increased after new release ---")
    logs = get_logs(pod_name)
    history = get_rollout_history()
    events = get_k8s_events()
    data = f"Deployment history:\n{history}\nError logs:\n{logs}\nEvents:\n{events}"
    print(analyze_with_claude(data, "production errors increased after new release, possible regression"))

# Main
if __name__ == "__main__":
    pod = "retail-app-deployment-abc123"
    scenario1_app_unavailable(pod)
    scenario2_slow_checkout(pod)
    scenario3_pod_restart(pod)
    scenario4_errors_after_release(pod)
