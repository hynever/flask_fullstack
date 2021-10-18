const socket = io();

let current_oppsite = "";


function bindAllUserClickEvent(){
  $(".list-group-item").click(function (event){
    let user = $(this).text().replace("【私】","").replace("【群】","");
    current_oppsite = user;
  });

  $(".list-group-item").click(function (event){
    let room = $(this).text().replace("【私】","").replace("【群】","");
    current_oppsite = user;
  });
}

$(window).bind("beforeunload", function (){
  socket.on("disconnect");
});

$(function (){
  socket.on("users", function (result){
    let users = result.users;
    let chats = [];
    for (let index = 0; index < users.length; index++) {
      let user = users[index];
      chats.push({"group": false, "name": user});
    }
    let raw_source = $("#chat-list-template").html();
    let source = template.render(raw_source, {"group": false, chats});
    $("#chat-ul").html(source);

    bindAllUserClickEvent();
  });

  socket.on("personal", function (data){
    let message = data.message;
    let from_user = data.from_user;
    current_oppsite = from_user;
    let raw_source = $("#chat-content-template").html();
    let source = template.render(raw_source, {"from_user": current_oppsite, "message": message});
    $("#chat-list-box").append(source);
  });

  socket.on("connect", function(){
    console.log("连接成功");
    $("#send-button").click(function (event){
      event.preventDefault();
      if(!current_oppsite){
        alert("请先选择联系人！");
        return;
      }
      let textarea = $("#chat-textarea");
      let content = textarea.val();
      socket.emit("personal", {"to_user": current_oppsite, "message": content}, function (){
        let raw_source = $("#chat-content-template").html();
        let source = template.render(raw_source, {"from_user": "me", "message": content});
        $("#chat-list-box").append(source);
      });
      textarea.val("");
    });

    socket.emit("join", {"room": "Flask交流群"});
    socket.emit("room_chat", {"room": "Flask交流群", "message": "大家好"});
    socket.on("room_chat", function (result){
      socket.emit("room_hat", {"room": "Flask交流群", "message": "大家好"});
    });
  });
});