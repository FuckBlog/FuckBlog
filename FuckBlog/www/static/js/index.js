/**
 * Created by Administrator on 2017/1/15.
 */

$(function fuckinit() {
    var art_html = '';
    initArticleData();
    // fuckinit().initArticleData=initArticleData();

    function getLocalTime(nS) {
        return new Date(parseInt(nS) * 1000).toLocaleString().replace(/:\d{1,2}$/,' ');
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
    add_tag();
    function add_tag() {
        $.getJSON('/api/tags',function (tag_data) {
            tags=tag_data['tags'];
            // console.log(tags);
            for(var i=0,dLen=tags.length;i<dLen;i++) {

                var tag=document.createElement("li");
                // console.log(getUrlVars()['tag']);
                if (getUrlVars()['tag'] && encodeURI(tags[i].tag)==getUrlVars()['tag']){
                    tag.setAttribute('class','active');
                    $('ul li:first-child').removeAttr('class')
                }
                else {
                    tag.setAttribute('class','')
                }

                tag.role='presentation';
                var url_tag=document.createElement("a");
                url_tag.href='/index.html?tag='+tags[i].tag;
                url_tag.innerHTML=tags[i].tag;
                // var node=document.createTextNode(tags[i].tag);
                tag.appendChild(url_tag);
                $('#nav-bar').append(tag);
                // document.getElementById('nav-bar').appendChild(tag)
            }
        })
    }    
    function copy_tail(TailString){
          new_art_html=TailString+'<footer class="footer" >'+
    	'<span class="footer__copyright">本站点采用<a href="http://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">知识共享 署名-非商业性使用-相同方式共享 4.0 国际 许可协议</a></span>'+
		'<span class="footer__copyright">本站由 <a href="http://www.songluyi.com">FuckBlog</a> 创建，学习'+'<a href="https://onevcat.com/" target="_blank">OneVs Den</a>的博客主题，您可以在 GitHub 上找到该主题<a href="https://github.com/onevcat/OneV-s-Den" target="_blank">开源代码</a> - © 2016</span>'+
	'</footer>' ;
         $('#article_list').append(new_art_html);
    }
    function initArticleData() {
         new_art_html='';
        // 文章页面请求
        if (getUrlVars()['page']){
            query_cmd='/api/blogs?page='+getUrlVars()['page']
        }
        else if (getUrlVars()['tag']){
            query_cmd='api/blogs?tag='+getUrlVars()['tag'];
            // add_tag();
            $('ul li:first-child').removeAttr('class');
            // var click_tag=$('ul.nav li');
            // click_tag.each(function check_tag() {
            //     console.log($(this).text());
            //     if (encodeURI($(this).text())==getUrlVars()['tag']){
            //         $(this).addClass('active');
            //         $(this).siblings().removeAttr('class');
            //
            //     }
            // })

        }
        else{
            query_cmd='/api/blogs'
        }

        // 具体文章请求

            // 注意一下： js 修改全局变量作用域的事情
        if (getUrlVars()['item']){
            item_query_cmd='/api/blogs/'+getUrlVars()['item'];
            $.getJSON(item_query_cmd,function(item_data){
                essay_data=item_data['blogs'];
                comment_data=item_data['comments'];
                console.log(typeof(comment_data));
                document.title=essay_data.blog_title;
                item_html='<h1 class="post-title">'+essay_data.blog_title+'</h1>'+
                    '<div class="post-meta">'+
                        '<time class="post-list__meta--date date">'+getLocalTime(essay_data.created_time)+'</time>'+
                         '<span class="post-list__meta--tags tags">'+
                    '<a href="'+'/index.html?tag='+essay_data.tag+'">'+essay_data.tag+'</a>'+
                    '</span>'+
                    '<span class="author">'+'作者: '+essay_data.user_name+'</span>'+
                    '</div>'+
                    '<section class="post tag-mysql tag-shell-scripts">'+essay_data.html_content +
                    '</section>';
                console.log(document.cookie.length);
                if (document.cookie.length>0){
                    decode_cookie=document.cookie.slice(11);
                    user_data=base64decode(decode_cookie);
                    user_name=user_data.split("-")[0];
                    user_email=user_data.split("-")[1];
                    // 这样的拼接不是回事啊，好麻烦
                    item_html+='<div class="comt-title">'+
                            '<div class="comt-avater pull-left">'+
                        '<img alt="默认用户图片" src="/static/images/default-user.jpg" class="comt-avatar" height="34" width="34">'+
                            '</div>'+
                            '<div class="comt-author pull-left">欢迎 '+'<code>'+user_name.replace('<', '&lt;').replace('>', '&gt;')+'</code>'+ ' 进行评论'+'	</div>'+
                            '</div>'+
                            '<div class="comt-box">'+
                            '<textarea placeholder="评论支持markdown语法，写点什么吧..." class="input-block-level comt-area" name="comment" id="comment" cols="89%" rows="5" tabindex="1" onkeydown="if(event.ctrlKey&amp;&amp;event.keyCode==13){document.getElementById("submit").click();return false};"></textarea>'+
                        '</div>'+
                            '<div class="comt-ctrl">'+
                            '<button class="newbtn btn-primary" onclick="post_comment()" type="submit" name="submit" id="submit" tabindex="5"><i class="fa fa-check-square-o"></i> 提交评论</button>'+
                        '</div>'

                }
                else{
                    item_html+='<div class="comt-title">'+'游客你好 评论先'+
                        '<a href="/login">登录 </a>'+ '或者 '+
                            '<a href="#myModal" data-reveal-id="myModal" data-toggle="modal" data-target="#myModal">注册</a>'+
                            '</div>'
                }

                if (comment_data){
                    item_html+='<ol class="commentlist">';
                    for(var i=0,dLen=comment_data.length;i<dLen;i++){
                    item_html+='<div class="c-avatar">'+
                            '<img alt="默认用户图片" src="/static/images/userimage.jpg" class="avatar avatar-54 photo" height="54" width="54" style="display: block;">'+
                            '<div class="c-main">'+comment_data[i].html_content+
                            '<div class="c-meta">'+
                        '<span class="c-author">'+comment_data[i].user_name.replace('<', '&lt;').replace('>', '&gt;')+' '+
                            getLocalTime(comment_data[i].created_time)+
                        '</span>'+
                        '</div>'+
                        '</div>'
                        +'</div>'
                }
                    item_html+='</ol>'
                }

                copy_tail(item_html)

            });

            }
        // 如果不是那么就应该是文章页请求 逻辑还是简单可以这么处理
        else {
            $.getJSON(query_cmd, function (data) {
            article_data=data["blogs"];
            blog_data=data['page'];
            for(var i=0,dLen=article_data.length;i<dLen;i++) {
	            art_html+= '<li>'+
                    // '<img src="'+ article_data[i].user_image +'">'+
                        '<h1 class="post-list__post-title post-title">'+
                    '<a target="_self" href="'+ '/index.html?item='+article_data[i].id+'">'+article_data[i].blog_title+'</a>'
                     +'</h1>'+
                        '<p class="excerpt">'+article_data[i].summary +'</p>'+
                        '<div class="post-list__meta">'+
                    '<time class="post-list__meta--date date">'+getLocalTime(article_data[i].created_time)+'</time>'+

                    '<span class="post-list__meta--tags tags">'+
                    '<a href="'+'/index.html?tag='+article_data[i].tag+'">'+article_data[i].tag+'</a>'+
                    '</span>'+
                        '<a class="btn-border-small" href="'+'/index.html?item='+article_data[i].id+'">继续阅读</a>'+
                    '</div>'+
  			            '</li>'+
                        '<hr class="post-list__divider">';

	        //这个js 是我写过的最傻逼的代码了 原因是我不想写完之后再通过写一个方法来隐藏
            next_page=blog_data.index+1;
            former_page=blog_data.index-1;
            if (blog_data.index>1 && blog_data.last_page>blog_data.index){

                new_art_html=art_html+
                        '<nav class="pagination" role="navigation">'+
                        '<a class="newer-posts pagination__newer btn btn-small btn-tertiary" href="/index.html?page='+
                    former_page+'">← 最近</a>'+
                        '<span class="pagination__page-number">'+ blog_data.index+' / '+blog_data.last_page+'</span>'+
                        '<a class="older-posts pagination__older btn btn-small btn-tertiary" href="/index.html?page="'+
                    next_page+'>更早 →</a>'
            }
            else if (blog_data.index==1 && blog_data.last_page>1){
                new_art_html=art_html+
                        '<nav class="pagination" role="navigation">'+

                        '<span class="pagination__page-number">'+ blog_data.index+' / '+blog_data.last_page+'</span>'+
                        '<a class="older-posts pagination__older btn btn-small btn-tertiary" href="/index.html?page='+
                    next_page+'">更早 →</a>'
            }
            else if (blog_data.index==blog_data.last_page && blog_data.last_page>1){
                new_art_html=art_html+
                        '<nav class="pagination" role="navigation">'+
                        '<a class="newer-posts pagination__newer btn btn-small btn-tertiary" href="/index.html?page='+
                    former_page+'">← 最近</a>'+
                        '<span class="pagination__page-number">'+ blog_data.index+' / '+blog_data.last_page+'</span>'
            }
            else if (blog_data.index==blog_data.last_page && blog_data.last_page==1){
                new_art_html=art_html+
                        '<nav class="pagination" role="navigation">'+
                        '<span class="pagination__page-number">'+ blog_data.index+' / '+blog_data.last_page+'</span>'
            }

        }
        // 注意 .getJSON 是异步的 return 返回是空，只能在函数内调用其他函数。。。

        copy_tail(new_art_html);

        });


        }


    }
    // 画面渐入的动画 后续完善
    change_background();
    function change_background() {
        var count = 1;
        var opt = $('#left-body');
        pic_path_list = ['/static/images/background-cover2.jpg', '/static/images/background-cover3.jpg',
            '/static/images/background-cover4.jpg', '/static/images/background-cover5.jpg'];
        setInterval(ready_change, 10000);
        function ready_change() {
            if (count > 3) {
                count = 0;
            }

            pic_path = 'url(' + pic_path_list[count] + ')';
            // setInterval(fade_in_movie, 2000);
            // function fade_in_movie() {
            //     for (var i = 1; i < 1000; i++) {
            //         opacity_float = i / 1000;
            //         opt.css('opacity', opacity_float);
            //
            //     }

                //
                // opt.className='panel-cover--overlay cover-slate';
                // 用js for 循环来模拟渐入的过程
                // for (var i=1;i<1000;i++){
                //     opacity_float=i/1000;
                //     opt.css('opacity',opacity_float);
                // }
                // opt.css({'-webkit-animation-name':'fadeIn',
                // '-webkit-animation-duration':'2s','-webkit-animation-iteration-count':'1',
                // '-webkit-animation-delay':'0s',"background-image":pic_path});


                // console.log(opt.className)
                // opt.className='panel-cover  panel-cover--fade';
            count += 1;
            opt.css('background-image', pic_path);
            }


    }



// 这里需要更深入的了解 css 和js 代码
    // function fadeInOut() {
    //     document.getElementById("left-body").className = "panel-cover  panel-cover--fade init-fade";
    //     setTimeout(function(){
    //                     if (count>3){
    //             count=0;
    //         }
    //     pic_path_list=['/static/images/background-cover2.jpg','/static/images/background-cover3.jpg',
    //     '/static/images/background-cover4.jpg','/static/images/background-cover5.jpg'];
    //         pic_path='url('+pic_path_list[count]+')';
    //         document.getElementById("left-body").className = "panel-cover  panel-cover--fade";
    //         document.getElementById("left-body").css('background-image',pic_path);
    //     },2000);
    //     count+=1
    // }
    // setTimeout(fadeInOut, 2000);//2s后淡入，2s后淡出
    check_visible();
    function check_visible() {
        // 各种浏览器兼容
        var hidden, state, visibilityChange;
        if (typeof document.hidden !== "undefined") {
            hidden = "hidden";
            visibilityChange = "visibilitychange";
            state = "visibilityState";
        } else if (typeof document.mozHidden !== "undefined") {
            hidden = "mozHidden";
            visibilityChange = "mozvisibilitychange";
            state = "mozVisibilityState";
        } else if (typeof document.msHidden !== "undefined") {
            hidden = "msHidden";
            visibilityChange = "msvisibilitychange";
            state = "msVisibilityState";
        } else if (typeof document.webkitHidden !== "undefined") {
            hidden = "webkitHidden";
            visibilityChange = "webkitvisibilitychange";
            state = "webkitVisibilityState";
        }

        // 添加监听器，在title里显示状态变化
        document.addEventListener(visibilityChange, function() {
            if (document[state]=='hidden')
                document.title='客官~快回来嘛~ ~';
            else{
                document.title = 'FuckBlog 首页';
            }

        }, false);

        // 初始化
        document.title = 'FuckBlog 首页';

    }



});




