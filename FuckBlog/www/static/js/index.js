/**
 * Created by Administrator on 2017/1/15.
 */

// $(function () {
//     initDataTable();
//         function initDataTable() {
//         $.getJSON('/api/blogs', function (data) {
//             console.log(data);
//             console.log(typeof data);
//             console.log(data["blogs"]);
//             IndexerDTO=data["blogs"];
//             loadDataTable()
//         })
//     }
//         function loadDataTable() {
//             var users= [];
//             $(IndexerDTO).each(function (index) {
//                 users.push([IndexerDTO[index]['user_name'], IndexerDTO[index]['blog_title'], IndexerDTO[index]['summary'], IndexerDTO[index]['content'],
//                     IndexerDTO[index]['created_time']]);
//                 console.log(users)
//             });
//             $('#example').dataTable({
//                 "data": users,
//                 "columns":[
//                         { "data": 0},
//                         { "data": 1 },
//                         { "data": 2 },
//                         { "data": 3 },
//                         {"data":4}
//                 ]
//             })
//         }
// });



$(function () {
    var art_html = '';
    initArticleData();
    function getLocalTime(nS) {
        return new Date(parseInt(nS) * 1000).toLocaleString().replace(/:\d{1,2}$/,' ');
        }
        function initArticleData() {

        $.getJSON('/api/blogs', function (data) {
            article_data=data["blogs"];
            blog_data=data['page'];
            console.log(article_data);
            for(var i=0,dLen=article_data.length;i<dLen;i++) {
	            art_html+= '<li>'+
                    // '<img src="'+ article_data[i].user_image +'">'+
                        '<h1 class="post-list__post-title post-title">'+
                    '<a target="_self" href="'+ '/api/blogs/'+article_data[i].id+'">'+article_data[i].blog_title+'</a>'
                     +'</h1>'+
                        '<p class="excerpt">'+article_data[i].summary +'</p>'+
                        '<div class="post-list__meta">'+
                    '<time class="post-list__meta--date date">'+getLocalTime(article_data[i].created_time)+'</time>'+

                    '<span class="post-list__meta--tags tags">'+
                    '<a href="'+'/api/'+article_data[i].tag+'">'+article_data[i].tag+'</a>'+
                    '</span>'+
                        '<a class="btn-border-small" href="'+'/api/blogs/'+article_data[i].id+'">继续阅读</a>'+
                    '</div>'+
  			            '</li>'+
                        '<hr class="post-list__divider">';
	        console.log(typeof blog_data.index)    ;
	        //这个js 是我写过的最傻逼的代码了 原因是我不想写完之后再通过写一个方法来隐藏
            if (blog_data.index>1 && blog_data.last_page>blog_data.index){
                new_art_html=art_html+
                        '<nav class="pagination" role="navigation">'+
                        '<a class="newer-posts pagination__newer btn btn-small btn-tertiary" href="/page/'+
                    blog_data.index-1+'">← 最近</a>'+
                        '<span class="pagination__page-number">'+ blog_data.index+' / '+blog_data.last_page+'</span>'+
                        '<a class="older-posts pagination__older btn btn-small btn-tertiary" href="/page/"'+
                    blog_data.index+1+'>更早 →</a>'
            }
            else if (blog_data.index==1 && blog_data.last_page>1){
                new_art_html=art_html+
                        '<nav class="pagination" role="navigation">'+

                        '<span class="pagination__page-number">'+ blog_data.index+' / '+blog_data.last_page+'</span>'+
                        '<a class="older-posts pagination__older btn btn-small btn-tertiary" href="/page/"'+
                    blog_data.index+1+'>更早 →</a>'
            }
            else if (blog_data.index==blog_data.last_page>1){
                new_art_html=art_html+
                        '<nav class="pagination" role="navigation">'+
                        '<a class="newer-posts pagination__newer btn btn-small btn-tertiary" href="/page/'+
                    blog_data.index-1+'">← 最近</a>'+
                        '<span class="pagination__page-number">'+ blog_data.index+' / '+blog_data.last_page+'</span>'
            }
            else if (blog_data.index==blog_data.last_page==1){
                new_art_html=art_html+
                        '<nav class="pagination" role="navigation">'+
                        '<span class="pagination__page-number">'+ blog_data.index+' / '+blog_data.last_page+'</span>'
            }
}       $('#article_list').append(new_art_html);
        })}
//js 函数是有作用域
    console.log(art_html);



});




