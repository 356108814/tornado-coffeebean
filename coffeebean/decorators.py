# encoding: utf-8
"""
公共装饰器
@author Yuriseus
@create 2016-5-11 14:59
"""
import json

from .cache import cache
from .valid.validate import ValidateForm
from .valid.validate import ValidateParam


def cacheable(timeout=60):
    """
    缓存装饰器，在service层
    示例：@cacheable(timeout=CacheType.DEFAULT, key="user_info")
    如果key为None,则根据函数名称、参数自动生成key
    """
    def handle_func(func):
        def wrapper(*args, **kwargs):
            func_name = str(func.__name__)
            cache_key = _gen_cache_key(func_name, args, kwargs)
            if cache.has_key(cache_key):
                result = cache.get(cache_key)
            else:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout=timeout)
            return result
        return wrapper
    return handle_func


def _gen_cache_key(func_name, args, kwargs):
    key_rule = '{0}_{1}_{2}'
    arg_list = []
    for index, arg in enumerate(args):
        if index > 0:    # 第一个参数为类对象
            arg_list.append(str(arg))
    kwargs_list = []
    for key in kwargs:
        kwargs_list.append(str(kwargs[key]))
    return key_rule.format(func_name, '_'.join(arg_list), '_'.join(kwargs_list))


validate_param = ValidateParam()
validate_form = ValidateForm()


def valid(cfg, is_body_arg=False):
    """
    数据验证器，在handler层，在service不再验证参数
    示例：@valid(cfg={'age': 'int'})
    @param cfg验证配置,dict类型
    @param is_body_arg 是否为请求体参数
    """
    def handle_func(func):
        def wrapper(*args, **kwargs):
            if not cfg:
                pass
            else:
                request_handler = None
                for index, arg in enumerate(args):
                    if index == 0:    # 第一个参数为类对象
                        request_handler = arg
                param_dict = {}
                for param_name in cfg:
                    if is_body_arg:
                        param_dict[param_name] = request_handler.get_body_argument(param_name, None)
                    else:
                        param_dict[param_name] = request_handler.get_argument(param_name, None)
                is_valid, error_msg = validate_form.is_valid(param_dict, cfg)
                if is_valid:
                    return func(*args, **kwargs)
                else:
                    response = {'success': False, 'errcode': 'INVALID_ARGUMENTS', 'error_msg': error_msg}
                    request_handler.finish(json.dump(response))
        return wrapper
    return handle_func


if __name__ == '__main__':
    print('{0}_{1}_{2}'.format(1, 2, 3))
