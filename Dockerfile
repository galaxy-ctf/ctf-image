FROM bgruening/galaxy-stable:17.05
MAINTAINER Galaxy CTF Group <galaxians+ctf@hx42.org>

ENV GALAXY_CONFIG_MASTER_API_KEY=p5Nzo6cjUO66Dh08dAiITJzekj6OvM \
	GALAXY_CONFIG_BRAND="CTF 2017" \
	GALAXY_CONFIG_ADMIN_USERS=admin@galaxy.org \
	NONUSE=nodejs,proftp,reports,condor \
	CTF_TOOLSHED_URL="http://toolshed.ctf.galaxians.org/" \
	GALAXY_CONFIG_FTP_UPLOAD_DIR="/ftp" \
	GALAXY_CONFIG_SHOW_WELCOME_WITH_LOGIN=True \
	GALAXY_CONFIG_FLAG="gccctf{environmental_protection_agency}" \
	GALAXY_CONFIG_REQUIRE_LOGIN=True

# Don't put ID_SECRET in environment (or can be found with jq chall) but directly in ini file
#RUN cp $GALAXY_ROOT/config/galaxy.ini.sample $GALAXY_ROOT/config/galaxy.ini && \
    #sed -i 's/#id_secret = USING THE DEFAULT IS NOT SECURE!/id_secret = gccctf{make_sure_you_trust_the_tools_you_install}/' $GALAXY_ROOT/config/galaxy.ini

RUN pip install ephemeris loremipsum -U

RUN add-tool-shed --url 'http://toolshed.ctf.galaxians.org/' --name 'CTF Tool Shed'
RUN add-tool-shed --url 'https://testtoolshed.g2.bx.psu.edu/' --name 'Test Tool Shed'
ADD galaxy-sleep.py $GALAXY_ROOT/sleep.py
ADD create_galaxy_user.py /usr/local/bin/create_galaxy_user.py


ADD docker/ctf_tools.yml $GALAXY_ROOT/other_ctf_tools.yml

RUN startup_lite && \
	$GALAXY_ROOT/sleep.py http://localhost:8080 && \
	shed-install -a $GALAXY_CONFIG_MASTER_API_KEY -t other_ctf_tools.yml -g "http://localhost:8080"


######################
# Challenge configs
######################

## Copy Flag directory
ADD flags /flags/

## Populate FTP directory for Find The Phlag challenge TODO: also add to non-admin user's FTP dir
ADD challenges/other/09_Find_The_Phlag/flag*.txt /ftp/admin@galaxy.org/
RUN chown -R galaxy:galaxy /ftp

## Hide flag in datatypes
ADD challenges/datatypes_conf.xml $GALAXY_ROOT/config/

## Hide flag in users
ADD challenges/other/12_user_management/ $GALAXY_ROOT/

## Hide flag in data tables
ADD challenges/other/13_reference_data/ $GALAXY_ROOT/challenges/
RUN $GALAXY_ROOT/challenges/configure_reference_data.sh

## Hide flag in uname output in admin job metrics
RUN sed -i 's|return "Operating System", value|return "Operating System", value + "gccctf{admins_get_more_job_info}"|' $GALAXY_ROOT/lib/galaxy/jobs/metrics/instrumenters/uname.py

