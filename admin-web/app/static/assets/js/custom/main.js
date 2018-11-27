$(document).ready(
	function()
	{
		oMain.init();
	}
);
//window.sUrl= 	"http://admin.r2s.tirsolutions.com/";
window.oMain = {
  init : function(){

		Tickets.init();

		$('button[action="save"]').click(function(){
 			Tickets.aWidgets.Tickets.save();
 		});

		$('div[name="Tickets"]').on('hidden.bs.modal', function () {
			 Tickets.init();
			 Tickets.aWidgets.Tickets.removeError();
		});


		oPusher.init('support_requests' , 'new_ticket', function(aResp){
			 toastr.info(aResp, 'New Ticket Added');
			 Tickets.init();
		});

		$("input[name='chat_message']").keypress(function(e) {
		    if (e.which == 13) {
					 e.preventDefault();
					 if($("input[name='chat_message']").val()){
						 aModules.oChat.send();
					 }else{
						  toastr.error("Chat messege required", 'Opps Something went wrong');
					 }
		    }
		});

		$( "textarea[name='solution']"  ).keyup(function( event ) {
			if(!$(this).val()){
				var status = $("select[name='status']").val();
				if(status == 'CLOSED'){
					Tickets.aWidgets.Tickets.addError();
				}else{
					Tickets.aWidgets.Tickets.removeError();
				}
			}else {
				Tickets.aWidgets.Tickets.removeError();
			}
		});

		$( "select[name='status']"  ).change(function(){
			if(this.value == 'CLOSED'){
				$("textarea[name='solution']").removeAttr("disabled");
				if($( "textarea[name='solution']"  ).val()){
					Tickets.aWidgets.Tickets.removeError();
				}else{
					Tickets.aWidgets.Tickets.addError();
				}
			}else{
				Tickets.aWidgets.Tickets.removeError();
				$("textarea[name='solution']").attr("disabled","disabled");
			}
		});
  }
};

// Lazy loading Images
window.oLazyLoad = {
  img : {},
  loadingImg : null,
  init : function() {
    var aImg = this.get();
    this.lazyLoad(aImg);
  },
  get : function()
  {
    return document.getElementsByClassName('lazy');
  },
  lazyLoad : function(aArg){
    for(var i = 0 ; i < aArg.length ; i++ ){
      var src = aArg[i].getAttribute('data-src');
      if(this.elementInViewPort(aArg[i])){
        aArg[i].setAttribute('src', aArg[i].getAttribute('data-src'));
      }
    }
  },
  elementInViewPort : function(el) {
    var rect = el.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right  <=  (window.innerWidth || document.documentElement.clientWidth)
    );
  }
};

//tickets
window.aModules = {
	aChatMessage : function(aArg){
		var Msg  = '<div class="direct-chat-msg right">'+
			'<div class="direct-chat-info clearfix">'+
				'<span class="direct-chat-name pull-left">'+ $("input[name='sFullName']").val()+'</span>'+
				'<span class="direct-chat-timestamp pull-right">23 Jan 2:00 pm</span>'+
			'</div>'+
			'<img class="direct-chat-img" src="https://adminlte.io/themes/AdminLTE/dist/img/user1-128x128.jpg" alt="message user image">'+
			'<div class="direct-chat-text">'+
				aData.sMsg+
			'</div>'+
		'</div>';

		return Msg;
	},

	oChat : {
		send : function() {
			var oSelf = this;
			var reference_code = $("input[name='reference_code']").val();
			oRequest.apiCall(sUrl+"/admin/supportrequests/"+reference_code, 'POST'  , {
					message : $("input[name='chat_message']").val(),
					csrf_token : $("input[name='csrf_token']").val()
			} , function(resp){
				if(resp.support_requests.conversations){
					 aModules.oChat.render(resp.support_requests.conversations);
				 }
				$("input[name='chat_message']").val('');
			});

		},
		render : function(aArg , reference_code){
			var Msgs = '';
			$.each(aArg, function( index, value ) {
				//console.log(value);
				Msgs  += '<div class="direct-chat-msg '+ ( value.sender_type =='Client' ? '' : 'right') +'">'+
					'<div class="direct-chat-info clearfix">'+
						'<span class="direct-chat-name pull-left">'+value.sender_name+'</span>'+
						'<span class="direct-chat-timestamp pull-right">'+value.date_submitted+'</span>'+
					'</div>'+
					'<img class="direct-chat-img" src="https://adminlte.io/themes/AdminLTE/dist/img/user1-128x128.jpg" alt="message user image">'+
					'<div class="direct-chat-text">'+
						value.message+
					'</div>'+
				'</div>';
			});
			if(reference_code){
				$('div[reference="'+reference_code+'"]').html(Msgs);
			}else{
				$('.direct-chat-messages').html(Msgs);
			}
		},

		keyPress : function(e){
			e.preventDefault();
			 alert("d");
			 return true;
		}
	}
};

