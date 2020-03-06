###runs only with GAWK
#  
BEGIN { firstline=1;}

{

 if( ($0 ~ /#/)) { printf "%s \n", $0; } # echo the comment lines for clarity
 if( ($0 !~ /#/)  && (NF != 0)){
     #printf "Number of fields " NF "\n";
  #printf "%f %f %f %f %f ", $1+12.18, $2-113.8, $3-113.8, $4-113.8, $5-113.8;
  #printf "%f %f %f %f %f ", $1+12.18, $2-100.0, $3-100.0, $4-100.0, $5-100.0;
  #printf "%f %f %f %f %f ", $1, $2-104.004, $3-99.1211, $6-134.277, $7-142.09;
  #printf "%f %f %f %f %f %f %f", $1, $2-170.898, $3-166.016, $4-172.363, 
   #                $5-172.852, $6-178.223, $7-172.852;
  # if ( $1 < -.1){printf "%f %f", $2, $1+.1}
#printf "%f %f %f %f %f %f %f", $1+13.81, $2, $3, $4, $5,$6,$7;
#printf "%f %f %f %f %f %f %f", $1+35.56, $2-170, $3-170, $4-170, $5-170,$6-170,$7-170;
     printf "%f %f", $1+35.56, $2/1000.0
     for ( i=1; i <= NF; i++){
         #if ( i == column){ printf ($i)+shift " " ;}
         #else { printf $i " "}
         #printf "\n";
        }
     printf  "\n"; 

   }
         
}


END  { }


	