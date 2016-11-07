/**
 * Created by Zach on 16/5/17.
 */
//notification
// function error(message) {
//   $('.top-right').notify({
//     message: { html: message},
//     type: 'danger'
//   }).show();
// }
//
// function info(message) {
//   $('.top-right').notify({
//     message: { html: message},
//     type: 'info'
//   }).show();
// }
//
// function warring(message) {
//   $('.top-right').notify({
//     message: { html: message},
//     type: 'warning',
//   }).show();
// }

function error(message) {
  $.alert({
    title: '<font style="font-size: 14px;">错误提示</font>',
    autoClose: 'confirm|11000',
    icon: 'fa fa-warning confirm2_error',
    content: message,
    closeIcon: true,
    confirmButton: '确认',
    confirm: function () {
    },
    keyboardEnabled: true,
    columnClass: 'col-md-6 col-md-offset-3'
  });
}

function info(message) {
  $.alert({
    title: '<font style="font-size: 14px;">信息提示</font>',
    autoClose: 'confirm|11000',
    icon: 'fa fa-warning confirm2_info',
    content: message,
    closeIcon: true,
    confirmButton: '确认',
    confirm: function () {
    },
    keyboardEnabled: true,
    columnClass: 'col-md-6 col-md-offset-3'
  });
}

function warring(message) {
  $.alert({
    title: '<font style="font-size: 14px;">警告提示</font>',
    autoClose: 'confirm|11000',
    icon: 'fa fa-warning confirm2_warring',
    content: message,
    closeIcon: true,
    confirmButton: '确认',
    confirm: function () {
    },
    keyboardEnabled: true,
    columnClass: 'col-md-6 col-md-offset-3'
  });
}

function success(message) {
  $('.top-right').notify({
    message: { html: message},
    type: 'success'
  }).show();
}

//confirm dialog
var ok_fn;
var console_fn;

function showConfirm(ok, msg,cansole){
  $("#confirmModal").modal('toggle');
  var tips = msg ? msg : "确认删除吗？";
  $('#content-message').html(tips);
  ok_fn= ok;
  console_fn=console;

}
$('#confirm_ok').on('click', function (e) {
  $("#confirmModal").modal('hide');
  ok_fn();
});

$('#confirm_console').on('click', function (e) {
  $("#confirmModal").modal('hide');
  console_fn();
});

$(function () {
    $("#fakeLoader").fakeLoader({
      zIndex: 999, // Default zIndex
      spinner: "spinner2",//Options: 'spinner1', 'spinner2', 'spinner3', 'spinner4', 'spinner5', 'spinner6', 'spinner7'
      bgColor: "transparent"
    });
});

function showLoading() {
  $("#fakeLoader").show();
}

function closeLoading() {
  $("#fakeLoader").hide();
}

// $(function () {
//   $('#confirmModal').on('hidden.bs.modal', function (e) {
//     // do something...
//   })
//
// })