"use strict";
var KTLoginGeneral = function() {
    var i = $("#kt_login"),
        t = function(i, t, e) {
            var n = $('<div class="alert alert-' + t + ' alert-dismissible" role="alert">\t\t\t<div class="alert-text">' + e + '</div>\t\t\t<div class="alert-close">                <i class="flaticon2-cross kt-icon-sm" data-dismiss="alert"></i>            </div>\t\t</div>');
            i.find(".alert").remove(), n.prependTo(i), KTUtil.animateClass(n[0], "fadeIn animated"), n.find("span").html(e)
        },
        e = function() {
            i.removeClass("kt-login--forgot"), i.removeClass("kt-login--signup"), i.addClass("kt-login--signin"), KTUtil.animateClass(i.find(".kt-login__signin")[0], "flipInX animated")
        },
        n = function() {
            $("#kt_login_forgot").click(function(t) {
                t.preventDefault(), i.removeClass("kt-login--signin"), i.removeClass("kt-login--signup"), i.addClass("kt-login--forgot"), KTUtil.animateClass(i.find(".kt-login__forgot")[0], "flipInX animated")
            }), $("#kt_login_forgot_cancel").click(function(i) {
                i.preventDefault(), e()
            }), $("#kt_login_signup").click(function(t) {
                t.preventDefault(), i.removeClass("kt-login--forgot"), i.removeClass("kt-login--signin"), i.addClass("kt-login--signup"), KTUtil.animateClass(i.find(".kt-login__signup")[0], "flipInX animated")
            }), $("#kt_login_signup_cancel").click(function(i) {
                i.preventDefault(), e()
            })
        };
    return {
        init: function() {
            n()
        }
    }
}();
jQuery(document).ready(function() {
    KTLoginGeneral.init()
});