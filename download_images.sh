for ((i=$1;i<=$2;i++))
do
wget -P images/test/unlabeled/ http://micampus.mxl.cetys.mx/fotos/0$i.jpg
done
