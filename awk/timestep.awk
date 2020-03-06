###runs only with GAWK
# 
BEGIN { FS = " "; dt=tsolid/99}

	{for(i=0; i<100; i++ ){ 
	  time=dt*i
#min:sec
# printf "%02d:%04.1f \n",  int(time/60),time%60

#HR:min:sec 

printf "%01d:%02d:%02d \n",int(time/3600),int(time/60)-60*int(time/3600),time%60

#>"select_time_steps"
#	 printf "%02d:%06.3f \n",  int(time/60),time%60
#	 printf "%01d:%02d:%02d \n",
#int(time/3600),int(time/60)-60*int(time/3600),time%60 >"select_time_steps"
# printf "%06.1f \n", time
	    }
	}

	

END  { #printf "%02d:%06.3f \n",  int(time/60), time%60
close("tmp_out")}

function scale(N, temp)
{

while( (getline < "tmp_out") !=0){ if( $0 !~ /#/){print $1,$2/temp} }

}


