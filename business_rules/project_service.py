from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import exc
from model.project import *
from business_rules.view_models.project_dto import *
from api.utils.custom_response import CustomResponse
from fastapi import status, Form
from .jwt_services import get_password_hash

def get_all_projects(db: Session):
    projects = db.query(Project).all()
    message = "Get projects successfully"
    response = CustomResponse(
        message=message,
        data=projects,
        status=status.HTTP_200_OK
    )
    return response

def get_project_by_id(db: Session, project_id: int):
    try:
        project_query = db.query(Project).where(project.id == project_id).first()
        project = project_query.__dict__
        message = "Get project successfully"
        response = CustomResponse(
            message = message,
            data = project,
            status = status.HTTP_200_OK
        )
        return response
    except Exception as ex:
        message = "Get project failed"
        exception = "project with given id does not exist"
        response = CustomResponse(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response

def update_project(db: Session, project_data: ProjectBase):
    try:
        project_in_db = db.query(Project).where(project_data.id == project_data.id).first()
        if project_in_db is not None:
            update_fields = ["email", "password", "phone", "project_name", "is_active"]
            for field in update_fields:
                setattr(project_in_db, field, getattr(project_data, field))
        else:
            raise ProjectDoesNotExist
        db.commit()
        db.refresh(project_in_db)
        message = "Udpate project successfully"
        response = CustomResponse(
            message = message,
            data = project_in_db.__dict__,
            status = status.HTTP_201_CREATED
        )
        return response
    except exc.SQLAlchemyError:
        message = "Update project failed"
        exception = f"project with email {project_data.email} already exist"
        response = CustomResponse(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response
    except Exception as ProjectDoesNotExist:
        message = "Update project failed"
        exception = f"project with given id {project_data.id} does not exist"
        response = CustomResponse(
            message = message,
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            exception = exception
        )
        return response

def create_project(db: Session, project_data: ProjectBase):
    try:
        project_item = project()
        create_fields = ["email", "phone", "project_name", "is_active", "is_admin"]
        project_item.password = get_password_hash(project_data.password)
        for field in create_fields:
            setattr(project_item, field, getattr(project_data, field))
        db.add(project_item)
        db.commit()
        db.refresh(project_item)
        project = project_item.__dict__
        message = "Create project successfully"
        response = CustomResponse(
            message = message,
            data = project,
            status = status.HTTP_200_OK
        )
        return response
    except Exception as ex:
        message = "Create project failed"
        exception = f"project with email {project_data.email} already exist"
        response = CustomResponse(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response


def delete_project(db: Session, project_id: int):
    try:
        project_query = db.query(Project).where(Project.id == project_id).first()
        db.delete(project_query)
        db.commit()
        project_in_db = get_project_by_id(db=db, project_id=project_id)
        if project_in_db.data is None:
            message = "Delete project successfully"
            response = CustomResponse(
                    message = message,
                    status = status.HTTP_200_OK
            )
            return response
        else:
            raise DeleteProjectException
    except Exception as DeleteProjectException:
        message = "Deleted project failed"
        exception = f"project id {project_id} does not exist"
        response = CustomResponse(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response
        
    