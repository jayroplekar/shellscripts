###runs only with GAWK
#  
BEGIN { firstline=1;}

{

 if( ($0 ~ /#/)) { printf "%s \n", $0; } # echo the comment lines for clarity
 if( ($0 !~ /#/)  && (NF != 0)){
   printf " %d, %d, %d, %d, %d, %d, %d \n", $1, $2, $4, $3, $5, $7, $6
   
   }
         
}


END  { }


	