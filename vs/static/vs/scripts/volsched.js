function enableIfNotNull(button, name) {
    if(name != null && trim(name) != "") {
        var tgt = document.getElementsByName(name);
        if(tgt != null) {
            if(tgt.length == 1)
            {
                if(trim(tgt[0].value) != "") {
                    button.disabled=false;
                }
            }
        }
    }    
}

function enableWidgets(doc) {
    if(doc != null) {
        var forms = doc.forms;
        if(forms != null ) {
            var formLoop = 0;
            for(formloop = 0; formLoop < forms.length; formLoop++) {
                var form = forms[formLoop];
                var widgets = form.elements;
                var loop = 0;
                for(loop = 0; loop < widgets.length; loop++) {
                    var widget = widgets[loop];
                    widget.disabled=false;
                }            
                widgets = document.forms[1].elements;
                loop = 0;
                for(loop = 0; loop < widgets.length; loop++) {
                    widget = widgets[loop];
                    widget.disabled=false;
                }               
            }
        }
    }    
}

function enableButton(item, name) 
{
    if(item != null) {
        var text = "" + item.value;
        if(text != null && trim(text) != "") {
            var tgt = document.getElementsByName(name);
            if(tgt != null) {
                if(tgt.length == 1)
                {
                    tgt[0].disabled=false;
                }
            }
        }
    }
}
    
function trim (str) {
    str = str.replace(/^\s+/, '');
    for (var i = str.length - 1; i >= 0; i--) {
        if (/\S/.test(str.charAt(i))) {
            str = str.substring(0, i + 1);
            break;
        }
    }
    return str;
}

function disableButtonsAndSubmit(item, display) {
    var formLoop = 0;
    forms = document.forms;
    for(formLoop = 0; formLoop < forms.length; formLoop++) {
        form = forms[formLoop];
        var widgets = form.elements;
        var loop = 0;
        for(loop = 0; loop < widgets.length; loop++) {
            var widget = widgets[loop];
            if(widget.type == "submit") {
                var name = widget.name;
                if(name != item.name) {
                    widget.disabled=true;
                }
            }
        }
    }
    disableAndSubmit(item, display);
}

function disableAndSubmit(item, display) {
    setButtonName(item);
    var form = item.form;
    var valid = true;
    if(item.value != "Delete" && item.value != "Cancel") {
      valid = validateTextFields(form, display);         
    }
    if(valid == true) {
      item.disabled=true;
      form.submit();
    }
}

function setButtonName(item) {
    var form = item.form;
    if(form != null) {
        var widgets = form.elements;
        if(widgets != null) {            
          var loop = 0;
          for(loop = 0; loop < widgets.length; loop++) {
              var widget = widgets[loop];
              if(widget.id == "buttonName") {
                widget.value=item.name;
                widget.name=item.name;
              }
          }
        }
    }
}
    
function validateTextFields(form, display) {
    var result = true;
    var validateRequired = true;
    var buttonName = document.getElementById("buttonName");
    if(buttonName != null) {
        if("Cancel" == buttonName.value) {
            validateRequired = false;
        }
        if("Delete" == buttonName.value) {
            validateRequired = false;
        }
    }
    if(validateRequired) {
      names = form.getAttribute("validateTextFieldNames");
      var errMsg = "";
      if(names != null) {
          var size = names.length;
          var loop = 0;
          for(loop = 0; loop < size && result == true; loop++) {
              var name = names[loop];
              var tf = document.getElementById(name);
              if(tf != null) {
                  var value = tf.value;                  
                  if(value == null || trim(value) == "") {
                      displayName = tf.getAttribute("displayName");
                      errMsg = displayName + " must not be blank or all spaces";
                      result = false;
                  }
              }
          }
      }
      if(result == false) {
          if(display == true) {
            alert(errMsg);
          }
      } else {
          result = validateNumericTextFields(form, true, display);
      }
      if(result == false) {
          enableAllButtons();
       }
    }
    return result;
}

