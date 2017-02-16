/**
 * Created by Administrator on 2017/2/16.
 */
        function loadScript(url, callback)
        {
            // Adding the script tag to the head as suggested before
            var head = document.getElementsByTagName('head')[0];
            var script = document.createElement('script');
            script.type = 'text/javascript';
            script.src = url;

            // Then bind the event to the callback function.
            // There are several events for cross browser compatibility.
            script.onreadystatechange = callback;
            script.onload = callback;

            // Fire the loading
            head.appendChild(script);
        }

        var myPrettyCode = function() {


              initArticleData();
           // Here, do what ever you want
        };
         toastr.options = {
          "closeButton": true,
          "debug": false,
          "newestOnTop": false,
          "progressBar": true,
          "positionClass": "toast-top-center",// 这个position 他喵的用center 结果放在左下角 我也是醉了 后来发现原先他的css比较老 自己加也行
          "preventDuplicates": false,
          "onclick": null,
          "showDuration": "300",
          "hideDuration": "1000",
          "timeOut": "3000",
          "extendedTimeOut": "1000",
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut"
        };
    $('#warning-block').hide();

    function get(id) {
            return document.getElementById(id);
        }
    function getUrlVars()
        {
            var vars = [], hash;
            var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
            for(var i = 0; i < hashes.length; i++)
            {
                hash = hashes[i].split('=');
                vars.push(hash[0]);
                vars[hash[0]] = hash[1];
            }
            return vars;
        }
               // {# 我之所以在此写js 是因为当时我发现写在index.js 无法被加载 我当时认为
               //  是因为js 单线程运行 无法调用的结果 虽然我个人觉得写在首页 真他妈的丑#}
   function post_comment() {
        var comment=document.getElementById('comment').value;
        var item_id=getUrlVars()['item'];
        console.log(typeof comment);

        var data={content:comment};

        query_post_cmd='/api/blogs/'+item_id+'/comment';
        $.ajax({
            method:'post',
            url:query_post_cmd,
            dataType:'text',
            data:data,
            success:function (resp) {
                if (JSON.parse(resp)['status']){
                    toastr["success"]("评论成功");
                    location.reload();
                    // 不好意思 我已经放弃这个傻逼 的js 了 原因是我打算重新刷新我原先的评论数据 但是由于写的js 不规范 导致页面死循环 下次重构
                    // loadScript("/static/js/index.js", myPrettyCode);

                }
                else if (JSON.parse(resp)['message']){
                    toastr["error"](JSON.parse(resp)['message'])
                }
            }
        })
    }
           // {# 2017.2.14 吃晚饭的时候我发现 我仅仅过滤了 评论 而用户名也会成为
           //  hack xss 胡乱弹框的场地，因此我认为 设定三道防线： 1. 注册时候 检测特殊字符
           //  2. 后台过滤 3.前端js 再过滤 （好吧 实际上除了第一个其他两个都蛮靠谱的）#}
    function check_reg(object) {
        var former_str=object.getAttribute("placeholder");
        $(':password').keypress(function(e) {
            var s = String.fromCharCode( e.which );
            if ( s.toUpperCase() === s && s.toLowerCase() !== s && !e.shiftKey ) {
            get("warning-block").innerHTML=' 大写按钮已经打开 ';
             }
            });
        if (object.value.length==0){
            get("warning-block").innerHTML=former_str+'不得为空';
            $('#warning-block').show();

        }
        //我他妈也是醉了 0<object.value.length<3 这样写居然是或运算 傻逼玩儿 js 你咋不上天呢
        else if(object.value.length<3){
            get("warning-block").innerHTML=former_str+'不小于3';
            $('#warning-block').show();

        }
        else if(object.value.length>3){
            $('#warning-block').hide()
        }

    }
    function check_pwd(object) {
        if (get("password1").value!=object.value){
            get("warning-block").innerHTML='两次密码不一致';

        }



    }

    function fuck_register() {
        var new_email=(get('email').value).trim().toLowerCase();
        var new_username=(get('user_name').value).replace('<', '&lt;').replace('>', '&gt;');
        var new_password=CryptoJS.SHA1(new_email+':'+(get('password2').value)).toString();
        if (new_email.length<3 || new_username.length<3){
            get("warning-block").innerHTML=' Fu*k u Do not test safe ';
        }
        else{
            var data={email:new_email,
            password:new_password,
            name:new_username};
            $.ajax({
                method: 'post',
                url: '/api/users',
                dataType: 'text',
                // 用户名和密码
                data: data,
                success: function (resp) {
                    if (JSON.parse(resp)["email"]) {
                        toastr["success"]("注册成功");
                        location.reload();
                    }
                    else if(JSON.parse(resp)['message']){
                        toastr["error"](JSON.parse(resp)['message'])
                    }
                }
            })
            }




    }