import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SECRET_KEY = 'just guess it '
	MAIL_SUBJECT_PREFIX = '我的博客'
	MAIL_SENDER = '博客管理员<793673704@qq.com>'
	

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://wyq:1234567@127.0.0.1:3306/myflask'
	MAIL_SERVER = 'smtp.qq.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USE_TSL = False
	MAIL_USERNAME = '793673704@qq.com'
	MAIL_PASSWORD = 'vqoahnfogetubebc'

class TestingConfig(Config):
	TESTING = True

class ProductionConfig(Config):
	pass	
config = {
		'development': DevelopmentConfig,
		'test': TestingConfig,
		'production': ProductionConfig,

		'default': DevelopmentConfig
		}
