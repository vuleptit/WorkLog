from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import exc
from model.project import *
from business_rules.view_models.project_dto import *
from api.utils.custom_response import CustomResponse
from fastapi import status

def get_all_projects(db: Session):
    projects = db.query(Project).all()
    message = "Successful"
    response = CustomResponse(
        message=message,
        data=projects,
        status=status.HTTP_200_OK
    )
    return response

def get_project_by_id(db: Session, project_id: int):
    try:
        project= db.query(Project).where(Project.id == project_id).first()
    
        if project is not None:
            return CustomResponse(
                message = "Successfully",
                data = project.__dict__,
                status = status.HTTP_200_OK
            )
        else:
            return CustomResponse(
                message = f"Project with id {project_id} does not exist",
                status = status.HTTP_400_BAD_REQUEST
            )
    except Exception as ex:
        print(ex)
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)

def update_project(db: Session, project_data: ProjectUpdate):
    try:
        project_in_db = db.query(Project).where(Project.id == project_data.id).first()
        if project_in_db is None:
            return CustomResponse(
                message = "Failed",
                exception = f"Project with id {project_data.id} does not exist",
                status = status.HTTP_400_BAD_REQUEST
            )
        update_fields = project_data.dict()
        for field in update_fields.keys():
            setattr(project_in_db, field, getattr(project_data, field))
        db.commit()
        db.refresh(project_in_db)
        response = CustomResponse(
            message = "Successfully",
            data = project_in_db.__dict__,
            status = status.HTTP_201_CREATED
        )
        return response
    except exc.IntegrityError:
        print(sys.exc_info())
        return CustomResponse(
            message = "Failed",
            status = status.HTTP_404_NOT_FOUND,
            exception = f"Project with name {project_data.name} already existed"
        )
    except Exception as ex:
        print(sys.exc_info())
        print(ex)
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)


def create_project(db: Session, project_data: ProjectCreate):
    try:
        project_item = Project()
        create_fields = list(ProjectCreate.__fields__.keys())
        for field in create_fields:
            setattr(project_item, field, getattr(project_data, field))
        db.add(project_item)
        db.commit()
        db.refresh(project_item)
        response = CustomResponse(
            message = "Successfully",
            data = project_item.__dict__,
            status = status.HTTP_200_OK
        )
        return response
    except exc.IntegrityError:
        response = CustomResponse(
            message = "Failed",
            status = status.HTTP_404_NOT_FOUND,
            exception = f"project with name {project_data.name} already exist"
        )
        return response
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)

def delete_project(db: Session, project_id: int):
    try:
        project_query = db.query(Project).where(Project.id == project_id).first()
        if project_query is None:
            return CustomResponse(
                message = "Failed",
                status = status.HTTP_404_NOT_FOUND,
                exception = f"project with id {project_id} does not exist"
            )
        db.delete(project_query)
        db.commit()
        return CustomResponse(
                message = "Succesfully",
                status = status.HTTP_200_OK,
            )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)
        
    