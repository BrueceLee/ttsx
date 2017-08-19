# coding:utf-8
# 定义中间件
class UrlMiddleware():

    def process_request(self,request):

        # 排除不需要记录url路径的几个页码
        if request.path not in ['/user/register/',
                                '/user/register_handle/',
                                '/user/register_valid/',
                                '/user/login/',
                                '/user/login_handle/',
                                '/user/logout/',
                                '/user/login/',
                                '/user/islogin/',
                                ]:
            request.session['url_path'] = request.get_full_path()