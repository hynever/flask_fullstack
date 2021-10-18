$(function (){
  $("#submit-button").click(function (event){
    event.preventDefault();
    let username = $("#username-input").val();
    if(!username){
      alert("请输入用户名！");
      return;
    }
    $.post({
      url: "/login",
      data: {"username": username},
    }).done(function (data){
        let code = data['code'];
        if(code != 200){
          alert(data['message']);
          return;
        }else{
          window.location = "/";
        }
      });
  });
});