window.oPusher = {
	init : function (sChannel,sEvent,cCb){
		Pusher.logToConsole = false;
		var pusher = new Pusher('07dd89e378d9a7f925bd', {
			cluster: 'ap1',
			encrypted: true
		});
		var channel = pusher.subscribe(sChannel);
		channel.bind(sEvent, function(aResp) {
			cCb(aResp);
		});
	}
};

window.Tickets =
{
	bInit	: false,
	sTitle	: 'Tickets Tickets',
	sDesc	: '',
	init	: function(aArg, cCb)
	{
		this.aWidgets.Tickets.init(aArg, cCb);
	},

	aWidgets :
	{
		Tickets :
		{
			oForm		: null,
			bInit		: false,
			sModule		: 'Tickets',
			sIndex		: 'iTicketsId',
			sItem		: 'tickets',
			oInterval : {},
			aDataTable	: {
				sId			: '#TicketsDataTable',
				sTable		: 'Tickets',
				sModule		: 'Tickets',
        aColumns	: [
					{
						sTitle		: 'Reference Code',
						mData		  : 'id',
						bVisible : false
					},
					{
						sTitle		: 'Reference Code',
						mData		  : 'reference_code',
						sWidth		: 10,
						render : function(data, type, row){
							return '<a href="javascript:Tickets.aWidgets.Tickets.form(\'' + row.reference_code + '\')">'+(row.status == 'PENDING' ? '<strong>'+data+'<strong>' : data)+'</a>'
						}
					},
					{
						sTitle		: 'Sender name ',
						mData		: 'sender_name',
						sWidth		: 20,
						render  : function(data, type, row){
							return row.status == 'PENDING' ? '<strong>'+data+'<strong>' : data;
						}
					},{
						sTitle		: 'Subject ',
						mData		: 'subject',
						sWidth		: 20,
						render  : function(data, type, row){
							return row.status == 'PENDING' ? '<strong>'+data+'<strong>' : data;
						}

					},{
						sTitle		: 'Message ',
						mData		: 'message',
						sWidth		: 20,
						render  : function(data, type, row){
							return row.status == 'PENDING' ? '<strong>'+data+'<strong>' : data;
						}
					},{
						sTitle		: 'Date accepted',
						mData		: 'support_date_started',
						sWidth		: 10,
						render : function(data, type, row)
						{
							var dateTime = new Date(data);
							dateTime = moment(dateTime).format("DD-MM-YYYY HH:mm:ss");
							return data ? dateTime : '';
							//return data ? oPhp.date("d-m-Y H:i:s",oPhp.strtotime(row.support_date_started)).toString() : '';
							//Date.parse(new Date(data)).toString('dd-MM-yyyy H:i:s')
						}
					},
					{
						sTitle		: 'Date created',
						mData		: 'created_date',
						sWidth		: 10,
						render : function(data, type, row)
						{
							var dateTime = new Date(data);
							dateTime = moment(dateTime).format("DD-MM-YYYY HH:mm:ss");
							return data ? dateTime : '';
							//return data ? oPhp.date("d-m-Y H:i:s",oPhp.strtotime(row.support_date_started)).toString() : '';
							//Date.parse(new Date(data)).toString('dd-MM-yyyy H:i:s')
						}
					},
				  {
					sTitle	: 'Actions',
					mData		: 'status',
					sWidth	: 30,
					render  : function(data, type, row){
						return '<div class="btn-group">'+
								'<button type="button" class="btn btn-primary">'+row.status+'</button>'+
								'<button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown">'+
									'<span class="caret"></span>'+
								'</button>'+
								'<ul class="dropdown-menu" role="menu">'+
									'<li><a href="javascript:Tickets.aWidgets.Tickets.form(\'' + row.reference_code + '\')"><i class="fa fa-search"></i>View</a></li>'+
								'</ul>'+
							'</div>';
					}
				}]
		    },
				aValidation : {
					debug: true,
					rules: {
						id	    : {},
						message	: { required: true },
						subject					: { required: true },
						reference_code  : {},
						solution				: {},
						issuer_name     : {},
						status        	: {},

					}
				},
			init : function(aArg, cCb)
			{

				var oSelf = this;
				oRequest.apiCall(sUrl+"/admin/supportrequests", 'GET'  , null , function(resp){

					var pending = 0;
					var ongoing = 0;
					var closed  = 0;
					console.log(resp);
					$.each(resp.support_requests,function(i,v){
						if(v.status == "PENDING"){
							pending = pending+1;
						}

						if(v.status == "ONGOING"){
							ongoing = ongoing+1;
						}

						if(v.status == "CLOSED"){
							closed = closed+1;
						}
					});
					$('span[name="pending"]').html(pending);
					$('span[name="ongoing"]').html(ongoing);
					$('span[name="closed"]').html(closed);

					oTables.render([{
						sTableId : oSelf.aDataTable.sId ,
						aData    : resp.support_requests,
						aColumns : oSelf.aDataTable.aColumns
					}]);
				});
			},

			addError : function(){
				$('div.solutions').addClass('has-error');
				$('span.help-block').html('Solutions is Required');
				$('button[name=save]').attr('disabled','disabled');
			},
			removeError : function()
			{
				$('div.solutions').removeClass('has-error');
				$('span.help-block').html('');
				$('button[name=save]').removeAttr('disabled');
			},

			exit : function(){
				$("div[name='Tickets']").modal('hide');
				this.init();
			},

			form : function(aArg){
					var oSelf = this;
					if(aArg){
						var oSelf = this;
						oRequest.apiCall(sUrl+"/admin/supportrequests/"+aArg, 'GET'  , null , function(aResp){
							$.each( oSelf.aValidation.rules , function( key, value ) {
								$("*[name='"+key+"']").val(aResp.support_requests[key]);
								if(key== 'status'){
									if(aResp.support_requests[key] == 'CLOSED'){
										$("select[name='"+key+"']").attr("disabled","disabled");
										$("button[name='save']").attr("disabled","disabled");
									}else{
										$("select[name='"+key+"']").removeAttr("disabled");
									}
								}
							});
						  if(aResp.support_requests.conversations){
									aModules.oChat.render(aResp.support_requests.conversations);
							}
						  if(aResp.iStatus == 1){
									$("input[name='message']").removeAttr("disabled");
									$("a#sendBtn").attr("href","javascript:aModules.oChat.send()");
							}else{
									$("input[name='message']").attr("disabled","disabled");
									$("a#sendBtn").removeAttr("href");
							}
						  $("div[name='Tickets']").modal('show');
							oScroll.scrollToBottom();
						  oPusher.init('support_requests',aResp.support_requests.reference_code ,function(resp){
							 oRequest.apiCall(sUrl+"/admin/supportrequests/"+aResp.support_requests.reference_code, 'GET'  , null , function(resp){
								 if(resp.support_requests.conversations){
										aModules.oChat.render(resp.support_requests.conversations,resp.support_requests.reference_code);
									oScroll.scrollToBottom();
									}
							 });
						  });

						 $("textarea[name='solution']").attr("disabled","disabled");
						 $('.direct-chat-messages').attr("Reference",aResp.support_requests.reference_code);
						});
					}else{
						$('.addForm').show();
						$('.btnAdd').show();
						$('.ViewConversation').hide();
						$('#ticketsModal').modal('show');
					}
			},
			ramdom : function(){
				var text = "";
				 var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

				 for (var i = 0; i < 15; i++)
					 text += possible.charAt(Math.floor(Math.random() * possible.length));
				 return text;
			},
			save : function(oNode, aArg)
			{
				var oSelf = this;
				var aFieldData = {};
				$.each( oSelf.aValidation.rules , function( key, value ) {
					if(key == 'solution'){
						aFieldData[key] =  $("*[name='"+key+"']").val();
					}else if($("*[name='"+key+"']").val()){
						aFieldData[key] =  $("*[name='"+key+"']").val();
					}
				});

				if(aFieldData['status'] == 'CLOSED'){
					if(!aFieldData['solution']){
						oSelf.addError();
						return false;
					}
				}
				aFieldData['csrf_token'] = $("input[name='csrf_token']").val();
				oRequest.apiCall(sUrl+"/admin/supportrequests", 'POST'  , aFieldData , function(resp){
					toastr.success('Success!', 'Ticket Updated Successfully');
					$('input[name="Tickets"]').modal('hide');
					Tickets.init();
				});

			},
			filterTable : function(sArg)
			{
				oTable = $('#TicketsDataTable').dataTable();
				var Filtered = oTable.fnFilter( sArg );
		    return Filtered;
			},
		}
	}
};

