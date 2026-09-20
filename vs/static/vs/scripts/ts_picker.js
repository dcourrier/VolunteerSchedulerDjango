// Title: Timestamp picker
// Description: See the demo at url
// URL: http://us.geocities.com/tspicker/
// Script featured on: http://javascriptkit.com/script/script2/timestamp.shtml
// Version: 1.0
// Date: 12-05-2001 (mm-dd-yyyy)
// Author: Denis Gritcyuk <denis@softcomplex.com>; <tspicker@yahoo.com>
// Notes: Permission given to use this script in any kind of applications if
//    header lines are left unchanged. Feel free to contact the author
//    for feature requests and/or donations


function showCalendarForJSF(fieldId) {
    var field = null;
    var flds = document.getElementsByClassName("forJSF");
    for (loop = 0; loop < flds.length; loop++) {
        var id = flds[loop].id;
        var idUp = id.toString().toUpperCase();
        var fldUp = fieldId.toString().toUpperCase();
        if (idUp.endsWith(fldUp)) {
            field = flds[loop];
            break;
        }
    }
    if (field == null) {
        alert("Can't find '" + fieldId + "'");
    } else {
        document.$$DateField = field;
        show_calendar('document.$$DateField', document.$$DateField.value, '/MavenVolunteerSchedulerWARV4/resources/images');
    }
}

function showCalendar(fieldId) {
    var field = document.getElementById(fieldId);
    document.$$DateField = field;
    show_calendar('document.$$DateField', document.$$DateField.value, '/<%=Constants.WEBAPP_NAME%>/images');
}

