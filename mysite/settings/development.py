from .base import *

SECRET_KEY = os.environ['SECRET_KEY']


DEBUG = True

ALLOWED_HOSTS = []


"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite_db',
        'USER': 'maxu',
        'PASSWORD': 'maxu0507',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'  # 用qq邮箱进行发送
EMAIL_PORT = 25  # 端口号
EMAIL_HOST_USER = '1472601637@qq.com'
EMAIL_HOST_PASSWORD = 'xogfahmmoxmbbafa'
EMAIL_SUBJECT_PREFIX = ['LebronMX的博客']
EMAIL_USER_TLS = True