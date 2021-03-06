from flask import request, jsonify
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import create_access_token
from operator import itemgetter

users_urls_list = [
    # {"id": "10", "url": "Н6икита12"}
]


def abort_if_todo_doesnt_exist(user_id):
    if user_id not in users_urls_list:
        abort(404, message="users_list {} doesn't exist".format(user_id))


parser = reqparse.RequestParser()
parser.add_argument('range')
parser.add_argument('filter')
parser.add_argument('sort')


def format_list(list_response):
    args = parser.parse_args()
    length = len(list_response)

    # filter_of_list = args['filter']
    # if filter_of_list:
    #     filter_of_list = args['filter'].replace('[', '').replace(']', '').replace('\"', '')

    sort_of_list = args['sort']
    if sort_of_list:
        sort_of_list = sort_of_list.replace('[', '').replace(']', '').replace('\"', '').split(',')
        sort_key = sort_of_list[0]
        order = False
        if sort_of_list[1] != 'ASC':
            order = True
        list_response = sorted(list_response, key=itemgetter(sort_key), reverse=order)

    range_of_list = args['range']
    section_start, section_end, section_of_list = 0, 0, []
    if range_of_list:
        range_of_list = range_of_list.replace('[', '').replace(']', '').split(',')
        section_start, section_end = tuple(map(int, range_of_list))
        section_of_list = list_response[section_start: section_end]

    str_content_range = f'{section_start}-{section_end}/{length}'
    return str_content_range, section_of_list


class AdminLogin(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']
        if username == 'admin' and password == 'admin':
            access_token = create_access_token(identity={
                'role': 'admin',
            }, expires_delta=False)
            result = {'token': access_token}
            return result
        return {'error': 'Invalid username and password'}


class AdminUsersList(Resource):
    def get(self):
        str_content_range, section_of_list = format_list(users_urls_list)
        response = jsonify(section_of_list)
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        # response.headers.add('Access-Control-Allow-Origin', ' http://localhost:3001')
        # response.headers.add('content-type', 'application/json')
        # response.headers.add('Access-Control-Allow-Headers', 'content-range')
        response.headers.add('Access-Control-Expose-Headers', 'content-range')

        # str_content_range = content_range(users_list)
        response.headers.add('content-range', f'users {str_content_range}')
        return response

    def post(self):
        pass
        # args = parser.parse_args()
        # todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        # todo_id = 'todo%i' % todo_id
        # TODOS[todo_id] = {'task': args['task']}
        # return TODOS[todo_id], 201
