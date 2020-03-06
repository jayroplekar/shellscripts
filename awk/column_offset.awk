###runs only with GAWK
#  
BEGIN { firstline=1;}

{
 if( $0 !~ /#/){
         if (  firstline == 1){
         tmp=$columno;  firstline =0;}
         else {
            printf  $columno-tmp; printf "\n";  tmp=$columno;}

             }
}

	

END  { #printf "%02d:%06.3f \n",  int(time/60), time%60
close("tmp_out")}


