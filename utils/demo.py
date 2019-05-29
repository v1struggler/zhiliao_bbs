from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def alidayu(telephone, captcha):
    client = AcsClient('LTAI1xbBJ5n1iWSW', 'wUXxTEP1zzKawWoVgwYsUCKSZExqQ1', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', telephone)
    request.add_query_param('SignName', "zlbbs论坛")
    request.add_query_param('TemplateCode', "SMS_166665344")
    request.add_query_param('TemplateParam', {"code": captcha})

    response = client.do_action_with_exception(request)
    # response = client.do_action(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))
    return response

# alidayu("13309567820","1234")