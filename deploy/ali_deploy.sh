#!/bin/sh
set -x

module=$1


# cd /Users/gufy/Documents/blog/house/; tar -zcf house.tar.gz app; mv house.tar.gz /Users/gufy/Documents/blog/house/deploy/;
# scp /Users/gufy/Documents/blog/house/deploy/house.tar.gz root@121.196.209.144:/home/deploy;

scp(){
	cd /Users/gufy/Documents/blog/house/; tar -zcf house.tar.gz app; mv house.tar.gz /Users/gufy/Documents/blog/house/deploy/;
	sshpass -p "Pingmi$2020" scp /Users/gufy/Documents/blog/house/deploy/house.tar.gz root@121.196.209.144:/home/deploy/;
}

deploy(){
ssh root@121.196.209.144 'cd /home/house/; rm -rf app; tar -xf /home/deploy/house.tar.gz'
}

restart(){
ssh root@172.31.2.138 'cd /home/house/bin; ./stop_uwsgi.sh; sleep 10; ./start_uwsgi.sh;'
}



if [ ${module} = "scp" ];then
	scp $;
elif [ ${module} = "deploy" ];then
	deploy $;	
elif [ ${module} = "restart" ];then
	restart $;
else echo "please input the right module."
fi