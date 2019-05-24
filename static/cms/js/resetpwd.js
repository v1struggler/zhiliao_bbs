
// 整个页面都加载完成才会执行这个函数$(function ())
$(function () {
    $("#submit").click(function (event) {      //获取提交按钮(通过id的方式获取)，并绑定单击事件，单击后执行function (event)函数

        event.preventDefault();         // 阻止按钮默认的提交表单的事件，通过js异步提交表单

        var oldpwdE = $("input[name=oldpwd]");   //获取标签：拿到name值为oldpwd的input标签
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();             // 获取标签的值
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        // 1. 要在模版的meta标签中渲染一个csrf-token
        // 2. 在ajax请求的头部中设置X-CSRFtoken：这部分代码在zlajax.js中
        zlajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {          //定义回调，data是服务器返回给我们的值
                // console.log(data)
                // code==200、code != 200
                if(data['code'] == 200){
                    zlalert.alertSuccessToast("恭喜！密码修改成功！");
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
                }else{
                    var message = data['message'];
                    zlalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                // console.log(error)
                zlalert.alertNetworkError();
            }
        });
    });
});