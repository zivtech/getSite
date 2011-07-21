def makeVhostData(siteName, siteFolder):
  vhostData = """<Directory /var/www/""" + siteName + """/webroot/>
  Options FollowSymLinks
  AllowOverride None
  # Protect files and directories from prying eyes.
  <FilesMatch "\.(engine|inc|info|install|module|profile|po|schema|sh|.*sql|theme|tpl(\.php)?|xtmpl)$|^(code-style\.pl|Entries.*|Repository|Root|Tag|Template)$">
    Order allow,deny
  </FilesMatch>
  RewriteEngine On
  RewriteBase /
        <Files "cron.php">
    Order Deny,Allow
    Deny from all
    Allow from localhost
    Allow from 127.0.0.1
  </Files>
  # Rewrite URLs of the form 'index.php?q=x'.
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule ^(.*)$ index.php?q=$1 [L,QSA]
</Directory>
<VirtualHost *:80>
  ServerName """ + siteName + """.local 
  DocumentRoot /var/www/""" + siteName + """/webroot
  LogLevel warn
  CustomLog """ + siteFolder + """/logs/access.log combined
  ErrorLog  """ + siteFolder + """/logs/access.log
  ServerSignature Off
</VirtualHost>
  """
  return vhostData

def makeSettingsPHPDataD6(database, username, password):
  dict = {"database": database, "username": username, "password": password}
  settingsPHPData = """<?php
ini_set('arg_separator.output',     '&amp;');
ini_set('magic_quotes_runtime',     0);
ini_set('magic_quotes_sybase',      0);
ini_set('session.cache_expire',     200000);
ini_set('session.cache_limiter',    'none');
ini_set('session.cookie_lifetime',  0);
ini_set('session.gc_maxlifetime',   200000);
ini_set('session.save_handler',     'user');
ini_set('session.use_cookies',      1);
ini_set('session.use_only_cookies', 1);
ini_set('session.use_trans_sid',    0);
ini_set('url_rewriter.tags',        '');

$db_url = 'mysqli://%(username)s:%(password)s@localhost/%(database)s';
""" % dict
  return settingsPHPData

def makeSettingsPHPDataD7(database, username, password):
  dict = {"database": database, "username": username, "password": password}
  settingsPHPData =  """<?php
ini_set('arg_separator.output',     '&amp;');
ini_set('magic_quotes_runtime',     0);
ini_set('magic_quotes_sybase',      0);
ini_set('session.cache_expire',     200000);
ini_set('session.cache_limiter',    'none');
ini_set('session.cookie_lifetime',  0);
ini_set('session.gc_maxlifetime',   200000);
ini_set('session.save_handler',     'user');
ini_set('session.use_cookies',      1);
ini_set('session.use_only_cookies', 1);
ini_set('session.use_trans_sid',    0);
ini_set('url_rewriter.tags',        '');

$databases = array (
  'default' =>
  array (
    'default' =>
    array (
      'database' => '%(database)s',
      'username' => '%(username)s',
      'password' => '%(password)s',
      'host' => 'localhost',
      'port' => '',
      'driver' => 'mysql',
      'prefix' => '',
    ),
  ),
);
""" % dict
  return settingsPHPData
