/**
 * Created by Administrator on 2017/1/14.
 */
$(function () {
    initDataTable();
        function initDataTable() {
        $.getJSON('/api/users', function (data) {
            console.log(data);
            console.log(typeof data);
            console.log(data["data"]);
            IndexerDTO=data["data"];
            loadDataTable()
        })
    }
        function loadDataTable() {
            var users= [];
            $(IndexerDTO).each(function (index) {
                users.push([IndexerDTO[index]['name'], IndexerDTO[index]['email'], IndexerDTO[index]['created_time'], IndexerDTO[index]['admin_flag'], IndexerDTO[index]['image'],IndexerDTO[index]['id'],
                    IndexerDTO[index]['password']]);
                console.log(users)
            });
            $('#example').dataTable({
                "data": users,
                "columns":[
                        { "data": 0},
                        { "data": 1 },
                        { "data": 2 },
                        { "data": 3 },
                        {"data":4},
                        {"data":5},
                        {"data":6}
                ]
            })
        }
});
