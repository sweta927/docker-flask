from flask import Blueprint, request, jsonify

from project import database
from project.helpers.auth import is_authenticated
from project.models.project import Project

project_bp = Blueprint("project_bp", __name__)


@project_bp.route("/add", methods=["POST"])
@is_authenticated
def add_project(curr_user):
    data = request.get_json()

    project_name = data["project_name"].strip()
    sampling_type = data["sampling_type"].strip()
    description = data["description"].strip()
    instructions = data["instructions"].strip()

    try:
        database.add_instance(
            Project,
            project_name=project_name,
            sampling_type=sampling_type,
            description=description,
            instructions=instructions,
            created_by=curr_user.id,
        )
        return jsonify(message=f"New Project {project_name} added"), 201
    except Exception as e:
        return jsonify(error=f"Something went wrong during Project Adding. ({e})"), 406


@project_bp.route("/details")
def all_details():
    """All Project Details."""
    try:
        data = database.get_all(Project)
        print("data", data)
        return jsonify(data=data, message="All Project Details"), 200
    except Exception as e:
        print("Error:", e)
        return jsonify(error=f"Having Some Issues find Project Details. ({e})"), 400


@project_bp.route("/details/<int:project_id>")
def project_details(project_id):
    """Project Details By Id"""
    try:
        data = database.get_filter_by(Project, id=project_id)
        return jsonify(data=data, message="Project Details"), 200
    except Exception as e:
        return jsonify(error=f"Project Details Not Found. ({e})"), 400


@project_bp.route("/details/created_by/<int:created_by>")
def project_details_created_by(created_by):
    """Project Details By Id"""
    try:
        data = database.get_filter_by(Project, created_by=created_by)
        return jsonify(data=data, message="Project Details"), 200
    except Exception as e:
        return jsonify(error=f"Project Details Not Found. ({e})"), 400


@project_bp.route("/edit/<int:project_id>", methods=["PUT"])
@is_authenticated
def project_edit(project_id, curr_user):
    """Edit Project Details by Id"""
    data = request.get_json()

    project_name = data["project_name"].strip()
    sampling_type = data["sampling_type"].strip()
    description = data["description"].strip()
    instructions = data["instructions"].strip()

    try:
        project_data = database.get_filter_by(Project, id=project_id)
        if not project_data:
            return (
                jsonify(error="Project not found with id '{}'".format(project_id)),
                404,
            )
        if project_data.created_by == curr_user.id:
            database.edit_instance(
                Project,
                id=project_id,
                project_name=project_name,
                sampling_type=sampling_type,
                description=description,
                instructions=instructions,
            )
            return (
                jsonify(message=f"Project '{project_name}' Updated successfully"),
                200,
            )
        return (
            jsonify(
                error=f"'{curr_user.uname}' You have no Authority on Project '{project_data.project_name}'"
            ),
            401,
        )
    except Exception as e:
        return jsonify(error=f"Updation Failed. ({e})"), 400


@project_bp.route("/remove/<int:project_id>", methods=["DELETE"])
@is_authenticated
def project_remove(project_id, curr_user):
    """Remove Project by Id"""

    try:
        project_data = database.get_filter_by(Project, id=project_id)
        if not project_data:
            return (
                jsonify(error="Project not found with id '{}'".format(project_id)),
                404,
            )
        if project_data.created_by == curr_user.id:
            database.delete_instance(
                Project,
                id=project_id,
            )
            return (
                jsonify(
                    message=f"Project '{project_data.project_name}' Removed successfully"
                ),
                200,
            )
        return (
            jsonify(
                error=f"'{curr_user.uname}' You have no Authority on Project '{project_data.project_name}'"
            ),
            401,
        )
    except Exception as e:
        return jsonify(error=f"Updation Failed. ({e})"), 400
