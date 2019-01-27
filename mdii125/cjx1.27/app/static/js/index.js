

$(function(){
	acCount();

	//点击放入餐车,选餐,
	// 点击事件委托给高层次元素,以免ajax请求刷新页面后新元素不能绑定js事件
	$('#pdv_05').on('click','.caipin_list img',function(){
			var cainame=$(this).parent().children('p:first').text().substring(3);
			var dcprice=$(this).parent().children('p:eq(1)').text().substring(3,7);
			var mealmeans=$(this).parent().children('p:eq(6)').text();
			console.log(mealmeans);
			//得到下拉列表选择数量的值
			var selCount=Number($(this).prev().children('select').val());

			var dcfood=new Array();
			$('#dcinfo li .dcfood').each(function(){
				var res=String($(this).text());
				dcfood.push(res);
			});

			//判断菜品是否已被勾选
			var listIndex=dcfood.indexOf(cainame);
			if(listIndex>-1){
				//说明此餐已点,则在原有数量上叠加
				var liCount=Number($('#dcinfo li input').eq(listIndex).val());
				$('#dcinfo li input').eq(listIndex).val(liCount+selCount);
				acCount();
			}
			//菜品头一次加入餐车需重新创建相应的列表
			else{
				$('#dcinfo').append("<li>\
								<p class='dcfood'>"+cainame+"</p>\
								<p class='dcprice'>"+dcprice+"</p>\
								<input type='text' value='"+selCount+"'>\
								<p class='dcCancel' style='background:#FFFDEA'>\
								<img src='/static/images/2019-01-06_212719.png'>\
								</p>\
								<p class='mealmeans' style='display: none;'>"+mealmeans+"</p>\
								</li>");
				// 判断已选餐单列表的索引奇偶性,设定其背景的css属性
				var newArr=$('#dcinfo li');
				for(i=0;i<newArr.length;++i){
					if(i%2!=0){
					newArr.eq(i).children('p').not('.dcCancel').css('background','#84A74A');
					}
				}
				acCount();
			}

			//单个菜品取消点餐
			$('#dcinfo li').each(function(){
				$(this).children('.dcCancel').click(function(){
					$(this).parent().remove();
					acCount();
				})
			});
			//手动修改点餐数量后,引起一系列改变事件
			$('#dcinfo li input').each(function(){
				$(this).bind("input propertychange",function(){
				acCount();
				})
			});
	})

	//全部菜品取消点餐
	$('#dc_img .dc_img02').click(function(){
		$('#dcinfo li').each(function(){
			$(this).remove()
		});
		acCount()
	});

	//定义算账函数
	function acCount(){
		var sumPrice=0;
		var sumCount=0;
		$('#dcinfo li input').each(function(){
			var count=parseFloat($(this).val());
			var price=parseFloat($(this).prev().html());
			sumCount+=count;
			sumPrice+=price*count;
		});
		$('#sum_dc .sumdc02 span').html(sumPrice);
		$('#sum_dc .sumdc03 span').html(sumCount);
	}

	//点击一级标题,选择订餐菜单信息表
	$.each($('#diancan_all_top p'),function(i,obj){
		$(obj).click(function(){
			//改变被点击的按钮的颜色,未被点击则不变
			$('#diancan_all_top p').each(function(){$(this).css('color','#ff9900');})
			$(this).css('color','#FA0320');
			//展示出相应的二级按钮
			$('.cat_01').each(function(){$(this).css('display','none')});
			$('.cat_01').eq(i).css('display','block');

			//判断二级标题的子按钮是否有clicked类,没有的话给第一个元素增加clicked类,有的话则取.clicked的文本字符
			if ($('.cat_01').eq(i).children('.clicked').length==0){$('.cat_01').eq(i).children('p:first').addClass('clicked')}
			var char = $('.cat_01').eq(i).children('.clicked').text();
			type_menus_ajax(char);
		})
	})

	//定义菜品的异步请求函数,方便调用
	function type_menus_ajax(char){
			$.ajax({
				url:'/type_menus?type='+char,
				async:true,
				dataType:'json',
				success:function(data){
					var html='';
					$.each(data,function(i,obj){

						html+="<div class='caipin_inform'>";
							html+="<div class='caipin_images'>";
								html+="<img src='/static/"+obj.images+"'>";
							html+="</div>";
							html+="<div class='caipin_list'>";
								html+="<p style='font-weight:bold;'>菜名:"+obj.cname+"</p>";
								html+="<p>单价:<span>"+obj.cprice+".0</span>&nbsp;元/份</p>";
								html+="<p>积分:<span>"+obj.points+"</span>分/份</p>";
								html+="<p>主料:"+obj.ingredients+"</p>";
								html+="<p>口味:<span>"+obj.taste+"</span></p>";
								html+="<p>可定份数:<span>"+obj.stock+"</span>份</p>";
								html+="<p style='display:none;'>"+obj.mealmeans+"</p>"
								html+="<p>";
									html+="<span style='color:#505050;'>份数</span>";
									html+="<select>";
										html+="<option value='1'>1</option>";
										html+="<option value='2'>2</option>";
										html+="<option value='3'>3</option>";
										html+="<option value='4'>4</option>";
										html+="<option value='5'>5</option>";
										html+="<option value='6'>6</option>";
									html+="</select>";
								html+="</p>";
								html+="<img src='/static/images/2019-01-08_172812.png'>";
							html+="</div>";
						html+="</div>";
					})
					$('#caipin').html(html);
				}
			})//单点餐品ajax结尾;
			 						}
	//点击事件委托,异步请求发送菜品种类,接受服务端响应的相应种类的菜品数据信息
	$('#pdv_05').on('click','.cat_01 p',function(){
        //点击时引起元素的颜色发生变化
		$(this).siblings().css({'color': '#666666', 'backgroundColor': '#FFFFFF'});
        $(this).css({'color': '#FFFFFF', 'backgroundColor': '#EC7521'});
        $(this).siblings().removeClass('clicked');
        $(this).addClass('clicked');
        var char = $(this).text();
        type_menus_ajax(char)
    })

});

