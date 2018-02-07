var isntance = null;


function init(userInfo,callbacks) {
    if (!userInfo.appKey || !userInfo.token){
        return false;
    }

    //公有云初始化
    RongIMLib.RongIMClient.init(userInfo.appKey);
    var instance = RongIMClient.getInstance();

    //连接状态监听器
    RongIMClient.setConnectionStatusListener({
        onChanged: function (status) {
            switch (status) {
                case RongIMLib.ConnectionStatus.CONNECTED:
                    console.log("链接成功 ");
                    callbacks.CONNECTED && callbacks.CONNECTED(instance);
                    break;
                case RongIMLib.ConnectionStatus.CONNECTING:
                    console.log('正在链接');
                    break;
                case RongIMLib.ConnectionStatus.DISCONNECTED:
                    console.log('断开连接');
                    break;
                case RongIMLib.ConnectionStatus.KICKED_OFFLINE_BY_OTHER_CLIENT:
                    console.log('其他设备登录');
                    break;
                case RongIMLib.ConnectionStatus.DOMAIN_INCORRECT:
                    console.log('域名不正确');
                    break;
                case RongIMLib.ConnectionStatus.NETWORK_UNAVAILABLE:
                    console.log('网络不可用');
                    break;
            }
        }
    });


    RongIMClient.setOnReceiveMessageListener({
        // 接收到的消息
        onReceived: function (message) {
            callbacks.Received && callbacks.Received(message);
        }
    });


    //开始链接
    RongIMClient.connect(userInfo.token, {
        onSuccess: function (id) {
            callbacks.Success && callbacks.Success(id);
        },
        onTokenIncorrect: function () {
            console.log('token无效');
        },
        onError: function (errorCode) {
            var info = '';
            switch (errorCode) {
                case RongIMLib.ErrorCode.TIMEOUT:
                    info = '超时';
                    break;
                case RongIMLib.ErrorCode.UNKNOWN_ERROR:
                    info = '未知错误';
                    break;
                case RongIMLib.ErrorCode.UNACCEPTABLE_PaROTOCOL_VERSION:
                    info = '不可接受的协议版本';
                    break;
                case RongIMLib.ErrorCode.IDENTIFIER_REJECTED:
                    info = 'appkey不正确';
                    break;
                case RongIMLib.ErrorCode.SERVER_UNAVAILABLE:
                    info = '服务器不可用';
                    break;
            }
            console.log(info);
            alert(info)
        }
    });
}


function sendTextMessage(){
	/*
	文档： http://www.rongcloud.cn/docs/web.html#5_1、发送消息
		   http://rongcloud.cn/docs/api/js/TextMessage.html
	1: 单条消息整体不得大于128K
	2: conversatinType 类型是 number，targetId 类型是 string
	*/
	/*
		1、不要多端登陆，保证所有端都离线
		2、接收 push 设备设置:
			（1）打开系统通知提醒
			（2）小米设置 “授权管理” －> “自己的应用” 为自启动
			（3）应用内不要屏蔽新消息通知
		3、内置消息类型，默认 push，自定义消息类型需要
		   pushData 显示逻辑顺序：自定义 > 默认
		4、发送其他消息类型与发送 TextMessage 逻辑、方式一致
	*/
	var pushData = "pushData" + Date.now();
	var isMentioned = false;
	var content = {
		content: [
			"阿拉伯语：الشرق الأوسط ",
			"希伯来语：המזרח התיכון",
			"emoji: 😊 ",
			"希腊字母： π，α，β, ",
			"数字单位部分字符 如：× ",
			"拉丁文所有字符 如：Ο Ρ σ Ï Æ ",
			"拼音所有字符 如： ě ì ň ",
			"英文音标部分字符 如 ： ə ʃ ",
			"俄文部分字符 如 ：ш ; ⊇ â Œ Š ™ "
        ].join(","),
		user : {
			"id" : "this-is-a-test-id",	//不支持中文及特殊字符
			"name" : "张三",
			"portrait" : "http://rongcloud.cn/images/newVersion/log_wx.png"
		},
		extra: "{\"key\":\"value\", \"key2\" : 12, \"key3\":true}"
	};
	var msg = new RongIMLib.TextMessage(content);
	var start = new Date().getTime();
	instance.sendMessage(conversationType, targetId, msg, {
        onSuccess: function (message) {
        	markMessage(message);
            showResult("发送文字消息 成功",message,start);
        },
        onError: function (errorCode,message) {
            showResult("发送文字消息 失败",message,start);
        }
    }, isMentioned, pushData);
}