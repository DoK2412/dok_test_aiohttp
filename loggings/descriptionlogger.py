logger_config = {
    'version': 1,
    'formatters': {
        'formatting_info': {'format': '{asctime} - {msecs} - {funcName} - {levelname} - {message}',
                              'style': '{'},
        'formatting-error': {'format': '{asctime} - {msecs} - {funcName} - {levelname} - {message}',
                              'style': '{'}
    },
    'handlers': {
        'info': {
            'class': 'logging.FileHandler',
            'filename': 'loggings/info.log',
            'mode': 'a',
            'level': 'INFO',
            'formatter': 'formatting_info'
        },
        'error': {
            'class': 'logging.FileHandler',
            'filename': 'loggings/error.log',
            'mode': 'a',
            'level': 'ERROR',
            'formatter': 'formatting-error'
        }

    },

    'loggers': {
        'app_info': {
            'level': 'INFO',
            'handlers': ['info'],
            'propagate': False
        },
        'app_error': {
            'level': 'ERROR',
            'handlers': ['error'],
            'propagate': False
        }
    },

    'disable_existing_loggers': False,
    'filters': {},
}
