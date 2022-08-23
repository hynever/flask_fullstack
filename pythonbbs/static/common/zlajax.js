'use strict';
var zlajax = {
  'get': function (args) {
    args['method'] = "get"
    return this.ajax(args);
  },
  'post': function (args) {
    args['method'] = "post"
    return this.ajax(args);
  },
  'put': function(args){
    args['method'] = "put"
    return this.ajax(args)
  },
  'delete': function(args){
    args['method'] = 'delete'
    return this.ajax(args)
  },
  'ajax': function (args) {
    // 设置csrftoken
    this._ajaxSetup();
    return $.ajax(args);
  },
  '_ajaxSetup': function () {
    $.ajaxSetup({
      'beforeSend': function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
          var csrftoken = $('meta[name=csrf-token]').attr('content');
          xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
      }
    });
  }
};