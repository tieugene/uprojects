var D=document;

function _init_auto_gray()
{
	var tags=['input', 'textarea'];
	for(var j=0;j<tags.length;j++)
	{
		var objs=D.getElementsByTagName(tags[j]);
		for(var i=0;i<objs.length;i++)
			if(_attr(objs[i], 'role')=="auto_gray")
			{
				_swc_obj(objs[i], '+bglgray');
				objs[i].onfocus=function(){_swc_obj(this, '-bglgray')}
				objs[i].onblur=function(){_swc_obj(this, '+bglgray')}
			}
	}
}

function _load_block(id, req_url)
{
	if(!_gete(id).loaded) {_req(req_url); _gete(id).loaded=1;}
	_swc(id, 'off');
	return false;
}

function _next_sib(obj)
{
	while(1){obj=obj.nextSibling; if(!obj || obj.nodeType==1) return obj;}
}

function _prev_sib(obj)
{
	while(1){obj=obj.previousSibling; if(!obj || obj.nodeType==1) return obj;}
}

function _attr(obj, name)
{
	var attr;
	if(!obj || !obj.attributes || !obj.attributes.getNamedItem || !(attr=obj.attributes.getNamedItem(name))) return false;
	return attr.value;
}

function _aproc(xml, fobj, xmldoc)
{
	if(xmldoc)
	{
		xml=xmldoc;
	}
	else if(fobj)
	{
		var xml=fobj.contentWindow.document;
		if(xml.XMLDocument) xml=xml.XMLDocument;
	}

	if(!xml) return;
	var ins=xml.getElementsByTagName("acts");
	if(!ins[0]) return;
	var ins=ins[0].getElementsByTagName("act");
	for(var i=0;i<ins.length;i++)
	{
		var ats={}, attrs=ins[i].attributes;
		for(var a=0;a<attrs.length;a++) ats[attrs[a].nodeName]=attrs[a].nodeValue;
		
		var data="";
		for(var dobj=ins[i].firstChild;dobj;dobj=dobj.nextSibling) data+=dobj.data;
		if(ats['do']=="set" || ats['do']=="tset")
		{
			var os=ats['id'].split(",");
			for(var j=0;j<os.length;j++)
			{
				var o=_gete(os[j]);
				if(!o) continue;
				if(typeof(ats['class'])!="undefined") o.className=ats['class'];
				if(ats['do']=="set") o.innerHTML=data;
				else o.innerText=data;
			}
		}
		else if(ats['do']=="append")
		{
			var os=ats['id'].split(",");
			for(var j=0;j<os.length;j++)
			{
				var o=_gete(os[j]);
				if(!o) continue;
				var o1=document.createElement(ats['tag']);
				o1.id=ats['tag_id'];
				o.appendChild(o1);
				o1.innerHTML=data;
			}
		}
		else if(ats['do']=="set_cell" || ats['do']=="tset_cell")
		{
			var os=ats['id'].split(","), index=ats['index'];
			for(var j=0;j<os.length;j++)
			{
				var o=_gete(os[j]);
				if(!o) continue;
				o=o.cells[index];
				if(typeof(ats['class'])!="undefined") o.className=ats['class'];
				if(ats['do']=="set_cell") o.innerHTML=data;
				else o.innerText=data;
			}
		}
		else if(ats['do']=="setc")
		{
			var os=ats['id'].split(",");
			for(var j=0;j<os.length;j++)
			{
				var o=_gete(os[j]);
				if(!o) continue;
				o.className=data;
			}
		}
		else if(ats['do']=="eval") eval(data);
	}
}

function _post(vars, func, pathname, host)
{
	if(!host) host=document.location.host;
	if(!pathname) pathname=document.location.pathname;
	if(typeof(func)=="undefined") func="_aproc(xml)";

	var req=window.XMLHttpRequest?new XMLHttpRequest():new ActiveXObject("Microsoft.XMLHTTP");
	req.onreadystatechange=function(){
		if(req.readyState==4)
		{
			var xml=req.responseXML;
			var txt=req.responseText;
			if(xml && xml.XMLDocument) xml=xml.XMLDocument;
			eval(func);
			req=null;
		}
	}
	
	var pairs=[];
	for(var i in vars) pairs.push(i+"="+_win(vars[i]+''));
	var qs=pairs.join("&");

//	alert(qs);
	req.open("POST", "http://"+host+pathname+"?"+Math.random(), true);
	req.setRequestHeader("Cookie", document.cookie);
	req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=windows-1251");
	req.setRequestHeader("Content-Length", qs.length);
	req.send(qs);

	return false;
}

