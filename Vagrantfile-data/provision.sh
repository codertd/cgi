set -e

package() {
  sudo yum -y install $1
}

conf_template() {
    if [ -f $PROJECT_ROOT/conf/$1 ]; then
        echo "Backing up $1"
        cp $PROJECT_ROOT/conf/$1 $PROJECT_ROOT/conf/$1.bak
    fi
    cp $VAGRANTFILE_DATA/conf/$1 $PROJECT_ROOT/conf/$1
}

echo "-- Installing EPEL repo"
package epel-release

echo "-- Installing Apache"
package httpd mod_ssl

echo "-- Installing Perl deps"
package perl-Try-Tiny perl-CGI perl-JSON perl-Test-Most perl-DateTime perl-TimeDate

echo "-- Installing PHP"
package php php-mysql php-mbstring

echo "-- Installing MySQL"
package mysql-server

echo "-- Setting up $PROJECT_NAME's Apache config"
chmod 755 $PROJECT_ROOT/../
#sudo sed -i 's/\#EnableSendfile off/EnableSendfile on/' /etc/httpd/conf/httpd.conf
#sudo sed -i '/DocumentRoot "\/var\/www\/html"/d' /etc/httpd/conf/httpd.conf
sudo cp $VAGRANTFILE_DATA/conf/httpd/httpd.conf /etc/httpd/conf/httpd.conf
sudo service httpd restart

#echo "-- Creating $PROJECT_NAME configuration"
