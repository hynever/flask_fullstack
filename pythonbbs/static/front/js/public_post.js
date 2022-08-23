$(function (){
  var editor = new window.wangEditor("#editor");
  editor.config.uploadImgServer  = "/upload/image";
  editor.config.uploadFileName = "image";
  editor.create();


  // 提交按钮点击事件
  $("#submit-btn").click(function (event) {
      event.preventDefault();

      var title = $("input[name='title']").val();
      var board_id = $("select[name='board_id']").val();
      var content = editor.txt.html();

      zlajax.post({
        url: "/post/public",
        data: {title,board_id,content}
      }).done(function(data){
          setTimeout(function (){
              window.location = "/";
          },2000);
      }).fail(function(error){
          alert(error.message);
      });
  });
});