## Hide flag in converter
ADD challenges/other/15_converters/files/* $GALAXY_ROOT/lib/galaxy/datatypes/converters/
ADD challenges/other/15_converters/images/* /flags/

## Hide flag in dbkeys
ADD challenges/tools/11_dbkeys/builds.txt $GALAXY_ROOT/tool-data/shared/ucsc/builds.txt

## Hide flag for tool-dev chall to read
RUN echo "Well done tool developer! gccctf{t00l_devel0pment_1s_345y}" > /home/read_this_flag.txt

## Hide flag in pages
# TODO: move pages to regular user's account or publish
ADD challenges/other/16_pages/makepage.py $GALAXY_ROOT/challenges/makepage.py
ADD challenges/data/viz_exploration_qr/data/ /data/a/
ADD challenges/data/viz_exploration_jb/data/ /data/b/
ADD challenges/data/viz_exploration_circ/data/ /data/c/
ADD docker/setup_data_libraries.py $GALAXY_ROOT/setup_data_libraries.py
ADD docker/library_data.yaml $GALAXY_ROOT/library_data.yaml
## configures things that require a running Galaxy instance
ADD toolshed/setup_toolshed.py /setup_toolshed.py
RUN sed -i 's|service postgresql start|service postgresql start; while ! pg_isready; do sleep 1; done;|' /usr/bin/startup_lite
RUN startup_lite && \
	$GALAXY_ROOT/sleep.py http://localhost:8080 && \
	/bin/bash -c "source $GALAXY_VIRTUAL_ENV/bin/activate; \
	pip install statsd graphitesend; \
	python $GALAXY_ROOT/make_users.py -g http://localhost:8080 -a $GALAXY_CONFIG_MASTER_API_KEY" && \
	python $GALAXY_ROOT/setup_data_libraries.py -i $GALAXY_ROOT/library_data.yaml
	#&& \
	#python /setup_toolshed.py -g $GALAXY_ROOT -c make_yaml -t ${CTF_TOOLSHED_URL} --galaxy_url "http://localhost:8080" && \
	#shed-install -a ${GALAXY_CONFIG_MASTER_API_KEY} -t ctf_tools.yml -g "http://localhost:8080"



## Install Tours
#ADD ./rna-workbench-tours/rnaseq-tour.yaml $GALAXY_ROOT/config/plugins/tours/rnateam.rnaseq.yaml

# Download training data and populate the data library
#RUN startup_lite && \
    #sleep 30 && \
    #. $GALAXY_VIRTUAL_ENV/bin/activate && \

#ADD docker/parsec.yml /home/galaxy/.parsec.yml
#RUN startup_lite && \
    #sleep 30 && \
    #. $GALAXY_VIRTUAL_ENV/bin/activate && \
    #pip install git+https://github.com/galaxy-iuc/parsec/ && \
    #cd $GALAXY_ROOT/tools/challenges/ && make docker_scripts

# Add visualisations
#RUN curl -sL https://github.com/bgruening/galaxytools/archive/master.tar.gz > master.tar.gz && \
    #tar -xf master.tar.gz galaxytools-master/visualisations && \
    #cp -r galaxytools-master/visualisations/dotplot/ config/plugins/visualizations/ && \
    #cp -r galaxytools-master/visualisations/dbgraph/ config/plugins/visualizations/ && \
    #rm -rf master.tar.gz rm galaxytools-master

# Container Style
#ADD assets/img/logo.png $GALAXY_CONFIG_DIR/web/welcome_image.png
ADD docker/welcome.html $GALAXY_CONFIG_DIR/web/welcome.html

# Setup
ADD run.sh /run.sh

# Telegraf for monitoring
RUN cd / && \
	wget https://dl.influxdata.com/telegraf/releases/telegraf-1.3.0_linux_amd64.tar.gz && \
	tar xfz telegraf-1.3.0_linux_amd64.tar.gz --strip-components=2 -C / && \
	printf "[program:telegraf]\ncommand = /usr/bin/telegraf\nuser = galaxy\nautostart = true\nautorestart = true" > /etc/supervisor/conf.d/telegraf.conf
ADD telegraf.conf /etc/telegraf/telegraf.conf


# only enable CTF toolshed
RUN sed -i 's|<tool_shed name="Test Tool Shed" url="https://testtoolshed.g2.bx.psu.edu/" />||' $GALAXY_ROOT/config/tool_sheds_conf.xml 
#\
	#&& sed -i 's|<tool_shed name="Galaxy Main Tool Shed" url="https://toolshed.g2.bx.psu.edu/" />||' $GALAXY_ROOT/config/tool_sheds_conf.xml

CMD ["/run.sh"]
