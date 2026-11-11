
def validate_server(server):
    """Validate server inventory information."""

    required_fields = ["hostname", "cpu", "memory", "environment"]

    if not isinstance(server, dict):
        return {
            "valid": False,
            "errors": ["Server data must be a dictionary."]
        }

    errors = []

    for field in required_fields:
        if field not in server:
            errors.append(f"Missing required field: {field}")

    if errors:
        return {"valid": False, "errors": errors}

    hostname = server["hostname"]

    if not isinstance(hostname, str) or not hostname.strip():
        errors.append("Hostname must be a non-empty string.")

    try:
        cpu = int(server["cpu"])
        if cpu <= 0:
            errors.append("CPU must be greater than zero.")
    except (ValueError, TypeError):
        errors.append("CPU must be a valid integer.")

    try:
        memory = int(server["memory"])
        if memory <= 0:
            errors.append("Memory must be greater than zero.")
    except (ValueError, TypeError):
        errors.append("Memory must be a valid integer.")

    if errors:
        return {"valid": False, "errors": errors}

    return {
        "valid": True,
        "hostname": hostname,
        "cpu": cpu,
        "memory": memory,
        "environment": server["environment"]
    }


if __name__ == "__main__":
    server = {
        "hostname": "web-server-01",
        "cpu": "4",
        "memory": "16",
        "environment": "production"
    }

    result = validate_server(server)
    print(result)
