###runs only with GAWK
#
# To do: have variable column numbers
BEGIN { FS = " " }
       {
	 while( getline !=0 ){
	  
	   if ( $1 == "50000") {
	     #print $0;
	     disp= $4;
	       while( (getline !=0) )
		 {
		   if($1 == "50000") {force=$4; break;}			   
		 }
	       printf "%f %f \n", -disp, -force;
	   }
	  }   
	}

END  {}

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


