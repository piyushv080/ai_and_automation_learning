
"""
Day 001 - Server Resource Validation

Validates server information received from an infrastructure API.
"""

def validate_server(server):
    """Validate server information and return validation results."""

    errors = []

    # 1. Check required fields
    required_fields = ["hostname", "cpu", "memory", "environment"]

    for field in required_fields:
        if field not in server:
            errors.append(f"Missing required field: {field}")

    if errors:
        return False, errors

    # 2. Extract hostname
    hostname = server["hostname"]

    if not isinstance(hostname, str) or not hostname.strip():
        errors.append("Hostname must be a non-empty string.")

    # 3. Convert CPU and memory to integers
    try:
        cpu = int(server["cpu"])
    except (ValueError, TypeError):
        cpu = None
        errors.append("CPU must be a valid integer.")

    try:
        memory = int(server["memory"])
    except (ValueError, TypeError):
        memory = None
        errors.append("Memory must be a valid integer.")

    # 4. Validate resource values
    if cpu is not None and cpu <= 0:
        errors.append("CPU must be greater than zero.")

    if memory is not None and memory <= 0:
        errors.append("Memory must be greater than zero.")

    # 5. Validate environment
    valid_environments = ["development", "testing", "production"]

    environment = server["environment"]

    if environment not in valid_environments:
        errors.append("Environment must be development, testing, or production.")

    if errors:
        return False, errors

    result = {
        "hostname": hostname.strip(),
        "cpu": cpu,
        "memory": memory,
        "environment": environment
    }

    return True, result


def main():
    # Example input from the challenge
    server = {
        "hostname": "web-server-01",
        "cpu": "4",
        "memory": "16",
        "environment": "production"
    }

    is_valid, result = validate_server(server)

    print("Server Resource Validation")
    print("-" * 35)

    if is_valid:
        print("Validation successful!")
        print(f"Hostname: {result['hostname']}")
        print(f"CPU: {result['cpu']}")
        print(f"Memory: {result['memory']} GB")
        print(f"Environment: {result['environment']}")
    else:
        print("Validation failed!")

        for error in result:
            print(f"- {error}")


if __name__ == "__main__":
    main()