window.oTables = {
  render :  function(aArg){
		var oTable = $(aArg[0].sTableId);
		if(oTable){
			if ( $.fn.DataTable.fnIsDataTable(oTable) ) {
					oTable.DataTable().clear().draw();
					oTable.DataTable().rows.add(aArg[0].aData);
					oTable.DataTable().columns.adjust().draw();
			}else{

					oTable.DataTable({
						data 	  : aArg[0].aData,
						columns : aArg[0].aColumns,
						order: [[ 0, "desc" ]],
						//columnDefs: [ { type: "datetime-moment", targets: 5 } ],
						aoColumnDefs: [{ "sType": "date-uk", "aTargets": [5,6] }]
					});
			}
		}
	},
  status : function(aArg)
	{
		var aColumns	= [];
		if (aArg.aColumns) {
			for (var i = 0, l = aArg.aColumns.length, mData; i < l; i++) {
				mData	= aArg.aRow[aArg.aColumns[i]];
				if (aArg.aPadding) {
					aArg.aPadding[i][0][0] && (mData = oPhp.str_pad(mData, aArg.aPadding[i][0][0], aArg.aPadding[i][0][1], 'STR_PAD_LEFT'));
					aArg.aPadding[i][1][0] && (mData = oPhp.str_pad(mData, aArg.aPadding[i][1][0], aArg.aPadding[i][1][1], 'STR_PAD_RIGHT'));
				}
				aColumns.push(mData);
			}
		}

		return (
			(aArg.aRow.bActive != undefined || aArg.aRow.bDeleted != undefined) ?
			parseInt(aArg.aRow.bDeleted) ?
			'<i class="fa fa-trash text-danger"></i>' : (
				aArg.aRow.bActive == undefined || parseInt(aArg.aRow.bActive) ?
				'<i class="fa fa-check-circle-o text-success"></i>' :
				'<i class="fa fa-times-circle-o text-danger"></i>'
			) :
			''
		)+aColumns.join(' ');
	}
};

