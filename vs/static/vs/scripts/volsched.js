function enableIfNotNull(button, name) {
    if (name !== null && trim(name) !== "") {
        var tgt = document.getElementsByName(name);
        if (tgt !== null) {
            if (tgt.length === 1)
            {
                if (trim(tgt[0].value) !== "") {
                    button.disabled = false;
                }
            }
        }
    }
}

function clearEventsInputFields() {
    const inputNames = ["eventName",
        "startDate",
        "startTime",
        "duration",
        "endDate",
        "interval"];
    const selectNames = [
        "locationSelector",
        "recurs"
    ];
    return clearInputAndSelectorFields(inputNames, selectNames);
}

function resetEventFields() {
    const inputNames = ["eventName",
        "startDate",
        "startTime",
        "duration",
        "endDate",
        "interval"];
    const selectNames = [
        "locationSelector",
        "recurs"];
    var ctr = -1;
    for (const name of inputNames) {
        ctr++;
        var id = "form1:" + name;
        var item = document.getElementById(id);
        if (item !== null) {
            item.value = "";
            switch (ctr) {
                case 0:
                    item.value = "a";
                    break;
                case 1:
                    item.value = "01/01/2000";
                    break;
                case 2:
                    item.value = "00:00";
                    break;
                case 3:
                    item.value = "1";
                    break;
                default:
                    item.value = "";
            }
        }
    }
    for (const name of selectNames) {
        var id = "form1:" + name;
        var item = document.getElementById(id);
        if (item !== null) {
            item.selectedIndex = -1;
        }
    }
    return true;
}

function clearInputAndSelectorFields(inputNames, selectNames) {
    for (let x in inputNames) {
        var name = inputNames[x];
        var input = document.getElementById("form1:" + name);
        //alert(name + " input = " + input);
        if (input !== null) {
            input.value = null;
        }
    }
    for (let x in selectNames) {
        var name = selectNames[x];
        var select = document.getElementById("form1:" + name);
        select.selectedIndex = -1;
    }
    return true;
}

function isNumber(value) {
    return isNaN(Number(value)) === false;
}

function checkRange(num, min, max) {
    var result = isNumber(num);
    if (result) {
        result = isNumber(min);
    }
    if (result) {
        result = isNumber(max);
    }
    ;
    var xNum = parseInt(num);
    var xMin = parseInt(min);
    var xMax = parseInt(max);
    if (result) {
        result = xNum >= xMin;
    }
    if (result) {
        result = xNum <= xMax;
    }
    return result;
}

function reopenWindow() {
    window.location.reload(true);
}

function moveRight() {
    var lt = document.getElementById("leftTable");
    var rt = document.getElementById("rightTable");
    var idx = lt.selectedIndex;
    var opt = lt.options[idx];
    lt.remove(idx);
    rt.add(opt);
    lt.selectedIndex = -1;
}

function moveLeft() {
    var lt = document.getElementById("leftTable");
    var rt = document.getElementById("rightTable");
    var idx = rt.selectedIndex;
    var opt = rt.options[idx];
    rt.remove(idx);
    lt.add(opt);
    rt.selectedIndex = -1;
}

function fixSubmitURL() {
    var form = document.getElementById('pdform');
    var tgt = form.action;
    var sel = document.getElementById("rightTable");
    var opts = sel.options;
    if (opts.length > 0) {
        tgt = tgt + "&teams=";
        for (var i = 0; i < opts.length; i++) {
            tgt = tgt + opts[i].value;
            tgt = tgt + "x";
        }
        form.action = tgt;
        alert(tgt);
    }
}

function enableWidgets(doc) {
    if (doc !== null) {
        var forms = doc.forms;
        if (forms !== null) {
            var formLoop = 0;
            for (formloop = 0; formLoop < forms.length; formLoop++) {
                var form = forms[formLoop];
                var widgets = form.elements;
                var loop = 0;
                for (loop = 0; loop < widgets.length; loop++) {
                    var widget = widgets[loop];
                    widget.disabled = false;
                }
                widgets = document.forms[1].elements;
                loop = 0;
                for (loop = 0; loop < widgets.length; loop++) {
                    widget = widgets[loop];
                    widget.disabled = false;
                }
            }
        }
    }
}

