###runs only with GAWK
#Script to scale a particular column in a data set for now
# To do: have variable column numbers
BEGIN { FS = " " }
	{while( getline !=0 ){ 
#	         v2=$2
#		if ($2 < 0)v2=0
#	  printf "%f %f \n",  $1+14.14, v2
#	printf "%d,", $2
#	printf "%s %s \n ", $1, $2
	if( $2 == "S1") printf "%s,", $1 >>"file1"
	if( $2 == "S2") printf "%s,", $1 >>"file2"
	if( $2 == "S3") printf "%s,", $1 >>"file3"
	if( $2 == "S4") printf "%s,", $1 >>"file4"
#	printf "%s %s \n ", $5, $6
	if( $6 == "S1") printf "%s,", $5 >>"file1"
	if( $6 == "S2") printf "%s,", $5 >>"file2"
	if( $6 == "S3") printf "%s,", $5 >>"file3"
	if( $6 == "S4") printf "%s,", $5 >>"file4"
	
	 }   
	}

END  {close("tmp_out")}

function scale(N, temp)
{

#following stuff to do frictional torque calc
	#printf "%f %f %f \n", $1, -$2*(755.4*3.1415), $3/(.11*755.4)
	#R1=$3
	#R2=$2
	R1=$3/(.11*755.4)
	R2=-$2*(755.4*3.1415)
        mu=0.22
#	P1=(R1+ mu*R2)/(1+mu*mu)
#	P2=(-R2+ mu*R1)/(1+mu*mu)
#FOLLOWING FOR GOING UP
	P1=(-R2+ mu*R1)/(1+mu*mu)
	P2=-(R2+ mu*R1)/(1+mu*mu)
	if (P1 < 0.0) {P1=0.0}
	if (P2 < 0.0) {P2=0.0}
	printf "%f %f %f %f \n", $1, P1*mu*404.24 , P2*mu*400.71,  P1*mu*404.24 +P2*mu*400.71


#while( (getline < "tmp_out") !=0){ if( $0 !~ /#/){print $1,$2/temp} }

}


