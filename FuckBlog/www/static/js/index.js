/**
 * Created by Administrator on 2017/1/15.
 */

$(function () {
    initDataTable();
        function initDataTable() {
        $.getJSON('/api/blogs', function (data) {
            console.log(data);
            console.log(typeof data);
            console.log(data["blogs"]);
            IndexerDTO=data["blogs"];
            loadDataTable()
        })
    }
        function loadDataTable() {
            var users= [];
            $(IndexerDTO).each(function (index) {
                users.push([IndexerDTO[index]['user_name'], IndexerDTO[index]['blog_title'], IndexerDTO[index]['summary'], IndexerDTO[index]['content'],
                    IndexerDTO[index]['created_time']]);
                console.log(users)
            });
            $('#example').dataTable({
                "data": users,
                "columns":[
                        { "data": 0},
                        { "data": 1 },
                        { "data": 2 },
                        { "data": 3 },
                        {"data":4}
                ]
            })
        }
});
