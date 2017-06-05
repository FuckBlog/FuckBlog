/**
 * Created by Administrator on 2017/2/16.
 */
$(document).ready(function() {

    $('#example11').dataTable({
        "ajax": '/api/all_blogs',
        "columns": [
            {data:'user_name'},
            {data:'blog_title'},
            {data:'id'},
            {data:'tag'}
        ]
    });
    $('#example1').dataTable({
        "ajax": '/api/all_comt',
        "columns": [
            {data:'user_name'},
            {data:'blog_title'},
            {data:'content'},
            {data:'created_time'}
            ]

    });
    var table = $('#example1').DataTable();

    $('#example1 tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );

    $('#button').click( function () {
        table.row('.selected').remove().draw( false );
    } );
});