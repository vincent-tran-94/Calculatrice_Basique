sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-comm>

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_>

sudo apt update

apt-cache policy docker-ce

sudo apt install docker-ce