window.oRequest = {
  call : function(aArg,cCb){
    $.ajax({
      url			: 'http://localhost/acl/openapi/',
      type		: 'POST',
      dataType	  : 'text',
      processData	: false,
      data			: window.btoa(JSON.stringify(aArg)),
      success		: function(sResp)
      {

        cCb(jQuery.parseJSON(sResp));
      },
      complete : function(oXhr, sStatus)
      {
        $('#cover').fadeOut(300);
      },
      error : function(oXhr, sStatus, Ticketsg)
      {
        $('#cover').fadeOut(300);
      }
    });
  },
	apiCall : function(sUrl, type  , aArg , cCb){
		$("button[name='chatBtn']").attr("disabled","disabled");
		$("button[name='chatBtn']").html("Sending...");
		$("input[name='chat_message']").attr("disabled","disabled");
		$.ajaxSetup({
			headers: {
					'X-CSRF-Token': $("input[name='csrf_token']").val()
			}
		});

    $.ajax({
      url			: sUrl,
      type		: type,
      dataType	: 'json',
			//contentType: "application/json; charset=utf-8",
      data			: aArg ? aArg : null,
      success		: function(sResp)
      {
				$("button[name='chatBtn']").removeAttr('disabled');
				$("button[name='chatBtn']").html("Send");
				$("input[name='chat_message']").removeAttr("disabled");
        cCb(sResp);
      },

      complete : function(oXhr, sStatus)
      {
        $('#cover').fadeOut(300);
      },

      error : function(oXhr, sStatus, Ticketsg)
      {
        $('#cover').fadeOut(300);
      }
    });
  },
	callNoHeaders : function(sUrl , sMethod , aArg , cCb ){
		$("div#divLoading").addClass('show');
    $.ajaxPrefilter(function(options, originalOptions, xhr){
      if (options.crossDomain) {
        delete options.headers["X-CSRF-Token"]
      }
    });

    $.ajax({
      url			  : $.trim(sUrl),
      global: false,
      type    : sMethod,
      dataType	: 'json',
			data			: aArg ? aArg : null,
      headers : {
           'Content-Type': 'application/x-www-form-urlencoded'
      },
      success		: function(sResp)
      {
				  $("div#divLoading").removeClass('show');
          cCb(sResp);
      },
			error : function(sResp){
				 $("div#divLoading").removeClass('show');
				cCb(sResp);
			}
    });
  }
};
window.oScroll = {
	scrollToBottom : function () {
		var div = $(".direct-chat-messages");
		console.log(div.prop('scrollHeight'));
	  div.scrollTop(div.prop('scrollHeight'));
	},
};

