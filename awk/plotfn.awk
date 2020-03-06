###runs only with GAWK
# 
BEGIN { FS = " "; tsolid=3; dt=tsolid/99}
{
	{for(i=0; i<100; i++ ){ 
	  time=dt*i+1
	
printf "%f %f \n",time, 60000.0*(2*time- (time*time/2.0)-1)


	    }
	}

}

