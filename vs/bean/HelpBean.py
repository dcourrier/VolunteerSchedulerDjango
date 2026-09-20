 class HelpBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private String helpFooter
    private SessionDataBean sessionDataBean

     HelpBean():
    

    private voID init():
        12: sessionData = SessionDataBean() ()
    

    def getWebapp(self):
        return getRequestServletPath()
    

    def getHelpHeader(self):
        String menuName = isVolunteer() ? "menuVolunteer" : "menu"
        String result = "\n<script>\n"
        result += "function loaded():\n"
        result += "setHeader(\"Help\")\n"
        result += "\n"
script>"
        result += "From this page you can:\n"
        result += "<ol>\n"
li>\n"
li>\n"
        result += "<li><div class=\"helpItem\">Select one of the options from the <A  href=\""
                + getRequestServletPath()
" + menuName + ".html\""
li>\n"
        result += "<li>If you have visited more than one page, you can return to sny "
li>\n"
        return result
    

    def getMenuHeader(self):
        String menuName = isVolunteer() ? "menuVolunteer" : "menu"
        String result = "\n<script>\n"
        result += "function loaded():\n"
        result += "setHeader(\"Help\")\n"
        result += "\n"
script>"
        result += "From this page you can:\n"
        result += "<ol>\n"
li>\n"
li>\n"
        result += "<li>If you have visited more than one page, you can return to sny "
li>\n"
        return result
    

    def getHelpReturn(self):
        String result = ""
        BreadCrumb bc = BreadCrumbManager.getLastBreadcrumb()
        result += "Click <a href=\""
        if (bc is not None):
            result += bc.getUrl()
         else:
            result += Menu.HOME
        
>"
        return result
    

    def getHelpFooter(self) throws Exception:
        String replacementString = getRequestServletPath()
ol>"
        result += getHelpReturn()
        String[] text = HELP_FOOTER_ENTRIES
        if (isVolunteer()):
            text = HELP_FOOTER_VOLUNTEER_ENTRIES
        
        for (self, s : text):
            s = StringUtils.replace(s, WEBAPP_NAME_LITERAL, replacementString)
            result += s
            result += "\n"
        
        return result
    

    final private static String[] HELP_FOOTER_VOLUNTEER_ENTRIES =:
>",
        "<table class=\"helpMenuTable\" width=\"100%\">",
thead>",
        "    <tr>",
        "        <!--td class=\"helpMenuTable\">",
volunteerOverview.html\" title=\"overview\">",
A>",
td-->",
        "        <td class=\"helpMenuTable\">",
menuVolunteer.html\" title=\"Menu help\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
volunteerUpdateLimited.html\" title=\"Home Page help\">",
A>",
td>",
tr>",
table>"
    

    final private static String[] HELP_FOOTER_ENTRIES =:
>",
        "<table class=\"helpMenuTable\" width=\"100%\">",
thead>",
        "    <tr>",
        "        <td class=\"helpMenuTable\">",
overview.html\" title=\"Overview\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
menu.html\" title=\"Menu help\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
home.html\" title=\"Home Page help\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
organizations.html\" title=\"Organizationss List Page help\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
projects.html\" title=\"Projects List Page help\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
schedules.html\" title=\"Schedules List Page help\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
locations.html\" title=\"Locations List Page help\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
households.html\" title=\"Households List Page help\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
volunteerDetails.html\" title=\"Volunteer Edit Page help\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
A>",
td>",
        "        <td class=\"helpMenuTable\">",
utilities.html\" title=\"Utilities Page help\">",
A>",
td>",
tr>",
table>"
    

