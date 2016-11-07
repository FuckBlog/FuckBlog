/**
 * Created by Zach on 16/5/16.
 */
function doAutoWork() {
  var doWork = $.query.get("doWork");
  if ("wbrw" == doWork) {
    var param = "";
    var taskName = $.query.get("taskName");
    if ("" != taskName)
      param += "taskName=" + taskName;
    var url = "/pages/nbcc/task/taskList.html?";
    if ("" != param)
      url += param;
    $('#content').attr("src", url);
  }
}

$(function () {
  doAutoWork();

  $('.closeMenu').on('click', function () {
      if ($('#indexMenu').is(':hidden')) {
        $('#indexMenu').show(function () {
          $('#page-wrapper').css("margin-left", "220px");
          $('#closeMenu2').hide();
        });
      } else {
        $('#indexMenu').hide(function () {
          $('#page-wrapper').css("margin-left", "0px");
          $('#closeMenu2').show();
        });
      }
  });

  $('#logout').click(function(){
    $("#logoutform").submit();
  });

  $("iframe.auto-height").iframeAutoHeight({minHeight: 500});

  var config = new nerinJsConfig();

  $.get(config.baseurl+'/api/isLogon',function (data) {
    if (!data)
        window.location.href = "/index.html";
  });

  //初始化后端页面菜单
  $.get(config.baseurl+'/api/menus/tree/back',function (data) {
    //循环一级节点数据
    $(data).each(function (index) {
      //获取当前一级菜单节点
      var children_L1 = data[index].children;

      var target_ = ("1" == data[index].outsideUrl ? "_blank" : "content");

      //如果当前一级菜单有子节点
      if(children_L1.length>0){
        //创建带箭头一级子节点
        var rootNav=$('<li><a target="' + target_ + '" href="'+data[index].url+'"><i class="fa '+data[index].icon+' fa-fw"></i>'+data[index].name+'<span class="fa arrow"></span></a></li>');
        //创建一级子节点的孩子节点,即二级节点
        var dropdown_L1 = $('<ul class="nav2 nav-second-level"></ul>');
        //循环二级节点
        $(children_L1).each(function (index1) {
          //获取二级节点子节点,即三级节点
          var children_L2 = children_L1[index1].children;

          //如果当前二级节点包含子节点,即三级节点
          if(children_L2.length>0){
            var target_2 = ("1" == children_L1[index1].outsideUrl ? "_blank" : "content");

            //创建展开箭头的二级子节点
            var child_L1=$('<li><a target="' + target_2+ '" href="'+children_L1[index1].url+'">'+children_L1[index1].name+'<span class="fa arrow"></span></a></li>');
            //创建二级节点的子节点,即三级节点
            var dropdown_L2 = $('<ul class="nav2 nav-third-level"></ul>');

            //循环三级节点
            $(children_L2).each(function (index2) {
              var target_3 = ("1" == children_L2[index2].outsideUrl ? "_blank" : "content");

              var child_L2 = $('<li><a target="' + target_3+ '" href="'+children_L2[index2].url+'">'+children_L2[index2].name+'</a></li>');
              child_L1.append(dropdown_L2.append(child_L2));
            });
          }else {
            var target_2 = ("1" == children_L1[index1].outsideUrl ? "_blank" : "content");
            //创建二级节点
            var child_L1 = $('<li><a target="' + target_2+ '" href="'+children_L1[index1].url+'"><i class="fa '+children_L1[index1].icon+' fa-fw"></i>'+children_L1[index1].name+'</a></li>');

          }
          //展开箭头的二级结点
          dropdown_L1.append(child_L1);
          //添加一级结点
          $(rootNav).append(dropdown_L1);
        });
      }else {
        //正常一级节点
        var rootNav=$('<li><a target="' + target_ + '" href="'+data[index].url+'"><i class="fa '+data[index].icon+' fa-fw"></i> '+data[index].name+'</a></li>');
      }
      $("#side-menu").append(rootNav);

    });
    $(function() {

      $('#side-menu').metisMenu();

    });
  });

  function setIframeHeight(){
    try{
      var iframe = document.getElementById("content");
      if(iframe.attachEvent){
        $(iframe).css({ "height": iframe.contentWindow.document.documentElement.scrollHeight});
        // iframe.attachEvent("onload", function(){
        //   console.log("a" + iframe.contentWindow.document.documentElement.scrollHeight);
        //   iframe.height =  iframe.contentWindow.document.documentElement.scrollHeight;
        // });
        return;
      }else{
        $(iframe).css({ "height": iframe.contentWindow.document.documentElement.scrollHeight});
        // iframe.onload = function(){
        //   iframe.height = iframe.contentDocument.body.scrollHeight + 10;
        // };
        return;
      }
    }catch(e){
      throw new Error('setIframeHeight Error');
    }
  }

  window.setInterval(setIframeHeight, 600);

});
