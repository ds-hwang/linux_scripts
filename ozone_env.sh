export WLD=$HOME/install
# change this to another location if you prefer
export LD_LIBRARY_PATH=$WLD/lib
export PKG_CONFIG_PATH=$WLD/lib/pkgconfig/:$WLD/share/pkgconfig/
export ACLOCAL="aclocal -I $WLD/share/aclocal"

$@
