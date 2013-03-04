// glue between editinplace.js and behaviour.js

// behaviour provides this CSS selector style for the class="editable"
// that class is now mapped to the edit function of editinplace.js

    var myrules = {
        '.editable' : function(element){
            element.onclick = function(){
                edit($(this.id));
            }
        }
    };
    
    Behaviour.register(myrules);
