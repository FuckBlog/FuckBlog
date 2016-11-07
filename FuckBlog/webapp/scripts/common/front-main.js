/**
 * Created by Zach on 16/5/15.
 */


$(function() {
  var config = new nerinJsConfig();

  $('iframe.auto-height').iframeAutoHeight({minHeight: 500});

  //初始化前端页面菜单
  $.get(config.baseurl+'/api/menus/tree/front',function (data) {
    console.log(data);
    $(data).each(function (index) {
      var children_L1 = data[index].children;
      if(children_L1.length>0){
        var rootNav=$('<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false" href="'+data[index].url+'">'+data[index].name+'<span class="caret"></span></a></li>');
        var dropdown_L1 = $('<ul class="dropdown-menu"></ul>');
        $(children_L1).each(function (index1) {
          console.log(children_L1[index1].name);
          var child_L1 = $('<li><a href="'+children_L1[index1].url+'">'+children_L1[index1].name+'</a></li>')
          dropdown_L1.append(child_L1);
        });
        $(rootNav).append(dropdown_L1);
      }else {
        var rootNav=$('<li><a href="'+data[index].url+'">'+data[index].name+'</a></li>');
      }
      $("#frontNav").append(rootNav);

    });
  });

});
