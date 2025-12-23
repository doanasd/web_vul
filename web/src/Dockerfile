# Use PHP 8.0 with Apache as the base image
FROM php:8.0-apache

# Set environment variables for noninteractive mode and time zone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Ho_Chi_Minh

# Install PHP extensions using docker-php-ext-install
RUN docker-php-ext-install mysqli

# Install required packages
RUN apt-get update -y && \
    apt-get install -y g++ flex bison curl apache2-dev \
        doxygen libyajl-dev ssdeep liblua5.2-dev \
        libgeoip-dev libtool dh-autoreconf \
        libcurl4-gnutls-dev libxml2 libpcre++-dev \
        libxml2-dev git wget tar apache2 nano apt-transport-https gnupg2 \
        autoconf automake pkg-config && \
    wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - && \
    echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list && \
    apt-get update && \
    apt-get install -y filebeat packetbeat libpcap0.8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and install LibModSecurity
RUN git clone https://github.com/SpiderLabs/ModSecurity.git && \
    cd ModSecurity && \
    git submodule init && \
    git submodule update && \
    ./build.sh && \
    ./configure && \
    make && \
    make install

# Install ModSecurity Apache Connector
RUN git clone https://github.com/SpiderLabs/ModSecurity-apache && \
    cd ModSecurity-apache && \
    ./autogen.sh && \
    ./configure --with-libmodsecurity=/usr/local/modsecurity/ && \
    make && \
    make install

# Load the Apache ModSecurity Connector Module
RUN echo "LoadModule security3_module /usr/lib/apache2/modules/mod_security3.so" >> /etc/apache2/apache2.conf

# Configure ModSecurity
RUN mkdir /etc/apache2/modsecurity.d && \
    cp ModSecurity/modsecurity.conf-recommended /etc/apache2/modsecurity.d/modsecurity.conf && \
    cp ModSecurity/unicode.mapping /etc/apache2/modsecurity.d/ && \
    sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/apache2/modsecurity.d/modsecurity.conf

ADD modsec_rules.conf /etc/apache2/modsecurity.d/

# Install OWASP ModSecurity Core Rule Set (CRS)
RUN git clone https://github.com/SpiderLabs/owasp-modsecurity-crs.git /etc/apache2/modsecurity.d/owasp-crs && \
    cp /etc/apache2/modsecurity.d/owasp-crs/crs-setup.conf.example /etc/apache2/modsecurity.d/owasp-crs/crs-setup.conf

# Update Apache configuration to activate ModSecurity
RUN mv /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/000-default.conf.old
ADD 000-default.conf /etc/apache2/sites-available/

# Set working directory
WORKDIR /var/www/html/

# Copy website files to the container
COPY ./WEB .

# Remove default Apache index.html file
RUN rm -rf /var/www/html/index.html

# Change permissions for the images directory
RUN chown -R www-data:www-data /var/www/html/img/ && \
    chmod -R 777 /var/www/html/img/

# Expose port 80 to the outside world
EXPOSE 80

# Start Apache server in the foreground
CMD ["apache2ctl", "-D", "FOREGROUND"]

