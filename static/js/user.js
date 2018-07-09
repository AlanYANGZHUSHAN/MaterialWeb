var starturl = "";

var apiurl = {
    loginUrl : '/login',
    registerUrl : '/register',
    setRightUrl : '/setright',
    deleteUrl   : '/delete',
    getallUrl   : '/getall',
    addmaterialUrl : '/addmaterial',
    getallmaterialUrl:'/getallmaterial',
    storageactionUrl :'storageaction',
    materialrestUrl:'/rest'
};

$(document).ready(function(){
    vue["User"].init();
});

var vue = {
    User : new Vue ({
        delimiters : ['<%', '%>'],
        mounted : function() {
        },
        el: '#user',
        data:{
	    username    :'',
	    password    :'',
	    position    :'',
	    action      :'',
            start_date  :'',
            end_date    : '',
	    record      :false,
	    query       :false,
	    manager     :false,
	    tousername  :'',
	    topassword  :'',
	    toposition  :'',
	    torecord    :0,
	    toquery     :0,
	    tomanager   :0,
	    isShowManager:false,
	    isShowRecord :false,
	    isShowQuery  :false,
	    user_list    :[],
	    material_list:[],
	    materialname :"",
	    manufacturer :"",
	    level        :"",
	    color        :"",
	    width        :0,
	    thick        :0,
	    id           :1,
	    direction    :'入库',
	    amount       :0,
	    batch_number :'',
	    id_list      :[],
	    sum_list     :[],
	    detail_list  :[],
	    isShowDetail : false,
        },
        methods : {
            init: function() {
                var _userThis = this;
                var now_date = (new Date()).valueOf();
                var now_date_array = this.$options.methods.formatDate.bind(this)(now_date);
                var start_date = now_date - 24*60*60*1000;
                var start_date_array =  this.$options.methods.formatDate.bind(this)(start_date);
                _userThis.start_date = start_date_array[1];
                _userThis.end_date = now_date_array[1];
		_userThis.isShowManager = false;
		_userThis.isShowRecord = false;
            },

            formatDate: function(time_params){
                var now_time = new Date(time_params);
                var now_time_stamp = Math.round(now_time/1000);
                var time = ((now_time.toLocaleString()).split(' ')[0]).split('/');
                var year = time[0];
                var month = time[1];
                var day = time[2];

                if(month.length == 1){
                    month = '0' + month;
                };

                if(day.length == 1){
                    day = '0' + day;
                };
                var now_time_format = year + '-' + month + '-' + day;
                return [now_time_stamp, now_time_format];
            },

	    login: function(){
	    	var _loginThis = this;
                $.ajax({
                    type : 'post',
                    dataType : 'json',
                    url :  starturl + apiurl.loginUrl,
                    data: JSON.stringify({action:'get',username:_loginThis.username, password:_loginThis.password}),
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
			    window.location = "/main";
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
                        };
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });

	    }, 

	    register: function(){
	    	var _registerThis = this;
                $.ajax({
                    type : 'post',
                    dataType : 'json',
                    url :  starturl + apiurl.registerUrl,
                    data: JSON.stringify({action:'add',username:_registerThis.username, password:_registerThis.password, position:_registerThis.position}),
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
			    window.location = "/login";
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
                        };
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });

	    }, 

	    setRight: function(){
	    	var _setRightThis = this;
                $.ajax({
                    type : 'post',
                    dataType : 'json',
                    url :  starturl + apiurl.setRightUrl,
                    data: JSON.stringify({action:'set',username:_setRightThis.tousername, password:_setRightThis.topassword, position:_setRightThis.toposition,record:_setRightThis.torecord,query:_setRightThis.toquery,manager:_setRightThis.tomanager}),
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
			    alert('set right success');
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
			};
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });

	    },
	    showmanager: function(){
	    	var _showmanagerThis = this;
		_showmanagerThis.isShowManager= true;
		_showmanagerThis.isShowRecord = false;
		_showmanagerThis.isShowQuery = false;
		_showmanagerThis.isShowDetail = false;
		$.ajax({
                    type : 'post',
                    dataType : 'json',
                    url :  starturl + apiurl.getallUrl,
                    data: JSON.stringify({action:'getall'}),
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
			    _showmanagerThis.user_list = response['result']
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
			};
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });

	    },
	     
            closeSetRight: function(){
		var _closeSetRight = this;
		_closeSetRight.isShowManager= false; 
	    },
	    selectuser: function(ele){
		var _selectuserThis = this;
		_selectuserThis.tousername = this.user_list[ele.target.value]['username'];
		_selectuserThis.topassword = this.user_list[ele.target.value]['password'];
		_selectuserThis.toposition = this.user_list[ele.target.value]['position'];
		_selectuserThis.torecord = this.user_list[ele.target.value]['record'];
		_selectuserThis.toquery = this.user_list[ele.target.value]['query'];
		_selectuserThis.tomanager = this.user_list[ele.target.value]['manager'];
	    },

	    deleteUser: function(){
	    	var _deleteUserThis = this;
                $.ajax({
                    type : 'post',
                    dataType : 'json',
                    url :  starturl + apiurl.deleteUrl,
                    data: JSON.stringify({action:'del',username:_deleteUserThis.tousername, password:_deleteUserThis.topassword, position:_deleteUserThis.toposition, record:_deleteUserThis.torecord, query:_deleteUserThis.toquery, manager:_deleteUserThis.tomanager}),
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
			    alert('delete user success');
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
			};
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });

	    },
	    
	    addMaterial: function(){
		var _addMaterialThis = this;
		$.ajax({
                    type : 'post',
                    dataType : 'json',
                    url :  starturl + apiurl.addmaterialUrl,
                    data: JSON.stringify({action:'addmat',materialname:_addMaterialThis.materialname,manufacturer:_addMaterialThis.manufacturer,level:_addMaterialThis.level,color:_addMaterialThis.color,width:_addMaterialThis.width,thick:_addMaterialThis.thick}),
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
			    alert('添加成功')
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
			};
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });
		
	    },
	
	    showrecord: function(){
		var _getAllMaterialThis = this;
		_getAllMaterialThis.isShowRecord = true;
		_getAllMaterialThis.isShowQuery = false;
		_getAllMaterialThis.isShowManager = false;
		_getAllMaterialThis.isShowDetail = false;
		$.ajax({
                    type : 'post',
                    dataType : 'json',
                    url :  starturl + apiurl.getallmaterialUrl,
                    data: JSON.stringify({action:'getallmat'}),
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
                            var result = response['result'];
			    _getAllMaterialThis.material_list = result;
			    _getAllMaterialThis.id = result[0]['ID'];
			    _getAllMaterialThis.materialname = result[0]['materialname'];
			    _getAllMaterialThis.manufacturer = result[0]['manufacturer'];
			    _getAllMaterialThis.level = result[0]['level'];
			    _getAllMaterialThis.color = result[0]['color'];
			    _getAllMaterialThis.width = result[0]['width'];
			    _getAllMaterialThis.thick = result[0]['thick'];
			    
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
			};
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });
		
	    },
	    
	    selectmaterial: function(ele){
	    	var _selectMaterialThis = this;
		_selectMaterialThis.id = this.material_list[ele.target.value]['ID'];
	        _selectMaterialThis.materialname = this.material_list[ele.target.value]['materialname'];
		_selectMaterialThis.manufacturer = this.material_list[ele.target.value]['manufacturer'];
		_selectMaterialThis.level = this.material_list[ele.target.value]['level'];
		_selectMaterialThis.color = this.material_list[ele.target.value]['color'];
		_selectMaterialThis.width = this.material_list[ele.target.value]['width'];
		_selectMaterialThis.thick = this.material_list[ele.target.value]['thick'];
	    },
	    
	    storageaction: function(){
	        var _storageActionThis = this;
		$.ajax({
                    type : 'post',
                    dataType : 'json',
                    url :  starturl + apiurl.storageactionUrl,
                    data: JSON.stringify({action:'storage',id:_storageActionThis.id,direction:_storageActionThis.direction,amount:_storageActionThis.amount,batch_number:_storageActionThis.batch_number}),
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
                            alert('操作成功');
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
			};
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });
		

	    
	    },
	    
	    checkid: function(index){
	    	 var _checkidThis = this;
		 id = _checkidThis.material_list[index]["ID"];
		 index = _checkidThis.material_list.indexOf(id);
		 if(index==-1){
		    _checkidThis.id_list.push(id);
		 }else{
		    _checkidThis.id_list = _checkidThis.material_list.splice(index,1);
		 };
	    },

	    closerecord:  function(){
	    	var _closeRecordThis = this;
		_closeRecordThis.isShowRecord = false;
	    },
	    
	    showquery: function(){
		var _getAllMaterialThis = this;
		_getAllMaterialThis.isShowQuery = true;
		_getAllMaterialThis.isShowRecord = false;
		_getAllMaterialThis.isShowDetail = false;
		_getAllMaterialThis.isShowManager = false;
		$.ajax({
                    type : 'post',
                    dataType : 'json',
                    url :  starturl + apiurl.getallmaterialUrl,
                    data: JSON.stringify({action:'getallmat'}),
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
                            var result = response['result'];
			    _getAllMaterialThis.material_list = result;
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
			};
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });
	    },

	    closequery:  function(){
	    	var _closeRecordThis = this;
		_closeRecordThis.isShowQuery = false;
	    },

	    materialrest: function(){
		var _materialrestThis = this;
		$.ajax({
                    type : 'post',
                    dataType : 'json',
                    url :  starturl + apiurl.materialrestUrl,
                    data: JSON.stringify({action:'rest',id_list:_materialrestThis.id_list}),
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
			    var result = response['result'];
			    _materialrestThis.sum_list = result;
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
			};
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });
		
	    },
	    
	    getdetail: function(index,s){
		var _getdetailThis = this;
	        _getdetailThis.detail_list = _getdetailThis.sum_list[index][s];
		_getdetailThis.isShowDetail = true;
	    },
	    closedetail:  function(){
	    	var _closeRecordThis = this;
		_closeRecordThis.isShowDetail = false;
	    },

	    
            queryData: function(){
                var _queryDataThis = this;
                $.ajax({
                    type : 'post',
                    dataType : 'json',
                    url :  starturl + apiurl.getContentListUrl,
                    data: JSON.stringify({start_date:_queryDataThis.start_date, end_date:_queryDataThis.end_date, tag:_queryDataThis.tag}),
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
                            var result = response['result'];
                            _queryDataThis.content_list = result;
			    this.$options.methods.queryData.bind(this)();
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert('msg');
                        };
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });

            },
            subPage: function(item){
                window.open('../../static/myhtml/'+item.url,'_blank','width=600,height=400,top=100px,left=0px,toolbar=yes,scrollbars=yes,status=yes,menubar=yes')
            },

            showAddDetail: function(){
                this.isShowAddDetail = true;
            },

            closeAddDetail: function(){
                this.isShowAddDetail = false;
            },
	    
	    

            addData: function(){
                var _addDataThis = this;
                this.$options.methods.submitFile.bind(this)();

                $.ajax({
                    type : 'post',
                    dataType : 'json',
                    async : false,
                    url: starturl + apiurl.addOneItemUrl,
                    data: JSON.stringify({title:_addDataThis.title, tag:_addDataThis.tag, author:_addDataThis.author, url: _addDataThis.url}),
                    processData: false, 
                    contentType: false, 
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
                            alert('操作成功');
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
                        };
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });

           
            },
            submitFile : function(){
                var form = new FormData();
                form.append("file", this.uploadfile);

                $.ajax({
                    type : 'post',
                    dataType : 'json',
                    async : false,
                    url: starturl + apiurl.addOneFileUrl,
                    data: form,
                    contentType: false,  
                    processData: false,  
                    success:function(response){
                        var status = response['status'];
                        if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
                        };
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });
            },
            onfilechange : function(e){
                var files = e.target.files || e.dataTransfer.files;
                if (!files.length){
                    return;
                };
                this.uploadfile = files[0];
                this.url = files[0].name;
            },
            picTran : function(){
                var _picTranThis = this;
                this.$options.methods.submitFile.bind(this)();

                $.ajax({
                    type : 'post',
                    dataType : 'json',
                    async : false,
                    url: starturl + apiurl.picToEpsUrl,
                    data: JSON.stringify({From_fileName:this.url}),
                    processData: false, 
                    contentType: false, 
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
                            $('#pic_tran').attr('href','../static/myhtml/'+response['To_fileName']);
                            $('#pic_tran').attr('download',response['To_fileName']);
                            $('#pic_tran').text('点击下载');
                            alert('操作成功');
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
                        };
                    },
                    error:function(response){
                        alert('请求出错');
                    }
                })
            },
            showPicTran : function(){
                this.isShowPicTran = true;
            },
            closePicTran : function(){
                this.isShowPicTran = false;
            }


        }


    })

};

