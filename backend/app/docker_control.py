import docker
from flask import Blueprint, jsonify, request

docker_blueprint = Blueprint("docker_control", __name__)

try:
    client = docker.DockerClient(base_url="unix://var/run/docker.sock")
except Exception as e:
    client = None
    print("⚠️ Docker not available, running in offline mode")
    
@docker_blueprint.route("/containers", methods=["GET"])
def list_containers():
    """List all Docker containers"""
    try:
        containers = client.containers.list(all=True)
        container_list = [
            {
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags,
                "labels": container.labels,
                "uptime": container.attrs["State"]["StartedAt"],
            }
            for container in containers
        ]
        return jsonify(container_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@docker_blueprint.route("/container/<container_id>/start", methods=["POST"])
def start_container(container_id):
    """Start a Docker container"""
    try:
        container = client.containers.get(container_id)
        container.start()
        return jsonify({"status": "started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@docker_blueprint.route("/container/<container_id>/stop", methods=["POST"])
def stop_container(container_id):
    """Stop a Docker container"""
    try:
        container = client.containers.get(container_id)
        container.stop()
        return jsonify({"status": "stopped"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@docker_blueprint.route("/container/<container_id>/restart", methods=["POST"])
def restart_container(container_id):
    """Restart a Docker container"""
    try:
        container = client.containers.get(container_id)
        container.restart()
        return jsonify({"status": "restarted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@docker_blueprint.route("/container/<container_id>/logs", methods=["GET"])
def get_container_logs(container_id):
    """Get logs of a Docker container"""
    try:
        container = client.containers.get(container_id)
        logs = container.logs()
        return jsonify({"logs": logs.decode("utf-8")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@docker_blueprint.route("/container/<container_id>/exec", methods=["POST"])
def exec_command(container_id):
    """Execute a command in a Docker container"""
    try:
        container = client.containers.get(container_id)
        command = request.json.get("command")
        if not command:
            return jsonify({"error": "No command provided"}), 400
        exec_command = client.api.exec_create(container.id, command)
        output = client.api.exec_start(exec_command["Id"])
        return jsonify({"output": output.decode("utf-8")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@docker_blueprint.route("/container/<container_id>/remove", methods=["DELETE"])
def remove_container(container_id):
    """Remove a Docker container"""
    try:
        container = client.containers.get(container_id)
        container.remove(force=True)
        return jsonify({"status": "removed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@docker_blueprint.route("/container/<container_id>/stats", methods=["GET"])
def get_container_stats(container_id):
    """Get stats of a Docker container"""
    try:
        container = client.containers.get(container_id)
        stats = container.stats(stream=False)
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@docker_blueprint.route("/container/<container_id>/inspect", methods=["GET"])
def inspect_container(container_id):
    """Inspect a Docker container"""
    try:
        container = client.containers.get(container_id)
        inspection = container.attrs
        return jsonify(inspection)
    except Exception as e:
        return jsonify({"error": str(e)}), 500