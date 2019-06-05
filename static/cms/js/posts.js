

$(function () {
    $(".highlight-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = tr.attr("data-highlight");
        var url = "";
        if(parseInt(highlight)){
            url = "/cms/uhpost/";
        }else{
            url = "/cms/hpost/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'post_id': post_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertSuccessToast('操作成功！');
                    setTimeout(function () {        // 延迟执行这样可以加载提示框，不然立马就重新加载了
                        window.location.reload();
                    },500);
                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});