function _req(qs, func, pathname, host)
{
	if(!host) host=document.location.host;
	if(!pathname) pathname=document.location.pathname;
	if(typeof(func)=="undefined") func="_aproc(xml)";

	var req=window.XMLHttpRequest?new XMLHttpRequest():new ActiveXObject("Microsoft.XMLHTTP");
	req.onreadystatechange=function(){
		if(req.readyState==4)
		{
			var xml=req.responseXML;
			var txt=req.responseText;
			if(xml && xml.XMLDocument) xml=xml.XMLDocument;
			eval(func);
			req=null;
		}
	}

//	alert("http://"+host+pathname+qs);
	req.open("GET", "http://"+host+pathname+qs+"&"+Math.random(), true);
	//req.open("GET", "http://"+host+pathname+_win(qs)+"&"+Math.random(), true);
	
	req.setRequestHeader("Cookie", document.cookie);
	req.send(null);

	return false;
}

function _fly(id, bind_id, dx, dy, ox, oy, rx, ry)
{
	var r=_setc_ex(id, 'fly', 'off');

	if(_gete(id).className!="off")
	{
		_gete(id).style.left=parseInt(_xoff(bind_id))+(ox?ox:0)-(rx?_gete(id).offsetWidth:0);
		_gete(id).style.top=parseInt(_yoff(bind_id))+(oy?oy:0)-(ry?_gete(id).offsetHeight:0);
		if(dx) _gete(id).style.width=dx;
		if(dy) _gete(id).style.height=dy;
	}

	if(!r) return false;
	return true;
}

function _xoff(id){for(var x=0,o=(typeof(id)=="object"?id:_gete(id));o;o=o.offsetParent) x+=o.offsetLeft; return x;}
function _yoff(id){for(var y=0,o=(typeof(id)=="object"?id:_gete(id));o;o=o.offsetParent) y+=o.offsetTop; return y;}

function _setc_ex(id, cl1, cl2)
{
	if(_gete(id).innerHTML.length>0) return _setc(id, cl1, cl2);
	return true;
}

function _xml_node(obj, tag, type)
{
	var tags=tag.split("/");
	
	for(var i=0;obj && i<tags.length;i++) obj=obj.getElementsByTagName(tags[i])[0];
	if(obj && obj.firstChild) return obj.firstChild.data;

	return false;
}

function _gete(id, w){return (w?w:window).document.getElementById(id);}

function _swc_obj(o, cl1, cl2)
{
	if(!o) return;
	var c=cl1.substr(0, 1);
	if(!cl2 && (c=="+" || c=="-"))
	{
		var r11=new RegExp('\\b'+cl1.substr(1)+'\\b');
		if(c=="+") {if(!o.className.match(r11)) o.className+=" "+cl1.substr(1);}
		else if(c=="-") o.className=o.className.replace(r11, "");
		return false;
	}

	var r1=new RegExp('\\b'+cl1+'\\b'), r2=new RegExp('\\b'+cl2+'\\b');
	var cls=o.className;

	if(cls.match(r1)) cls=cls.replace(r1, cl2);
	else if(cl2 && cls.match(r2)) cls=cls.replace(r2, cl1);
	else cls+=" "+cl1;
	o.className=cls;
	return false;
}

function _swc(id, cl1, cl2)
{

	var ids=id.split(",");
	for(var i=0;i<ids.length;i++) _swc_obj(_gete(ids[i]), cl1, cl2);
	return false;
}

function _setc(id, cl1, cl2, w)
{
	var ids=id.split(",");
	
	for(var i=0;i<ids.length;i++)
	{
		id=ids[i];
		var o=_gete(id, w);
		if(!o) continue;
		
		if(!cl2) o.className=cl1;
		else o.className=(o.className==cl1?cl2:cl1);
	}

	return false;
}

