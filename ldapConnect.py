from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES
import settings

try:
    directoryServer = Server(settings.ldap["ldapServer"], get_info=ALL, use_ssl=True)
    ldapConnection = Connection(directoryServer, auto_bind=True,
                                user=settings.ldap["ldapAccessDomain"] + "\\" + settings.ldap["ldapAccessUserName"],
                                password=settings.ldap["ldapAccessPassword"], authentication=NTLM)
except:
    print("Can't connect to your LDAP server! Check your settings and try again!")
def getStudentName(id):
    searchName = "s" + str(id)  # adds s so you can search AD by student number...
    ldapConnection.search(settings.ldap["ldapSearchBase"], '(sAMAccountName=' + searchName + ')',
                                      attributes=ALL_ATTRIBUTES)
    ldapQueryResult = ldapConnection.entries[0] # there shouldn't be more than one entry anyway
    return ldapQueryResult.givenname.value + " " + ldapQueryResult.sn.value # first and last name

