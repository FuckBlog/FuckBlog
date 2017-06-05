/**
 * Created by Administrator on 2017/4/13.
 */

    var admin_flag = [
        { Name: "否", Id: 0 },
        { Name: "是", Id: 1 }
    ];
    query_user='/api/users';
    $.getJSON(query_user,function (user_data) {
        clients=user_data['data'];
        $("#jsGrid").jsGrid({
            height: "400px",
            width: "100%",

            filtering: true,
            editing: true,
            sorting: true,
            paging: true,
            autoload: true,

            pageSize: 10,
            pageButtonCount: 5,

            deleteConfirm: "真的要删除喵?",



            data: clients,

            fields: [
                { name: "name", type: "text", width: 150, validate: "required"},
                { name: "email", type: "text", width: 150,validate: "required" },
                { name: "created_time", type: "text", width: 200 },
                { name: "admin_flag", type: "select", items: admin_flag, valueField: "Id", textField: "Name" },
                // { name: "Married", type: "checkbox", title: "Is Married", sorting: false },
                // { name: "password",type: "text", width: 150, validate: "required"},
                { type: "control" }
            ]
        });
    });

    // var clients = [
    //     { "姓名": "Otto Clay", "Age": 25, "Country": 1, "Address": "Ap #897-1459 Quam Avenue", "Married": false },
    //     { "姓名": "Connor Johnston", "Age": 45, "Country": 2, "Address": "Ap #370-4647 Dis Av.", "Married": true },
    //     { "姓名": "Lacey Hess", "Age": 29, "Country": 3, "Address": "Ap #365-8835 Integer St.", "Married": false },
    //     { "姓名": "Timothy Henson", "Age": 56, "Country": 1, "Address": "911-5143 Luctus Ave", "Married": true },
    //     { "姓名": "Ramona Benton", "Age": 32, "Country": 3, "Address": "Ap #614-689 Vehicula Street", "Married": false }
    // ];

    // var countries = [
    //     { Name: "", Id: 0 },
    //     { Name: "United States", Id: 1 },
    //     { Name: "Canada", Id: 2 },
    //     { Name: "United Kingdom", Id: 3 }
    // ];

    // $("#jsGrid").jsGrid({
    //     width: "100%",
    //     height: "400px",
    //
    //     inserting: true,
    //     editing: true,
    //     sorting: true,
    //     paging: true,
    //
    //     data: clients,
    //
    //     fields: [
    //         { name: "姓名", type: "text", width: 150, validate: "required" },
    //         { name: "Age", type: "number", width: 50 },
    //         { name: "Address", type: "text", width: 200 },
    //         { name: "Country", type: "select", items: countries, valueField: "Id", textField: "Name" },
    //         { name: "Married", type: "checkbox", title: "Is Married", sorting: false },
    //         { type: "control" }
    //     ]
    // });
