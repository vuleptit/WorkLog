def get_all_users(db: Session):
    users = db.query(User).all()
    message = "Get users successfully"
    data=[]
    for user in users:
        data.append(user.__dict__)
    response = CustomResponse(
        message=message,
        data=data,
        status=status.HTTP_200_OK
    )
    return response