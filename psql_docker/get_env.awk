#! /bin/awk -f
BEGIN { FS = "=" }
/NAME/ { print $2 }
/HOST/ { print $2 }
/PASSWORD/ { print $2 }
/SECRET/ { print $2 }
/USER/ { print $2 }
/PORT/ { print $2 }
