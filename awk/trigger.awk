###runs only with GAWK
# 
BEGIN {flag=0 }

	{
	if ( ($2 == 3.00000) && (flag ==0)) {print $0; flag=1}
	if ( ($2 != 3.00000) && (flag ==1)) { flag=0}
	}

	

END  { }




