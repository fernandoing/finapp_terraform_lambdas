from expenses_entities import Expense
from expenses_persistence import ExpenseRepositoryImplementation as Repository
from pymysql import MySQLError

import jwt
import os


def handler(event, context):
    rds_host = os.environ['RDS_HOST']
    name = os.environ['RDS_USERNAME']
    password = os.environ['RDS_PASSWORD']
    db_name = os.environ['RDS_DB_NAME']
    db_port = os.environ['RDS_PORT']
    secret_key = os.environ['SECRET_KEY']

    token = event['Authorization'].split(' ')[1]

    token_data = jwt.decode(token, secret_key, algorithms=["HS256"])

    user_id = token_data.get('user_id')

    body: dict = event['expense']

    entity = Expense(
        expense_name=body['expense_name'],
        expense_amount=body['expense_amount'],
        month_year=body['month_year'],
        exp_category_id=body['exp_category_id'],
        user_id=user_id
    )

    try:
        expense_id = Repository(
            host=rds_host,
            db_port=int(db_port),
            user=name,
            password=password,
            db_name=db_name
        ).add(entity)
    except MySQLError:
        return {
            'error': 'Internal server error'
        }

    return {
        'expense_id': expense_id
    }
