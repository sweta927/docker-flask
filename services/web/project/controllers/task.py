from flask import Blueprint, request, jsonify

from project import database
from project.helpers.auth import is_authenticated
from project.models.task import Task
from project.models.project import Project

task_bp = Blueprint("task_bp", __name__)


@task_bp.route("/add", methods=["POST"])
@is_authenticated
def add_task(curr_user):
    try:
        data = request.get_json()

        if not ("project_id" in data and "title" in data and "comment" in data):
            return jsonify(error="Please Provide Proper data"), 400

        project_id = data["project_id"].strip()
        title = data["title"].strip()
        comment = data["comment"].strip()

        project_data = database.get_filter_by(Project, id=project_id)
        if not project_data:
            return jsonify(error="Project not found, for given project_id."), 401
        database.add_instance(
            Task,
            project_id=project_id,
            title=title,
            comment=comment,
            created_by=curr_user.id,
        )
        return (
            jsonify(
                message=f"Task Added successfully, for Project {project_data.project_name}"
            ),
            201,
        )
    except Exception as e:
        return jsonify(error=f"Adding task failed. {e}"), 400


@task_bp.route("/project/<int:project_id>")
@is_authenticated
def get_task_by_project_id(project_id, curr_user):
    try:
        args = request.args.to_dict()
        # created_by = args.get("created_by")

        project_data = database.get_filter_by(Project, id=project_id)

        if not project_data:
            return jsonify(error=f"Project {project_id} not found"), 404

        if project_data.created_by != curr_user.id:
            return jsonify(
                error=f"User:({curr_user.uname}) not have rights on Project:({project_data.project_name})"
            ), 401

        task_data = database.get_filter_all(Task, project_id=project_id, **args)

        if not task_data:
            return jsonify(error=f"NO Task Found with Filteration"), 404

        return jsonify(data=task_data), 200
    except Exception as e:
        return jsonify(error=f"Tasks Not Found. ({e})"), 400


@task_bp.route("/status/<int:task_id>", methods=["PUT"])
@is_authenticated
def update_task_status(task_id, curr_user):
    try:

        data = request.get_json()

        task_data = database.get_filter_by(Task, id=task_id)

        if not task_data:
            return jsonify(error=f"NO Task Found. {task_id}"), 404

        if task_data.created_by != curr_user.id:
            return (
                jsonify(
                    error=f"You ({curr_user.uname}) are not allowed to Update Task:{task_id}."
                ),
                403,
            )

        status = data["status"].lower()

        database.edit_instance(Task, id=task_id, status=status)

        return jsonify(message=f"Task:{task_id} has been updated"), 200

    except Exception as e:
        return jsonify(error=f"Task Updation Failed. ({e})"), 400
