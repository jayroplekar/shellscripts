###runs only with GAWK
# 
BEGIN { FS = " "; }

	{
	 	
        if( NF != 0){
           if ($1 == 0.0){ min=$2; max=$2; minpt=$1; maxpt=$1}
           
           if ( $2 > max){ max=$2;  maxpt=$1}
           if ( $2 < min){ min=$2;  minpt=$1}
           #printf "%d %s \n", NR, $0
              }
	}

	

END  {printf "Max:  %e Min:  %e Range:  %e Avg: %e \n", max,  min, 
max-min, (max+min)/2.0 }

function scale(N, temp)
{

while( (getline < "tmp_out") !=0){ if( $0 !~ /#/){print $1,$2/temp} }

}


