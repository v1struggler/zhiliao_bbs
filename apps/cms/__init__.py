# 后台

from .views import bp
# import的方式导入模块，必须是全路径
import apps.cms.hooks  # 初始化的时候就导入钩子函数，不然钩子函数和其他模块没有关联，就没有办法执行；