function show_calendar(str_target, str_datetime, imgLocation) {
    var arr_months = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];
    var week_days = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
    var n_weekstart = 1; // day week starts from (normally 0 or 1)

    var dt_datetime = (str_datetime == null || str_datetime == "" ? new Date() : str2dt(str_datetime));
    var dt_prev_month = new Date(dt_datetime);
    dt_prev_month.setMonth(dt_datetime.getMonth() - 1);
    var dt_next_month = new Date(dt_datetime);
    dt_next_month.setMonth(dt_datetime.getMonth() + 1);
    var dt_firstday = new Date(dt_datetime);
    dt_firstday.setDate(1);
    dt_firstday.setDate(1 - (7 + dt_firstday.getDay() - n_weekstart) % 7);
    var dt_lastday = new Date(dt_next_month);
    dt_lastday.setDate(0);

    // html generation (feel free to tune it for your particular application)
    // print calendar header
    var str_buffer = new String(
            "<html>\n" +
            "<head>\n" +
            "	<title>Calendar</title>\n" +
            "</head>\n" +
            "<body bgcolor=\"White\">\n" +
            "<table class=\"clsOTable\" cellspacing=\"0\" border=\"0\" width=\"100%\">\n" +
            "<tr><td bgcolor=\"#4682B4\">\n" +
            "<table cellspacing=\"1\" cellpadding=\"3\" border=\"0\" width=\"100%\">\n" +
            "<tr>\n	<td bgcolor=\"#4682B4\"><a href=\"javascript:window.opener.show_calendar('" +
            str_target + "', '" + dt2dtstr(dt_prev_month) + "', '" + imgLocation + "');\">" +
            "<img src=\"" + imgLocation + "/prev.gif\" width=\"16\" height=\"16\" border=\"0\"" +
            " alt=\"previous month\"></a></td>\n" +
            "	<td bgcolor=\"#4682B4\" colspan=\"5\">" +
            "<font color=\"white\" face=\"tahoma, verdana\" size=\"2\">"
            + arr_months[dt_datetime.getMonth()] + " " + dt_datetime.getFullYear() + "</font></td>\n" +
            "	<td bgcolor=\"#4682B4\" align=\"right\"><a href=\"javascript:window.opener.show_calendar('"
            + str_target + "', '" + dt2dtstr(dt_next_month) + "', '" + imgLocation + "');\">" +
            "<img src=\"" + imgLocation + "/next.gif\" width=\"16\" height=\"16\" border=\"0\"" +
            " alt=\"next month\"></a></td>\n</tr>\n"
            );

    var dt_current_day = new Date(dt_firstday);
    // print weekdays titles
    str_buffer += "<tr>\n";
    for (var n = 0; n < 7; n++) {
        str_buffer += "	<td bgcolor=\"#87CEFA\">" +
                "<font color=\"white\" face=\"tahoma, verdana\" size=\"2\">" +
                week_days[(n_weekstart + n) % 7] + "</font></td>\n";
    }
    // print calendar table
    str_buffer += "</tr>\n";
    while (dt_current_day.getMonth() == dt_datetime.getMonth() ||
            dt_current_day.getMonth() == dt_firstday.getMonth()) {

        // print row header
        str_buffer += "<tr>\n";
        for (var n_current_wday = 0; n_current_wday < 7; n_current_wday++) {
            if (dt_current_day.getDate() == dt_datetime.getDate() &&
                    dt_current_day.getMonth() == dt_datetime.getMonth()) {
                // print current date
                str_buffer += "	<td bgcolor=\"#FFB6C1\" align=\"right\">";
            } else if (dt_current_day.getDay() == 0 || dt_current_day.getDay() == 6) {
                // weekend days
                str_buffer += "	<td bgcolor=\"#DBEAF5\" align=\"right\">";
            } else {
                // print working days of current month
                str_buffer += "	<td bgcolor=\"white\" align=\"right\">";
            }

            if (dt_current_day.getMonth() == dt_datetime.getMonth()) {
                // print days of current month
                str_buffer += "<a href=\"javascript:window.opener." + str_target +
                        ".value='" + dt2dtstr(dt_current_day) + "'; window.close();\">" +
                        "<font color=\"black\" face=\"tahoma, verdana\" size=\"2\">";
            } else {
                // print days of other months
                str_buffer += "<a href=\"javascript:window.opener." + str_target +
                        ".value='" + dt2dtstr(dt_current_day) + "'; window.close();\">" +
                        "<font color=\"gray\" face=\"tahoma, verdana\" size=\"2\">";
            }
            str_buffer += dt_current_day.getDate() + "</font></a></td>\n";
            dt_current_day.setDate(dt_current_day.getDate() + 1);
        }
        // print row footer
        str_buffer += "</tr>\n";
    }
    // print calendar footer
    str_buffer += "</td></tr>\n</table>\n</tr>\n</td>\n</table>\n</body>\n</html>\n";

    var vWinCal = window.open("", "Calendar",
            "width=200,height=250,status=no,resizable=yes,top=200,left=200");
    vWinCal.opener = self;
    var calc_doc = vWinCal.document;
    calc_doc.write(str_buffer);
    calc_doc.close();
}
// datetime parsing and formatting routimes. modify them if you wish other datetime format
function str2dt(str_datetime) {
    var trimmed = trim(str_datetime);
    var re_date = /^\d{1,2}(\-|\/|\.)\d{1,2}\1\d{4}$/;
    var parsedDate = Date.parse(trimmed);
    if (parsedDate == null) {
        return alert("Invalid Datetime format: \"" + str_datetime + "\"");
    }
    return parsedDate;
}
function dt2dtstr(dt_datetime) {
    return (new String(
            (dt_datetime.getMonth() + 1) + "/" + dt_datetime.getDate() + "/" + dt_datetime.getFullYear()));
}
function validateUSDate(strValue) {
    /************************************************
     DESCRIPTION: Validates that a string contains only
     valid dates with 2 digit month, 2 digit day,
     4 digit year. Date separator can be ., -, or /.
     Uses combination of regular expressions and
     string parsing to validate date.
     Ex. mm/dd/yyyy or mm-dd-yyyy or mm.dd.yyyy
     
     PARAMETERS:
     strValue - String to be tested for validity
     
     RETURNS:
     True if valid, otherwise false.
     
     REMARKS:
     Avoids some of the limitations of the Date.parse()
     method such as the date separator character.
     *************************************************/
    var objRegExp = /^\d{1,2}(\-|\/|\.)\d{1,2}\1\d{4}$/
    //check to see if in correct format
    if (!objRegExp.test(strValue)) {
        return false; //doesn't match pattern, bad date
    } else {
        var arrayDate = getDateArray(strValue);
        //create a lookup for months not equal to Feb.
        var arrayLookup = {'01': 31, '03': 31,
            '04': 30, '05': 31,
            '06': 30, '07': 31,
            '08': 31, '09': 30,
            '10': 31, '11': 30,
            '12': 31}
        var arrayLookup1 = {'1': 31, '3': 31,
            '4': 30, '5': 31,
            '6': 30, '7': 31,
            '8': 31, '9': 30,
            '10': 31, '11': 30,
            '12': 31}
        var intDay = parseInt(arrayDate[1], 10);

        //check if month value and day value agree
        if (arrayLookup[arrayDate[0]] != null) {
            if (intDay <= arrayLookup[arrayDate[0]] && intDay != 0)
                return true; //found in lookup table, good date
        } else if (arrayLookup1[arrayDate[0]] != null) {
            if (intDay <= arrayLookup1[arrayDate[0]] && intDay != 0)
                return true; //found in lookup table, good date
        } else {
            alert("failed lookup for " + arrayDate[0])
        }

        //check for February (bugfix 20050322)
        //bugfix  for parseInt kevin
        //bugfix  biss year  O.Jp Voutat
        var intMonth = parseInt(arrayDate[0], 10);
        if (intMonth == 2) {
            var intYear = parseInt(arrayDate[2]);
            if (intDay > 0 && intDay < 29) {
                return true;
            } else if (intDay == 29) {
                if ((intYear % 4 == 0) && (intYear % 100 != 0) ||
                        (intYear % 400 == 0)) {
                    // year div by 4 and ((not div by 100) or div by 400) ->ok
                    return true;
                }
            }
        }
    }
    return false; //any other values, bad date
}
