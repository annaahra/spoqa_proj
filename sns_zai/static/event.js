function init()
{   
    	$('#searchFriendTable').hide();
}
window.onload=init;

$(function()
{
// TOP
	$("#logout").click(function(){
		location.href = '/logout';
	});
	
	$("#show_join").click(function() {
		$('#join_area').show();
		$('#login_area').hide();
	});

	$("#cancel").click(function() {
		$('#login_area').show();
		$('#join_area').hide();
	});

// LEFT	
	// String Matching - kmp algorithm
	$("#searchFriend").keyup(function(){
		$('#searchFriendTable').show();

		var i = null;
		var opname = null;
		var rowN = null;
		var this_val = ($(this).val()).toLowerCase();
		
		if(this_val=="")
			init_searchTable();
		else
		for(i=0;(opname=($(document.getElementById("sft_"+i)).text()).replace(/\s/g, '').toLowerCase())!="";i++)
		{
			rowN = '#sft_row'+i;
			var result = kmp(opname, this_val);
			
			if(result==1)
			{
				$(rowN).show();
			}
			else
			{
				$(rowN).hide();
			}
		}
	});	
	$("#searchFriend").focusout(function(){
	//	$('#searchFriendTable').hide();
    });

// RIGHT
	$("#submitPost").click(function() {
		alert("submit post");
	});

	$("#getPost").click(function() {
		alert("refresh post");
	});

// FOCUS IN
	$("#searchFriend").focusin(function(){
		document.getElementById("searchFriend").value = ""
	});
	$("#post").focusin(function(){
		document.getElementById("post").value = ""
	});

});


function get_friendTable()
{
}
function get_searchTable()
{
}
function init_searchTable()
{
	var i = null;
	var opname = null;
	var rowN = null;
	
	for(i=0;(opname=($(document.getElementById("sft_"+i)).text()).replace(/\s/g, '').toLowerCase())!="";i++)
	{
		rowN = '#sft_row'+i;
		$(rowN).hide();
	}
}
function get_postTable()
{
}

function kmp(opname, this_val)
{
	var posP = 0;
	var posS = 0;
	var lengthP = this_val.length;
	var lengthS = opname.length;
	var f = new Array(lengthS);
	f = FailureFunction(opname, lengthS);
	
	while((posP<lengthP)&&(posS<lengthS))
		if(this_val[posP] == opname[posS]){
			posP++; posS++;
		}else if(posP == 0)	posS++;
		else	posP = f[posP -1]+1;
	if(posP<lengthP) return 0;
	else return 1;
}
function FailureFunction(opname, len)
{
		var lengthP = len;
		var f = new Array(len);
		var j;
		var i;
		f[0] = -1;
		for(j=1; j<lengthP; j++){
			i = f[j-1];
			while((opname[j]!=opname[i+1])&&(i>=0))	i=f[i];
			if(opname[j]==opname[i+1])	f[j] = i+1;
			else f[j] = -1;
		}
		return f;
}

function disableEnterKey(e)
{
     var key;
     if(window.event)
          key = window.event.keyCode;     //IE
     else
          key = e.which;     //firefox
     if(key == 13)
          return false;
     else
          return true;
}
