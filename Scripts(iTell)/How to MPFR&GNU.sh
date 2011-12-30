curl -O -L http://www.mpfr.org/mpfr-current/mpfr-3.1.0.tar.gz
cd ~
tar xfvz mpfr-3.1.0.tar.gz
cd mpfr
mkdir build
cd build
../configure
make -j2
sudo make install
curl -O -L ftp://ftp.gnu.org/gnu/gmp/gmp-5.0.2.tar.gz
cd ~
tar xfvz gmp-5.0.2.tar.gz
cd mpfr
mkdir build
cd build
../configure
make -j2
sudo make install