//购物车提交
$(document).ready(function(){
	$('.dc_img01').click(function(){
		var nowcpprice=$('.sumdc02').children('span').html();//餐车中的餐品总价格
		var nowallnums=$('.sumdc03').children('span').html();//餐车中的餐品总数量
		if (nowcpprice>0&&nowallnums>0) {
            //满足条件发起异步请求向服务端传递数据

			$.ajax({
                url: '/dingcan_post',
                type: 'post',
                data:JSON.stringify(GetJsonData()),
                dataType: "json",
				contentType:"application/json",
                error: function(){
                    alert('请求数据传递失败');
                },
                success: function (msg) {
                	console.log(typeof(msg))
                    alert(msg);
                    if (msg == "OK") {

                        window.location = '/dingcan_startorder';
                    } else if (msg == "kongcart") {
                        alert("您的购物车中没有餐品");
                    } else if (msg == "wrongcart") {
                        alert("订单错误");
                    } else {
                        alert(msg);
                    }
                }

            });
            //将用户点的餐品的信息打包成json格式传递过去,定义函数方便调用
            function GetJsonData() {
                var teamdata = [];
                var mealmeans;
                for (var i = 0; i < $("#dcinfo li").length; i++) {
                    var teamobj = {
                        "cname": $(".dcfood").eq(i).text(),
                        "cprice": $(".dcprice").eq(i).text().substring(0,3),
						"number":$("#dcinfo li input").eq(i).val(),
						'mealmeans':$('.mealmeans').eq(i).text()
                    };
                teamdata.push(teamobj);
                }
                var json={
                	"userOrder":teamdata
				}
            return  json;
            }//GetJsonData()函数结尾
        }//if条件为真执行体的结尾
		else{
				alert("对不起，提交失败！请确保您已正确选择了餐品并正确填写了份数！");
		}
	})
})






