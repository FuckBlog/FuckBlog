/**
 * Created by Zach on 16/5/16.
 */
$(function () {
  var config = new nerinJsConfig();

  //login popup
  //if("dev"!=config.evn) {
    $.get('/api/authenticate', function (data) {
      if (!data['currentUser'] || '' == data['currentUser']) {
        $('#loginModal').modal({});
        $('#loginPopup').css('display', 'block');
      } else {
        $('#currentUser').html(data['currentUser']);
        // $.getJSON('/api/account', function (data) {
        //   console.log(data);
        // });
        $('#loginPopup').css('display', 'none');
        $('#userProfile').css('display', 'block')
      }
    });
  //}else {
  //  $('#loginPopup').css('display', 'block');
  //}

  $('#loginPopup').click(function () {
    $('#loginModal').modal({
    });
  });

  //login
  $('#loginbutton').click(function(){
    var username=$('#j_username').val();
    var password=$('#j_password').val();
    $.ajaxSetup({
      contentType:"application/x-www-form-urlencoded; charset=UTF-8",
      dataType:"",
    });
    $.post('/api/authentication',{'_csrf':$.cookie('CSRF-TOKEN'),j_username:username,j_password:password})
      .done(function (data) {
          location.reload();
          // console.log(data);
        })
      .fail(function(response) {
        if(401==response.status){
          error('请检查用户名密码是否正确!');
          console.log(response);
        }
      });
  });

  //logout
  $('#logout').click(function(){
    //$.cookie('name');
    //$.post(config.baseurl+'/api/logout',{'_csrf':$.cookie('CSRF-TOKEN')},function () {
    //  location.reload();
    //});
     $("#logoutform").submit();
  });
  

});
