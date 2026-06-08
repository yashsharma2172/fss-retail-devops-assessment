# Task 5: AI-powered Kubernetes troubleshooting agent using OpenRouter

import os
import subprocess
import time
from openai import OpenAI


# Collect kubectl logs for a pod
def get_logs(pod_name, namespace="retail"):
    result = subprocess.run(
        ["kubectl", "logs", pod_name, "-n", namespace, "--tail=100"],
        capture_output=True,
        text=True
    )
    return result.stdout


# Collect pod events and status details
def get_events(pod_name, namespace="retail"):
    result = subprocess.run(
        ["kubectl", "describe", "pod", pod_name, "-n", namespace],
        capture_output=True,
        text=True
    )
    return result.stdout


# Get all pods in namespace
def get_pods(namespace="retail"):
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace],
        capture_output=True,
        text=True
    )
    return result.stdout


# Get recent K8s events sorted by time
def get_k8s_events(namespace="retail"):
    result = subprocess.run(
        ["kubectl", "get", "events", "-n", namespace, "--sort-by=.lastTimestamp"],
        capture_output=True,
        text=True
    )
    return result.stdout


# Analyze logs/events with OpenRouter
def analyze_with_ai(logs, events, scenario):

    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable is not set."
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    prompt = f"""
You are a Kubernetes SRE expert.

Scenario:
{scenario}

Pod Logs:
{logs[:4000]}

Pod Events:
{events[:4000]}

Analyze the issue and provide:

1. Root Cause
2. Impact
3. Step-by-Step Remediation
4. Preventive Measures

Keep the answer concise and practical.
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# Scenario 1: Pod continuously restarting
def troubleshoot_pod_restart(pod_name):
    print(f"\n--- Scenario 1: Pod {pod_name} is restarting ---")

    logs = get_logs(pod_name)
    events = get_events(pod_name)

    analysis = analyze_with_ai(
        logs,
        events,
        "Pod is continuously restarting / CrashLoopBackOff"
    )

    print(analysis)


# Scenario 2: High latency after deployment
def troubleshoot_high_latency(pod_name):
    print(f"\n--- Scenario 2: High latency detected for {pod_name} ---")

    logs = get_logs(pod_name)
    events = get_events(pod_name)

    analysis = analyze_with_ai(
        logs,
        events,
        "Application latency increased after deployment"
    )

    print(analysis)


# Scenario 3: Deployment failed
def troubleshoot_deployment_failure(namespace="retail"):
    print(f"\n--- Scenario 3: Deployment failed in {namespace} ---")

    events = get_k8s_events(namespace)
    pods = get_pods(namespace)

    analysis = analyze_with_ai(
        pods,
        events,
        "Deployment failed in Kubernetes"
    )

    print(analysis)


# Main
if __name__ == "__main__":

    try:
        pod = subprocess.run(
            [
                "kubectl",
                "get",
                "pods",
                "-n",
                "retail",
                "-l",
                "app=userprofile",
                "-o",
                "jsonpath={.items[0].metadata.name}"
            ],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

    except Exception:
        pod = ""

    if not pod:
        print(
            "No active userprofile pods found in retail namespace. "
            "Using fallback pod name."
        )
        pod = "userprofile-rollout"

    troubleshoot_pod_restart(pod)

    print("\n[Waiting 2 seconds...]")
    time.sleep(2)

    troubleshoot_high_latency(pod)

    print("\n[Waiting 2 seconds...]")
    time.sleep(2)

    troubleshoot_deployment_failure()
