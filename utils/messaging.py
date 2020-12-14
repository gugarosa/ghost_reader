def handler_error(task_type):
    """
    """

    # Defines a response object to output
    res = {
        'error': f'Failed to add a {task_type} task to the pool.'
    }

    return res

def handler_success(task_type):
    """
    """

    # Defines a response object to output
    res = {
        'success': f'A new {task_type} task has been added to the pool.'
    }

    return res
