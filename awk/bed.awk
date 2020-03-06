###runs only with GAWK
#Script to spit out data from bill bedfords data
BEGIN { FS = " " }

	{while(   (getline !=0) ){ 
	    v1=$3
	    #print $0
	    getline 
	    #print $0
	    v2=$3
	    v3=$2

	 #getline 
	 #getline 
	 #v4=$3
	 printf "%f %f %f  \n", -v1 ,-(v2)/(755.4*3.1415), v3*.11*755.4
	
 	 #printf "%f %f %f  \n", v1 ,v2,v3
	    }
	}

	

END  { #printf "%02d:%06.3f \n",  int(time/60), time%60
close("tmp_out")}

function scale(N, temp)
{

while( (getline < "tmp_out") !=0){ if( $0 !~ /#/){print $1,$2/temp} }

}


