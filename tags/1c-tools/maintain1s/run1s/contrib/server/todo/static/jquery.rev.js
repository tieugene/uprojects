$(document).ready(function(){
setClickable();
});

function setClickable() {


$('#edit').click(function() {
var show = '<p>'+$(this).html()+'</p>';

var revert = $(this).html();

$(this).after(show).remove();
$('#update').click(function(){saveChanges(this, false);});
})
.mouseover(function() {
$(this).addClass("editable");
})
.mouseout(function() {
$(this).removeClass("editable");
});
};

function saveChanges(obj, cancel) {
if(!cancel) {
var t = $(obj).parent().siblings(0).val();
$.post("/update",{
  content: t
},function(txt){
alert( txt);
});
}
else {
var t = cancel;
}
if(t=='') t='(click to add text)';
$(obj).parent().parent().after('<div id="show">'+t+'</div>').remove();
setClickable();
}
