###runs only with GAWK
#  
BEGIN { firstline=1;}

{
 if( ($0 !~ /#/)  && (NF != 0)){

      if( (/[a-z]/ || /[A-Z]/) && (/E/ || /e/) && (/+/ || /-/) ){print $0;}
 ## && 0 !( (~ /E+/) || (~ /E-/)||(~ /e+/)||(~ /e-/))){print $0;}
     #printf "Number of fields " NF "\n";
     
     printf  "\n"; 

   }
         
}


END  { }


