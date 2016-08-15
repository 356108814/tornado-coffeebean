# encoding: utf-8
"""

@author Yuriseus
@create 2016-8-1 18:09
"""
import json

from coffeebean.handler import BaseRequestHandler
from handlers.response_code import ResponseCode


class BaseHandler(BaseRequestHandler):

    def get_url_argument_dict(self, names):
        argument_dict = {}
        for _, name in enumerate(names):
            argument_dict[name] = self.get_argument(name, None)
        return argument_dict

    def get_body_argument_dict(self, names):
        argument_dict = {}
        for _, name in enumerate(names):
            argument_dict[name] = self.get_body_argument(name, None)
        return argument_dict

    def write_response(self, data=None, response_code=None, error_msg_params=None):
        """
        写回客户端的json
        @param data: 返回格式化对象
        @param response_code: ResponseCode属性
        @param error_msg_params: 错误信息参数列表
        """
        response = {}
        if not response_code:
            response_code = ResponseCode.SUCCESS
        if response_code == ResponseCode.SUCCESS:
            response['success'] = True
        else:
            response['success'] = False
        response['errcode'] = response_code.value[0]
        error_msg = response_code.value[1]
        if error_msg_params and (isinstance(error_msg_params, list) or isinstance(error_msg_params, tuple)):
            error_msg = error_msg.format(*error_msg_params)
        response['errmsg'] = error_msg
        if not data:
            data = []
        response['data'] = data
        # 响应类型
        self.set_header('Access-Control-Allow-Methods', 'PUT,POST,GET,DELETE,OPTIONS')
        # 响应头设置
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with,content-type')
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(json.dumps(response, ensure_ascii=False))    # ensure_ascii True为转换为ascii码