$.extend(jQuery.fn.dataTableExt.oSort, {
	"date-uk-pre": function (a) {
	var x;
	try {
	var dateA = a.replace(/ /g, '').split("-");
	var day = parseInt(dateA[0], 10);
	var month = parseInt(dateA[1], 10);
	var year = parseInt(dateA[2], 10);
	var date = new Date(year, month - 1, day)
	x = date.getTime();
	}
	catch (err) {
	x = new Date().getTime();
	}

	return x;
	},

	"date-uk-asc": function (a, b) {
	return a - b;
	},

	"date-uk-desc": function (a, b) {
	return b - a;
	}
	});

	jQuery.extend( jQuery.fn.dataTableExt.oSort, {
  "datetime-us-flex-pre": function ( a ) {
    // If there's no slash, then it's not an actual date, so return zero for sorting
    if(a.indexOf('/') === -1) {
        return '0';
    } else {
      // Set optional items to zero
      var hour = 0,
          min = 0,
          ap = 0;
      // Execute match. Requires month, day, year. Can be mm/dd or m/d. Can be yy or yyyy
      // Time is optional. am/pm is optional
      // TODO - remove extra time column from array
      var b = a.match(/(\d{1,2})\/(\d{1,2})\/(\d{2,4})( (\d{1,2}):(\d{1,2}))? ?(am|pm|AM|PM|Am|Pm)?/),
          month = b[1],
          day = b[2],
          year = b[3];
      // If time exists then output hours and minutes
      if (b[4] != undefined) {
        hour = b[5];
        min = b[6];
      }
      // if using am/pm then change the hour to 24 hour format for sorting
      if (b[7] != undefined) {
        ap = b[7];
        if(hour == '12') hour = '0';
        if(ap == 'pm') hour = parseInt(hour, 10)+12;
      }

      // for 2 digit years, changes to 20__ if less than 70
      if(year.length == 2){
        if(parseInt(year, 10) < 70) year = '20'+year;
        else year = '19'+year;
      }
      // Converts single digits
      if(month.length == 1) month = '0'+month;
      if(day.length == 1) day = '0'+day;
      if(hour.length == 1) hour = '0'+hour;
      if(min.length == 1) min = '0'+min;
      var tt = year+month+day+hour+min;

      return tt;
    }
  },
  "datetime-us-flex-asc": function ( a, b ) {
    return a - b;
  },
  "datetime-us-flex-desc": function ( a, b ) {
    return b - a;
  }
});

$.fn.dataTable.moment = function ( format, locale ) {
    var types = $.fn.dataTable.ext.type;

    // Add type detection
    types.detect.unshift( function ( d ) {
        return moment( d, format, locale, true ).isValid() ?
            'moment-'+format :
            null;
    } );

    // Add sorting method - use an integer for the sorting
    types.order[ 'moment-'+format+'-pre' ] = function ( d ) {
        return moment( d, format, locale, true ).unix();
    };
};
