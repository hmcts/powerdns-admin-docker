import os
basedir = os.path.abspath(os.path.dirname(__file__))

# BASIC APP CONFIG
SECRET_KEY = 'We are the world'
BIND_ADDRESS = '0.0.0.0'
PORT = 9191

# TIMEOUT - for large zones
TIMEOUT = 10

# LOG CONFIG
#  	- For docker, LOG_FILE=''
LOG_LEVEL = 'INFO'
LOG_FILE = ''

# UPLOAD DIRECTORY
UPLOAD_DIR = os.path.join(basedir, 'upload')

# DATABASE CONFIG
SQLA_DB_USER = os.getenv('PDA_DB_USER', '')
SQLA_DB_PASSWORD = os.getenv('PDA_DB_PASSWORD', '')
SQLA_DB_HOST = os.getenv('PDA_DB_HOST', '')
SQLA_DB_PORT = os.getenv('PDA_DB_PORT', 5432)
SQLA_DB_NAME = os.getenv('PDA_DB_NAME', '')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# DATABASE - MySQL
SQLALCHEMY_DATABASE_URI = 'postgresql://'+SQLA_DB_USER+':'+SQLA_DB_PASSWORD+'@'+SQLA_DB_HOST+':'+str(SQLA_DB_PORT)+'/'+SQLA_DB_NAME

# DATABASE - SQLite
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'pdns.db')

# SAML Authentication
SAML_ENABLED = os.environ.get('SAML_ENABLED') == 'true'
SAML_DEBUG = os.environ.get('SAML_DEBUG') == 'true'
SAML_PATH = os.path.join(os.path.dirname(__file__), 'saml')
##Example for ADFS Metadata-URL
#SAML_METADATA_URL = 'https://login.microsoftonline.com/rpe899.onmicrosoft.com/FederationMetadata/2007-06/FederationMetadata.xml'
SAML_METADATA_URL = os.environ.get('SAML_METADATA_URL')
#Cache Lifetime in Seconds
SAML_METADATA_CACHE_LIFETIME = 900

# SAML SSO binding format to use
## Default: library default (urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect)
#SAML_IDP_SSO_BINDING = 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'

## EntityID of the IdP to use. Only needed if more than one IdP is
##   in the SAML_METADATA_URL
### Default: First (only) IdP in the SAML_METADATA_URL
### Example: https://idp.example.edu/idp
#SAML_IDP_ENTITY_ID = 'https://idp.example.edu/idp'
## NameID format to request
### Default: The SAML NameID Format in the metadata if present,
###   otherwise urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified
### Example: urn:oid:0.9.2342.19200300.100.1.1
#SAML_NAMEID_FORMAT = 'urn:oid:0.9.2342.19200300.100.1.1'

## Attribute to use for Email address
### Default: email
### Example: urn:oid:0.9.2342.19200300.100.1.3
SAML_ATTRIBUTE_EMAIL = 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress'

## Attribute to use for Given name
### Default: givenname
### Example: urn:oid:2.5.4.42
#SAML_ATTRIBUTE_GIVENNAME = 'urn:oid:2.5.4.42'

## Attribute to use for Surname
### Default: surname
### Example: urn:oid:2.5.4.4
#SAML_ATTRIBUTE_SURNAME = 'urn:oid:2.5.4.4'
SAML_ATTRIBUTE_NAME = 'http://schemas.microsoft.com/identity/claims/displayname'
## Attribute to use for username
### Default: Use NameID instead
### Example: urn:oid:0.9.2342.19200300.100.1.1
SAML_ATTRIBUTE_USERNAME = 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress'

## Attribute to get admin status from
### Default: Don't control admin with SAML attribute
### Example: https://example.edu/pdns-admin
### If set, look for the value 'true' to set a user as an administrator
### If not included in assertion, or set to something other than 'true',
###  the user is set as a non-administrator user.
#SAML_ATTRIBUTE_ADMIN = 'https://example.edu/pdns-admin'

## Attribute to get admin group from
### Default: Don't control admin with SAML attribute
### Example: https://example.edu/pdns-admin-group
### If set, look for the value 'true' to set a user as an administrator
### If not included in assertion, or set to something other than 'true',
###  the user is set as a non-administrator user.
SAML_ATTRIBUTE_GROUP = 'http://schemas.microsoft.com/ws/2008/06/identity/claims/groups'
#SAML_GROUP_ADMIN_NAME = '356b57d8-84f4-457a-b49e-9500820c0b2d'
SAML_GROUP_ADMIN_NAME = os.environ.get('SAML_GROUP_ADMIN_NAME')
## Attribute to get group to account mappings from
### Default: None
### If set, the user will be added and removed from accounts to match
###  what's in the login assertion if they are in the required group
#SAML_GROUP_TO_ACCOUNT_MAPPING = '9189d86a-e260-4c3d-8227-803123cdce84=cnp'
SAML_GROUP_TO_ACCOUNT_MAPPING = os.environ.get('SAML_GROUP_TO_ACCOUNT_MAPPING')

## Attribute to get account names from
### Default: Don't control accounts with SAML attribute
### If set, the user will be added and removed from accounts to match
###  what's in the login assertion. Accounts that don't exist will
###  be created and the user added to them.
#SAML_ATTRIBUTE_ACCOUNT = 'https://example.edu/pdns-account'

SAML_SP_ENTITY_ID = os.environ.get('SAML_SP_ENTITY_ID')
#SAML_SP_ENTITY_ID = 'http://127.0.0.1:9191'
SAML_SP_CONTACT_NAME = '<contact name>'
SAML_SP_CONTACT_MAIL = '<contact mail>'
#Configures if SAML tokens should be encrypted.
#If enabled a new app certificate will be generated on restart
SAML_SIGN_REQUEST = False

# Configures if you want to request the IDP to sign the message
# Default is True
SAML_WANT_MESSAGE_SIGNED = False

#Use SAML standard logout mechanism retrieved from idp metadata
#If configured false don't care about SAML session on logout.
#Logout from PowerDNS-Admin only and keep SAML session authenticated.
SAML_LOGOUT = False
#Configure to redirect to a different url then PowerDNS-Admin login after SAML logout
#for example redirect to google.com after successful saml logout
#SAML_LOGOUT_URL = 'https://google.com'