function _submit(frm, msg, js_req, pairs, path, host)
{
	var els=frm.elements;

	if(msg=="q") alert(1);

	var msgs=[], all_els=[], err_els=[];
	var params={};
	if(!pairs) pairs=[];
	else for(var i=0;i<pairs.length;i++)
	{
		var ar=pairs[i].split("=");
		params[ar[0]]=ar[1];
	}
	for(var i=0;i<els.length;i++)
	{
		el=els[i];
		if(el.check && el.offsetWidth>0)
		{
			all_els.push(el);
			var txt=el.check.replace(/^\S+\s+/, '');
			if(el.check.match(/^#/))
			{
				var ar=el.check.substr(1).split(' ');
				var r=new RegExp(ar[0]);
				if(!el.value.match(r)) {msgs.push(txt); err_els.push(el);}
			}
			else if(el.check.match(/^\S*N\+/) && !(parseFloat(el.value)>0)) {msgs.push(txt); err_els.push(el);}
		}
		if(!(el.type=="radio" || el.type=="checkbox") || el.checked)
			if(el.name) {pairs.push(el.name+'='+_win(el.value+'')); params[el.name]=el.value;}
	}

	window.submit_result={'all_els': all_els, 'err_els': err_els};
	if(msgs.length) {alert(msg?msg:msgs.join(";\n")+"."); return false;}
	if(!js_req) return true;

	if(js_req==2) _post(params, '_aproc(xml)', path, host);
	else _req("?"+pairs.join("&"), '_aproc(xml)', path, host);

	return false;
}

var win_chr=new Array('%C0','%C1','%C2','%C3','%C4','%C5','%C6','%C7','%C8','%C9','%CA','%CB','%CC','%CD','%CE','%CF','%D0','%D1','%D2','%D3','%D4','%D5','%D6','%D7','%D8','%D9','%DA','%DB','%DC','%DD','%DE','%DF','%E0','%E1','%E2','%E3','%E4','%E5','%E6','%E7','%E8','%E9','%EA','%EB','%EC','%ED','%EE','%EF','%F0','%F1','%F2','%F3','%F4','%F5','%F6','%F7','%F8','%F9','%FA','%FB','%FC','%FD','%FE','%FF','%A8','%B8');

function _win(str)
{
	var res='';
	for(var i=0;i<str.length;i++)
		if(str.charAt(i)>='А' && str.charAt(i)<='я') res+=win_chr[str.charCodeAt(i)-0x0410];
		else if(str.charAt(i)=='Ё') res+=win_chr[64];
		else if(str.charAt(i)=='ё') res+=win_chr[65];
		else if(str.charAt(i)=='=') res+='%3D';
		else if(str.charAt(i)=='&') res+='%26';
		else res+=str.charAt(i);

	return res;
}

function mlt_click(tag)
{
	_swc(tag+'_pop', 'off');
	
	return false;
}

function mlt_item_click(tag, id, checked)
{
	var o=_gete(tag+'_item_'+id);
	var val=_gete(tag+'_val');

	if(o)
	{
		if(checked) val.value+=','+o.value;
		else
		{
			var reg=new RegExp('\\b'+o.value+'\\b');
			val.value=val.value.replace(reg, '');
		}
	}
	val.value=val.value.replace(/\,{2,}/, ',');
	val.value=val.value.replace(/(^,|,$)/, '');
	val.value=val.value.split(',').sort().join(",");

	var val_ids=val.value.split(',');
	var strs=[];
	for(var i=0;i<val_ids.length;i++)
	{
		var it=_gete(tag+'_name_'+val_ids[i]);
		if(it) strs.push(it.innerHTML);
	}
	_gete(tag+"_txt").innerHTML=(strs.length>0?strs.join(", "):"установить");
}

// Ещё немного

function _id(id, w){return (w?w:window).document.getElementById(id);}

function _rl(obj, way)
{
	obj=obj.constructor==String?_id(obj):obj;
	var ways=way.split(/\s+/);
	for(var i in ways)
	{
		if(ways[i]=="ps") do{obj=obj.previousSibling} while(obj && obj.nodeType!=1);
		if(ways[i]=="ns") do{obj=obj.nextSibling} while(obj && obj.nodeType!=1);
		if(ways[i]=="p") obj=obj.parentNode;
		if(ways[i]=="c") {obj=obj.firstChild; while(obj && obj.nodeType!=1) obj=obj.nextSibling;}
	}
	return obj;
}

function _sc(objs, cmds)
{
	var cmds=cmds?cmds.split(/\s+/):['off'];
	if(objs.constructor!=Array) objs=[objs];
	for(var i in objs)
	{
		var obj=objs[i].constructor==String?_id(objs[i]):objs[i];
		var classes=obj.className.replace(/^\s+|\s+$/, '').split(/\s+/);
		for(var j in cmds)
		{
			var cmd=cmds[j], op=cmd.substr(0, 1), is_in=0;
			if(op=="+" || op=="-") cmd=cmd.substr(1);
			else op=false;
			for(var c in classes)
				if(classes[c]==cmd)
				{
					is_in=1;
					if(op!="+") classes[c]=null;
				}
			if(op!="-" && !is_in) classes.push(cmd);
		}
		obj.className=classes.join(' ');
	}
	return false;
}