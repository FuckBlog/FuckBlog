/**
 * local dev
 */

$(function () {
  if (900 <= window.screen.height) {
    $("body").css("font-size", "13px");
    $("body").css("font-family", "微软雅黑");
    $(".btn").css("font-size", "13px");
    $(".btn").css("font-family", "微软雅黑");
  } else {
    $("body").css("font-size", "11px");
    $("body").css("font-family", "微软雅黑");
    $(".btn").css("font-size", "11px");
    $(".btn").css("font-family", "微软雅黑");
  }

  //console.log(window.screen.width);
});

function nerinJsConfig() {

  this.evn="dev";
  //this.evn="test";

  //通用配制
  this.searchResultSize=1000;
  //开发环境配制
  if("dev"==this.evn){
    this.baseurl = "http://127.0.0.1:8080";
  }else if("test"==this.evn){
    this.baseurl = "http://192.168.15.95:8080";
  }
}

$.ajaxSetup({
  contentType:"application/json",
  dataType:"json",
});

var ajaxError_loadData = "加载数据出错！";
var ajaxError_sys = "系统异常，请稍后再试！";

var tips_delSuccess = "删除成功！";
var tips_saveSuccess = "保存成功！";
var valTips_selOne = "请勾选一行！";
var valTips_selcheckOne = "请选择一行！";
var valTips_workOne = "每次只能对一行数据进行操作，请确认只勾选一行数据！";

