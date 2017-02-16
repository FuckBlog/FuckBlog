/**
 * Created by Administrator on 2017/1/12.
 */
$(function () {
    var art_html = '';
    initArticleData();
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
    function initArticleData() {
    if (getUrlVars()['page']){
        query_cmd='/api/blogs?page='+getUrlVars()['page']
    }
    else{
        query_cmd='/api/blogs'
    }
    $.getJSON(query_cmd, function (data) {
        article_data=data["blogs"];
        blog_data=data['page'];
        console.log(article_data);
        for(var i=0,dLen=article_data.length;i<dLen;i++) {
            art_html+= '<li>'+
                // '<img src="'+ article_data[i].user_image +'">'+
                    '<h1 class="post-list__post-title post-title">'+
                '<a target="_self" href="'+ '/blog/'+article_data[i].id+'">'+article_data[i].blog_title+'</a>'
                 +'</h1>'+
                    '<p class="excerpt">'+article_data[i].summary +'</p>'+
                    '<div class="post-list__meta">'+
                '<time class="post-list__meta--date date">'+getLocalTime(article_data[i].created_time)+'</time>'+

                '<span class="post-list__meta--tags tags">'+
                '<a href="'+'/api/'+article_data[i].tag+'">'+article_data[i].tag+'</a>'+
                '</span>'+
                    '<a class="btn-border-small" href="'+'/blog/'+article_data[i].id+'">继续阅读</a>'+
                '</div>'+
                    '</li>'+
                    '<hr class="post-list__divider">';
        console.log(typeof blog_data.index)    ;
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

    new_art_html=new_art_html+'<footer class="footer" >'+
    '<span class="footer__copyright">本站点采用<a href="http://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">知识共享 署名-非商业性使用-相同方式共享 4.0 国际 许可协议</a></span>'+
    '<span class="footer__copyright">本站由 <a href="http://www.songluyi.com">FuckBlog</a> 创建，学习'+'<a href="https://onevcat.com/" target="_blank">OneVs Den</a>的博客主题，您可以在 GitHub 上找到该主题<a href="https://github.com/onevcat/OneV-s-Den" target="_blank">开源代码</a> - © 2016</span>'+
'</footer>'
}       $('#article_list').append(new_art_html);
    })}
//js 函数是有作用域
    console.log(art_html);



});