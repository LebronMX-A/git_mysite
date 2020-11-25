from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False
ALLOWED_HOSTS = ['*']

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}"""
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite_db',
        'USER': 'maxu',
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'  # 用qq邮箱进行发送
EMAIL_PORT = 465  # 端口号
EMAIL_HOST_USER = '1472601637@qq.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_SUBJECT_PREFIX = ['LebronMX的博客']
EMAIL_USER_TLS = True

ADMINS = (
    ('admin', '1472601637@qq.com'), # 元组：管理员名称、邮箱
)

# 日志文件
LOGGING = {
    'version': 1, # 版本，自己命名
    'disable_existing_loggers': False, # 是否禁用已经存在的记录器
    'handlers': {   # 处理器
        'file': {   # 把日志写到一个文件里面
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/mysite_debug.log',    # 指定目录，
        },
        'mail_admins': {    # 发送邮件给管理员
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {    #日志记录器
        'django': {
            'handlers': ['file'],   # 启用‘file’这个处理器
            'level': 'DEBUG',   # 级别
            'propagate': True,  # 日志记录完之后，需不需要继续往上传递（DEBUG-->DEFAULT-->WARNING-->ERROR)
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}