function enableButton(item, name)
{
    if (item !== null) {
        var text = "" + item.value;
        if (text !== null && trim(text) !== "") {
            var tgt = document.getElementsByName(name);
            if (tgt !== null) {
                if (tgt.length === 1)
                {
                    tgt[0].disabled = false;
                }
            }
        }
    }
}

function trim(str) {
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
    for (formLoop = 0; formLoop < forms.length; formLoop++) {
        form = forms[formLoop];
        var widgets = form.elements;
        var loop = 0;
        for (loop = 0; loop < widgets.length; loop++) {
            var widget = widgets[loop];
            if (widget.type === "submit") {
                var name = widget.name;
                if (name !== item.name) {
                    widget.disabled = true;
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
    if (item.value !== "Delete" && item.value !== "Cancel") {
        valid = validateTextFields(form, display);
    }
    if (valid === true) {
        item.disabled = true;
        form.submit();
    }
}

function setButtonName(item) {
    var form = item.form;
    if (form !== null) {
        var widgets = form.elements;
        if (widgets !== null) {
            var loop = 0;
            for (loop = 0; loop < widgets.length; loop++) {
                var widget = widgets[loop];
                if (widget.id === "buttonName") {
                    widget.value = item.name;
                    widget.name = item.name;
                }
            }
        }
    }
}

function validateTextFields(form, display) {
    var result = true;
    var validateRequired = true;
    var buttonName = document.getElementById("buttonName");
    if (buttonName !== null) {
        if ("Cancel" === buttonName.value) {
            validateRequired = false;
        }
        if ("Delete" === buttonName.value) {
            validateRequired = false;
        }
    }
    if (validateRequired) {
        names = form.getAttribute("validateTextFieldNames");
        var errMsg = "";
        if (names !== null) {
            var size = names.length;
            var loop = 0;
            for (loop = 0; loop < size && result === true; loop++) {
                var name = names[loop];
                var tf = document.getElementById(name);
                if (tf !== null) {
                    var value = tf.value;
                    if (value === null || trim(value) === "") {
                        displayName = tf.getAttribute("displayName");
                        errMsg = displayName + " must not be blank or all spaces";
                        result = false;
                    }
                }
            }
        }
        if (result === false) {
            if (display === true) {
                alert(errMsg);
            }
        } else {
            result = validateNumericTextFields(form, true, display);
        }
        if (result === false) {
            enableAllButtons();
        }
    }
    return result;
}

function validateNumericTextFields(form, allowSpace, display) {
    var result = true;
    names = form.getAttribute("validateNumericFieldNames");
    if (names !== null) {
        var size = names.length;
        var loop = 0;
        for (loop = 0; loop < size && result === true; loop++) {
            var name = names[loop];
            var tf = document.getElementById(name);
            if (tf !== null) {
                var value = tf.value;
                if (validateNotEmpty(value) === false) {
                    if (allowSpace !== true) {
                        result = false;
                        displayName = tf.getAttribute("displayName");
                        errMsg = displayName + " must not be blank or all spaces";
                    }
                } else if (validateInteger(value) === false) {
                    result = false;
                    displayName = tf.getAttribute("displayName");
                    errMsg = displayName + " must be blank or numeric";
                }
            }
        }
    }
    if (result === false) {
        if (display === true) {
            alert(errMsg);
        }
    }
    return result;
}

function enableAllButtons(formIn) {
    var forms = document.forms;
    var formLoop = 0;
    for (formLoop = 0; formLoop < forms.length; formLoop++) {
        var form = forms[formLoop];
        var widgets = form.elements;
        var loop = 0;
        for (loop = 0; loop < widgets.length; loop++) {
            var widget = widgets[loop];
            if (widget.type === "submit") {
                widget.disabled = false;
            }
        }
    }
}

function setResourceCount(resourceSelect) {
    resourceCountSelect = getForJSFelement("resourceNum");
    resourceCountSelect.options.length = 0;
    opts = getAvailabilityTable();
    opts = opts[resourceSelect.selectedIndex];
    for (loop in opts) {
        resourceCountSelect.add(opts[loop]);
    }

}

function getForJSFelement(fieldId) {
    var cls = null;
    getForJSFelement(fieldId, cls);
}

function getForJSFelement(fieldId, className) {
    if (className == null) {
        className = "forJSF";
    }
    var field = document.getElementById(fieldId);
    if (field == null) {
        var flds = document.getElementsByClassName(className);
        for (loop = 0; loop < flds.length; loop++) {
            var id = flds[loop].id;
            var idx = id.lastIndexOf(":");
            id = id.substring(idx + 1);
            var idUp = id.toString().toUpperCase();
            var fldUp = fieldId.toString().toUpperCase();
            if (idUp === fldUp) {
                field = flds[loop];
                break;
            }
        }
    }
    return field;
}

function clickButton(name) {
    var button = getForJSFelement(name);
    if (button !== null) {
        button.click();
    }
}

function clickComponentButton(name) {
    var button = getForJSFelement(name, "autoClickButton");
    if (button !== null) {
        button.click();
    }
}

function clickComponentButton(name, elementClass) {
    var cls = elementClass;
    if (cls === null) {
        cls = "autoClickButton";
    }
    var button = getForJSFelement(name, cls);
    if (button !== null) {
        button.click();
    }
}

function loaded() {
    doLoadProcessing();
}

function unloaded() {
    alert('closing');
}
function checkTaskDetailInput(isAdd) {
    var result = true;
    var msg = "";
    var rqdWidget = "";
    var available = "";
    if (isAdd) {
        rqdWidget = document.getElementById("form2:resourceAmt");
        available = document.volschedAmt;
    } else {
        rqdWidget = document.getElementById("form2:resourceRemoveAmt");
        available = document.volschedRemoveAmt;
    }
    var rqd = rqdWidget.value;
    if (isNumber(rqd) === false) {
        result = false;
    } else {
        result = checkRange(rqd, 0, available);
        if (result === false) {
            msg = "You must supply a quantity between 0 and " + available;
        }
    }
    if (result) {
        if (isAdd) {
            PF('resourceAmt').jq.val(rqd).trigger('change');
            PF('myAddDialogVar').hide();
        } else {
            PF('resourceRemoveAmt').jq.val(rqd).trigger('change');
            PF('myRemoceDialogVar').hide();
        }
    } else {
        msg = "Quantity must be a number between 0 and"
                + available
                + "\n You entered \"" + rqd + '"';
        alert(msg);
    }
    return result;
}

function prepareAddForPF(link) {
    var allInsTags = document.querySelectorAll('ins');
    allInsTags.forEach(insTag => {
        var tagContent = insTag.textContent;
        if (tagContent === "red") {
            var name = link.innerHTML;
            var idx = name.indexOf(':');
            name = name.substring(0, idx);
            insTag.textContent = name;
        }
    });
    var href = link.href;
    var args = href.split('&amp;');
    var amt = "";
    var resourceID = "";
    args.forEach(arg => {
        pair = arg.split("=");
        if (pair[0] === "qty") {
            amt = pair[1];
        }
        if (pair[0] === "id") {
            resourceID = pair[1];
        }
    });
    PF('resourceAmt').jq.val(amt);
    document.volschedAmt = amt;
    if (parseInt(amt) > 1) {
        PF('resourceID').jq.val(resourceID);
        PF('myAddDialogVar').show();
        return false;
    } else {
        return true;
    }
}

function prepareRemoveForPF(link) {
    var allInsTags = document.querySelectorAll('ins');
    allInsTags.forEach(insTag => {
        var tagContent = insTag.textContent;
        if (tagContent === "$blue") {
            var name = link.innerHTML;
            var idx = name.indexOf(':');
            name = name.substring(0, idx);
            insTag.textContent = name;
        }
    });
    var href = link.href;
    var args = href.split('&amp;');
    var amt = "";
    var resourceID = "";
    args.forEach(arg => {
        pair = arg.split("=");
        if (pair[0] === "qty") {
            amt = pair[1];
        }
        if (pair[0] === "id") {
            resourceID = pair[1];
        }
    });
    PF('resourceRemoveAmt').jq.val(amt);
    document.volschedRemoveAmt = amt;
    if (parseInt(amt) > 1) {
        PF('resourceRemoveID').jq.val(resourceID);
        PF('myRemoveDialogVar').show();
        return false;
    } else {
        return true;
    }
}