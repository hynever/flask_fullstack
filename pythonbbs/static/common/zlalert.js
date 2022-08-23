var ZLAlert = function () {
   this.alert = Swal.mixin({});

   this.toast = Swal.mixin({
      toast: true,
      position: "top",
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: false,
      didOpen: (toast) => {
         toast.addEventListener('mouseenter', Swal.stopTimer)
         toast.addEventListener('mouseleave', Swal.resumeTimer)
      }
   });
}

ZLAlert.prototype.successToast = function (title){
    this.toast.fire({
        icon: "success",
        title
    })
}

ZLAlert.prototype.infoToast = function (title){
    this.toast.fire({
        icon: "info",
        title
    })
}


var zlalert = new ZLAlert();