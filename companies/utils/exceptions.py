from rest_framework.exceptions import APIException

class NotFuondEmployee (APIException):
    status_code = 404
    default_detail = 'Funcionário não encontrado'
    default_code = 'not_found_employee'
    
class NotfoundGroup(APIException):
    status_code = 404
    default_detail = 'O grupo não foi encontrado'
    default_code = 'not_found_group'

class RequiredFields(APIException):
    status_code = 400
    default_detail = 'Enviei os campos no padrão correto'
    default_code = 'error_requiredd_field'
    
class NotFoundtaskStattus(APIException):
    status_code=404
    default_detail='Status da tarefa não foi encontrada'
    default_code='not_found_status'

class NotFoundTask(APIException):
    status_code = 404
    default_detail = 'Tarefa não encontrada'
    default_code ='not_found_task'