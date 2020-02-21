$(function(){
    var error_name=false;
    var error_password=false;
    var error_check_password=false;
    var error_email=false;
    var error_check=false;

    $('#user_name').blur(function(){  //光标移出
        check_username();
    })

    $('#user_name').click(function(){
        $(this).next().hide()    //点击#user_name时，报错信息隐藏
    })

    $('#pwd').blur(function(){
        check_password();
    })

    $('#pwd').click(function(){
        $(this).next().hide()
    })

    $('#cpwd').blur(function(){
        check_cpwd();
    })

    $('#cpwd').click(function(){
        $(this).next().hide()
    })

    $('#email').blur(function(){
        check_email();
    })

    $('#email').click(function(){
        $(this).next().hide()
    })

    //是否勾选协议校验
    $('#allow').click(function(){
        if($(this).is(':checked')){
            $(this).siblings('span').hide();
            error_check = false;
        }
        else{
            $(this).siblings('span').html('请勾选协议！');
            $(this).siblings('span').show();
            error_check = true;
        }
    })

    //检查用户名
    function check_username(){
        var val=$('#user_name').val()
        var reg=/^[\w]{5,15}$/

        if(val==''){      //空值判断
            $('#user_name').next().html('用户名不能为空！')
            $('#user_name').next().show();
            error_name=true;
            return
        }

        if(reg.test(val)){    //正则判断
            $.get('/user/register_exit/?uname='+$('#user_name').val(),function(data){   //判断用户名是否存在
                if(data.count==1){
                    $('#user_name').next().html('用户名已存在').show();
                    error_name=true;
                }
                else{
                    $('#user_name').next().hide();
			        error_name = false;
                }
		    })
        }
        else{
            $('#user_name').next().html('用户名是5到15个英文或数字，还可包含“_”')
            $('#user_name').next().show();
            error_name=true;
        }
    }

    //检查密码
    function check_password(){
        var val=$('#pwd').val()
        var reg=/^[a-zA-Z0-9@\!\*\?\.\&]{6,16}$/;

        if(val==''){      //空值判断
            $('#pwd').next().html('密码不能为空！')
            $('#pwd').next().show();
            error_password=true;
            return
        }

        if(reg.test(val)){    //正则判断
            $('#pwd').next().hide();
            error_password=false;
        }
        else{
            $('#pwd').next().html('密码是6到16位字母、数字，还可包含@!*？。&.~字符')
            $('#pwd').next().show();
            error_password=true;
        }
    }

    //检查确认密码
    function check_cpwd(){
        var pwd=$('#pwd').val();
        var cpwd=$('#cpwd').val();

        if(cpwd==pwd){
            $('#cpwd').next().hide();
            error_check_password=false;
        }
        else{
            $('#cpwd').next().html('两次输入的密码不一致');
            $('#cpwd').next().show();
            error_check_password=true;
        }
    }

    //检查邮箱
    function check_email(){
        var val=$('#email').val()
        var reg=/^[0-9a-z][\w\.\-]*@[a-z-0-9\-]+(\.[a-z]{2,3}){1,2}$/;

        if(val==''){      //空值判断
            $('#email').next().html('邮箱不能为空！')
            $('#email').next().show();
            error_email=true;
            return
        }

        if(reg.test(val)){    //正则判断
            $('#email').next().hide();
            error_email=false;
        }
        else{
            $('#email').next().html('你输入的邮箱格式不正确')
            $('#email').next().show();
            error_email=true;
        }
    }

    //表单提交校验
    $('.reg_form').submit(function(){
        check_username();
        check_password();
        check_cpwd();
        check_email();

        /*
        if(error_name==false && error_password==false && error_check_password==false && error_email==false && error_check==false){
            return true;
        }
        else{
            return false;
        }
        */

        if(! (error_name==false && error_password==false && error_check_password==false && error_email==false && error_check==false)){
            return false;
        }

    })
})