function validateNumericTextFields(form, allowSpace, display) {
    var result = true;
    names = form.getAttribute("validateNumericFieldNames");
    if(names != null) {
          var size = names.length;
          var loop = 0;
          for(loop = 0; loop < size && result == true; loop++) {
              var name = names[loop];
              var tf = document.getElementById(name);
              if(tf != null) {
                  var value = tf.value;
                  if(validateNotEmpty(value) == false) {
                      if(allowSpace != true) {
                          result = false;
                          displayName = tf.getAttribute("displayName");
                          errMsg = displayName + " must not be blank or all spaces";
                      }
                  } else if(validateInteger(value) == false) {
                      result = false;
                      displayName = tf.getAttribute("displayName");
                      errMsg = displayName + " must be blank or numeric";
                  }
              }
          }
    }
      if(result == false) {
          if(display == true) {
            alert(errMsg);
          }
      }
    return result;
}

function enableAllButtons(formIn) {
    var forms = document.forms;
    var formLoop = 0;
    for(formLoop = 0; formLoop < forms.length; formLoop++) {
        var form = forms[formLoop];
        var widgets = form.elements;
        var loop = 0;
        for(loop = 0; loop < widgets.length; loop++) {
            var widget = widgets[loop];
            if(widget.type == "submit") {
              widget.disabled=false;
            }
        }
    }  
}

function checkForModal(link) {
	//alert(link)
	document = link.ownerDocument;
	//alert(document)
	document.myClickedLink = link
	href = link.getAttribute('href');
	//alert( href)
	idx = href.indexOf('qty=');
	//alert(idx)
	idxend = href.indexOf('&',idx);
	//alert(idxend)
	if(idxend > 0) {
		countStr = href.substring(idx + 4, idxend);
	} else {
		countStr = href.substring(idx + 4);
	}
	//alert(countStr)
	count = +countStr
	document.maxAvailable = count
	alert(count)
	if(count == 1) {	
		return true
	} else {
		//alert('going modal');
		var modal = document.getElementById("myModal");
		var modalMessage = document.getElementById("modalMessage");
		var msg = 'Enter a value between 1 and ZZZ';
		msg = msg.replace('ZZZ', countStr);
		modalMessage.innerText = msg;
		//alert(msg)
	  	/*var span = document.getElementsByClassName("modalclose")[0];
	  	span.onclick = function() {
	}*/
	  	modal.style.display = "block";
	}
	return false;
}
	
	function cancelParm() {
		//alert('cancelParm')
		document.myClickedLink = null
		var modal = document.getElementById("myModal");
	  	modal.style.display = "none";
	}
		
	function setParm() {
		var link = document.myClickedLink 
		var quantity = +(document.getElementById("quantity").value);
		//alert('quantity ' + quantity.constructor.name)
		if(quantity < 1 || quantity > document.maxAvailable) {
			return
		}
		href = link.href
		var rmdr = ''
		idx = href.indexOf('qty=');
		idxend = href.indexOf('&',idx);
		if(idxend > 0) {
			rmdr = href.substring(idxend);
		}
		newRef = href.substring(0, idx + 4);
		newRef += quantity
		newRef += rmdr
		window.location.replace(newRef)
		var modal = document.getElementById("myModal");
	  	modal.style.display = "none";
}

	
	function cancelParm() {
		//alert('cancelParm')
		document.myClickedLink = null
		var modal = document.getElementById("myModal");
	  	modal.style.display = "none";
	}
		
	function setParm() {
		var link = document.myClickedLink 
		var quantity = +(document.getElementById("quantity").value);
		//alert('quantity ' + quantity.constructor.name)
		if(quantity < 1 || quantity > document.maxAvailable) {
			return
		}
		href = link.href
		var rmdr = ''
		idx = href.indexOf('qty=');
		idxend = href.indexOf('&',idx);
		if(idxend > 0) {
			rmdr = href.substring(idxend);
		}
		newRef = href.substring(0, idx + 4);
		newRef += quantity
		newRef += rmdr
		window.location.replace(newRef)
		var modal = document.getElementById("myModal");
	  	modal.style.display = "none";
}