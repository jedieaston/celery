# Requires Schoolopy. Could I had used requests? yes, but this guy already did it.
import schoolopy
from modules.settings import schoology as settings
from flask import session
#auth = False
auth = schoolopy.Auth(settings['apiKey'], settings['apiSecret'], three_legged=True, domain=settings['instanceUrl'])
def authUrl(baseUrl):
    # Makes the URL to give to the user to authorize Celery to access Schoology.

    try:
        # Creates the URL that redirects back to celery
        url = "https://" + auth.request_authorization()
        urlsep = "oauth_callback="
        url = url.split(urlsep)[0] + 'oauth_callback=' + baseUrl
        return url
    except:
        #If we are authorized or something is wrong.
        return connectionCheck()

def connectionCheck(userAccessToken=None, userAccessTokenSecret=None):
    # Checks to make sure we have authorization, and if we don't, checks to see if we can use
    # preexisting schoology oauth credentials in a cookie (we probably cannot)
    global sc
    try:
        if userAccessToken == None and userAccessTokenSecret == None:
            check = auth.authorize()
            if check == True:
                session['schoologyUserAccessToken'] = auth.access_token
                session['schoologyUserAccessTokenSecret'] = auth.request_token_secret
                sc = schoolopy.Schoology
                sc = schoolopy.Schoology(auth)
                sc.limit = 5000         # TODO: This needs to be configurable!!!
                return True
            elif check == False:
                    # Recursion intensifies.....
                    try:
                        if 'schoologyUserAccessToken' in session:
                            tryCookies = connectionCheck(userAccessToken=session.get('schoologyUserAccessToken'),
                                            userAccessTokenSecret=session.get('schoologyUserAccessTokenSecret'))
                            return tryCookies
                        else:
                            return False # No keys anywhere...
                    except:
                        return False # Can't find keys yo.
        else:
            # Now we'll try what's in the cookie.
            auth.access_token_secret = userAccessTokenSecret
            auth.access_token = userAccessToken
            check = auth.authorize()
            if check ==  True:
                sc = schoolopy.Schoology
                sc = schoolopy.Schoology(auth)
                sc.limit = 5000
                return True
            elif check == False:
                return False
    except:
        return False
def devConnect():
    # Uses two-leg authentication and the keys we have in settings to connect a REPL to schoology.
    sc = schoolopy.Schoology(schoolopy.Auth(settings['apiKey'], settings['apiSecret']))
    return sc
def showMe():
    # More of a test, gives information about the user logged in,
    sc.limit = 5
    me = sc.get_me()
    me = me.name_display
    return me
def schoolGroups():
    # Gets you a dictionary of school-wide groups and their schoology IDs.
    groups = {}
    for group in sc.get_groups():
        groups[group.id] = group.title
    return groups
def groupEvents():
    # Gets you a dictionary of group events and their IDs
    events = {}
    for event in sc.get_events(group_id=settings['reportingGroupID']):
        events[event.id] = event.title
    return events
# def getGroupMembersUserNames():
#     # Gets you a dictionary of users and their usernames
#     sc.get_group


