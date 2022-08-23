function captchaBtnClickEvent(event) {
  event.preventDefault();
  var $this = $(this);

  // 获取邮箱
  var email = $("input[name='email']").val();
  var reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/;
  if (!email || !reg.test(email)) {
    alert("请输入正确格式的邮箱！");
    return;
  }

  zlajax.get({
    url: "/user/mail/captcha?mail=" + email
  }).done(function (result) {
    alert("验证码发送成功！");
  }).fail(function (error) {
    alert(error.message);
  })
}

$(function () {
  $('#captcha-btn').on("click",function(event) {
    event.preventDefault();
    // 获取邮箱
    var email = $("input[name='email']").val();

    zlajax.get({
      url: "/user/mail/captcha?mail=" + email
    }).done(function (result) {
      alert("验证码发送成功！");
    }).fail(function (error) {
      alert(error.message);
    })
  });
});